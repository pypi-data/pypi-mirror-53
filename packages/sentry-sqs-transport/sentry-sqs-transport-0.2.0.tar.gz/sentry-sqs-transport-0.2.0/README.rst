Sentry SDK SQS Transport
========================

.. image:: https://img.shields.io/pypi/v/sentry_sqs_transport.svg
        :target: https://pypi.python.org/pypi/sanic_openid_connect_provider

.. image:: https://img.shields.io/travis/terrycain/sentry-sqs-transport.svg
        :target: https://travis-ci.org/terrycain/sanic-openid-provider

.. image:: https://pyup.io/repos/github/terrycain/sentry-sqs-transport/shield.svg
     :target: https://pyup.io/repos/github/terrycain/sanic-openid-provider/
     :alt: Updates

Simple AWS SQS sentry-sdk transport that takes ideas from https://github.com/Netflix-Skunkworks/raven-sqs-proxy

It closely follows the HTTPTransport just substituting the HTTP POST section with an SQS Send Message.

Below is an example of how to use the transport.

.. code:: python

    import sentry_sdk
    from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration
    from sentry_sqs_transport import SQSTransport

    sentry_sdk.init(
        dsn="https://00000000000000000000000000000000@sentry.example.org/11",
        integrations=[AwsLambdaIntegration()],
        transport=SQSTransport,

        # Optional
        sqs_queue_url='https://sqs.eu-west-2.amazonaws.com/000000000000/SomeQueue',
        sqs_client_kwargs={'region_name': 'us-east-1'}
    )

Configuration
-------------

To configure which SQS queue to use, pass ``sqs_queue_url`` into the SDK init function with the SQS queue url as the value.
You can also set ``SENTRY_SQS_QUEUE_URL`` envrionment variable.

The parameter ``sqs_client_kwargs`` should be a dictionary and will be passed into the boto3 client
like ``boto3.client('sqs', **sqs_client_kwargs)``.
