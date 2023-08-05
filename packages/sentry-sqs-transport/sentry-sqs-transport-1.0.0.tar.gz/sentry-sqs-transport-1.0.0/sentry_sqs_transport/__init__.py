import io
import os
import gzip
import base64
import json

import boto3
from sentry_sdk.transport import Transport
from sentry_sdk.utils import logger, capture_internal_exceptions
from sentry_sdk.worker import BackgroundWorker
from sentry_sdk._types import MYPY
from sentry_sdk.consts import DEFAULT_OPTIONS

if MYPY:
    from typing import Any, Optional, Dict
    from sentry_sdk._types import Event

__all__ = ['SQSTransport']

# Update default options to allow our specific sqs parameters
DEFAULT_OPTIONS['sqs_queue_url'] = None
DEFAULT_OPTIONS['sqs_client_kwargs'] = {}


class SQSTransport(Transport):
    """The default HTTP transport."""

    def __init__(
        self, options  # type: Dict[str, Any]
    ):
        # type: (...) -> None
        from sentry_sdk.consts import VERSION

        Transport.__init__(self, options)
        assert self.parsed_dsn is not None
        self._worker = BackgroundWorker()
        self._auth = self.parsed_dsn.to_auth("sentry.python/%s" % VERSION)
        self.options = options

        self._sqs_queue_url = options.get('sqs_queue_url')
        if not self._sqs_queue_url:
            self._sqs_queue_url = os.environ.get('SENTRY_SQS_QUEUE_URL')

        self._sqs_client_kwargs = options['sqs_client_kwargs']

        from sentry_sdk import Hub

        self.hub_cls = Hub

    def _send_event(
        self, event  # type: Event
    ):
        # type: (...) -> None

        # As this is ran in a thread
        sqs_client = boto3.client('sqs', **self._sqs_client_kwargs)

        body = io.BytesIO()
        with gzip.GzipFile(fileobj=body, mode="w") as f:
            f.write(json.dumps(event, allow_nan=False).encode("utf-8"))

        assert self.parsed_dsn is not None
        assert self._sqs_queue_url is not None

        logger.debug(
            "Sending event to SQS, type:%s level:%s event_id:%s project:%s host:%s"
            % (
                event.get("type") or "null",
                event.get("level") or "null",
                event.get("event_id") or "null",
                self.parsed_dsn.project_id,
                self.parsed_dsn.host,
            )
        )

        sqs_payload = json.dumps({
            'method': 'POST',
            'headers': {
                "User-Agent": str(self._auth.client),
                "X-Sentry-Auth": str(self._auth.to_header()),
                "Content-Type": "application/json",
                "Content-Encoding": "gzip",
            },
            'url': str(self._auth.store_api_url),
            'body': base64.b64encode(body.getvalue()).decode()
        })

        # TODO if message is greater than 256KiB then SQS wont take it, should add S3 ref fallback system
        try:
            sqs_client.send_message(
                QueueUrl=self._sqs_queue_url,
                MessageBody=sqs_payload

            )
        except Exception as err:
            logger.exception('Unexpected error whilst putting message on SQS', exc_info=err)

    def capture_event(
        self, event  # type: Event
    ):
        # type: (...) -> None
        hub = self.hub_cls.current

        def send_event_wrapper():
            # type: () -> None
            with hub:
                with capture_internal_exceptions():
                    self._send_event(event)

        self._worker.submit(send_event_wrapper)

    def flush(
        self,
        timeout,  # type: float
        callback=None,  # type: Optional[Any]
    ):
        # type: (...) -> None
        logger.debug("Flushing SQS transport")
        if timeout > 0:
            self._worker.flush(timeout, callback)

    def kill(self):
        # type: () -> None
        logger.debug("Killing SQS transport")
        self._worker.kill()
