import base64
import json
import logging
from typing import Dict, Any

import requests

logger = logging.getLogger('sentry-lambda')
logger.setLevel(logging.INFO)


def process_record(body: str, attributes: Dict[str, Any], session: requests.Session) -> None:
    try:
        json_data = json.loads(body)
    except ValueError:
        logger.warning('Sentry message is not valid json, skipping: {0}'.format(body))
        return

    # Some data validation
    valid = True
    for key in ('method', 'headers', 'url', 'body'):
        if key not in json_data:
            logger.warning('Invalid Sentry message, missing key {0}'.format(key))
            valid = True
    # This way we log out all message errors then skip.
    if not valid:
        return

    if json_data['method'] != 'POST':
        logger.warning('Invalid Sentry message, not a POST request')
        return

    sentry_payload = base64.b64decode(json_data['body'])

    try:
        resp = session.post(
            json_data['url'],
            headers=json_data['headers'],
            data=sentry_payload
        )
        if resp.status_code == 200:
            logger.info('Successfully posted Sentry message')
        else:
            logger.info('Failed to post Sentry message, got non-200 status code: {0}, text: {1}'.format(resp.status_code, resp.text))
    except Exception as err:
        logger.exception('Failed to POST to Sentry', exc_info=err)


def handler(event: Dict[str, Any], context) -> None:
    requests_session = requests.Session()
    requests_session.trust_env = True  # This should merge in proxy variables

    # logger.info(event)
    for record in event.get('Records', []):
        try:
            process_record(record['body'], record['messageAttributes'], requests_session)
        except Exception as err:
            logger.exception('Caught exception whilst processing Sentry message', exc_info=err)
            # TODO add messages back to queue with delay
            # record['eventSourceARN'] is queue ARN
