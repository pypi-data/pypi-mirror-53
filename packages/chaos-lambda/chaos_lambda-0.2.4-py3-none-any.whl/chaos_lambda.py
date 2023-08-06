# -*- coding: utf-8 -*-
"""
Chaos Injection for AWS Lambda - chaos_lambda
======================================================

|docs| |issues| |Maintenance| |Pypi| |Travis| |Coveralls| |twitter|

.. |docs| image:: https://readthedocs.org/projects/aws-lambda-chaos-injection/badge/?version=latest
    :target: https://aws-lambda-chaos-injection.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |twitter| image:: https://img.shields.io/twitter/url/https/github.com/adhorn/aws-lambda-chaos-injection?style=social
    :alt: Twitter
    :target: https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Fadhorn%2Faws-lambda-chaos-injection

.. |issues| image:: https://img.shields.io/github/issues/adhorn/aws-lambda-chaos-injection
    :alt: Issues

.. |Maintenance| image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
    :alt: Maintenance
    :target: https://GitHub.com/adhorn/aws-lambda-chaos-injection/graphs/commit-activity

.. |Pypi| image:: https://badge.fury.io/py/chaos-lambda.svg
    :target: https://badge.fury.io/py/chaos-lambda

.. |Travis| image:: https://api.travis-ci.org/adhorn/aws-lambda-chaos-injection.svg?branch=master
    :target: https://travis-ci.org/adhorn/aws-lambda-chaos-injection

.. |Coveralls| image:: https://coveralls.io/repos/github/adhorn/aws-lambda-chaos-injection/badge.svg?branch=master
    :target: https://coveralls.io/github/adhorn/aws-lambda-chaos-injection?branch=master

``chaos_lambda`` is a small library injecting chaos into `AWS Lambda
<https://aws.amazon.com/lambda/>`_.
It offers simple python decorators to do `delay`, `exception` and `statusCode` injection
and a Class to add `delay` to any 3rd party dependencies called from your function.
This allows to conduct small chaos engineering experiments for your serverless application
in the `AWS Cloud <https://aws.amazon.com>`_.

* Support for Latency injection using ``delay``
* Support for Exception injection using ``exception_msg``
* Support for HTTP Error status code injection using ``error_code``
* Using for SSM Parameter Store to control the experiment using ``isEnabled``
* Support for adding rate of failure using ``rate``. (Default rate = 1)
* Per Lambda function injection control using Environment variable (``CHAOS_PARAM``)

Install
--------
.. code:: shell

    pip install chaos-lambda


Example
--------
.. code:: python

    # function.py

    import os
    from chaos_lambda import inject_delay, inject_exception, inject_statuscode

    # this should be set as a Lambda environment variable
    os.environ['CHAOS_PARAM'] = 'chaoslambda.config'

    @inject_exception
    def handler_with_exception(event, context):
        return {
            'statusCode': 200,
            'body': 'Hello from Lambda!'
        }


    @inject_exception(exception_type=TypeError, exception_msg='foobar')
    def handler_with_exception_arg(event, context):
        return {
            'statusCode': 200,
            'body': 'Hello from Lambda!'
        }

    @inject_exception(exception_type=ValueError)
    def handler_with_exception_arg_2(event, context):
        return {
            'statusCode': 200,
            'body': 'Hello from Lambda!'
        }


    @inject_statuscode
    def handler_with_statuscode(event, context):
        return {
            'statusCode': 200,
            'body': 'Hello from Lambda!'
        }

    @inject_statuscode(error_code=400)
    def handler_with_statuscode_arg(event, context):
        return {
            'statusCode': 200,
            'body': 'Hello from Lambda!'
        }

    @inject_delay
    def handler_with_delay(event, context):
        return {
            'statusCode': 200,
            'body': 'Hello from Lambda!'
        }

    @inject_delay(delay=1000)
    def handler_with_delay_arg(event, context):
        return {
            'statusCode': 200,
            'body': 'Hello from Lambda!'
        }


    @inject_delay(delay=0)
    def handler_with_delay_zero(event, context):
        return {
            'statusCode': 200,
            'body': 'Hello from Lambda!'
        }


When excecuted, the Lambda function, e.g ``handler_with_exception('foo', 'bar')``, will produce the following result:

.. code:: shell

    exception_msg from config I really failed seriously with a rate of 1
    corrupting now
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "/.../chaos_lambda.py", line 199, in wrapper
        raise Exception(exception_msg)
    Exception: I really failed seriously

Configuration
-------------
The configuration for the failure injection is stored in the `AWS SSM Parameter Store
<https://aws.amazon.com/ssm/>`_ and accessed at runtime by the ``get_config()``
function:

.. code:: json

    {
        "isEnabled": true,
        "delay": 400,
        "error_code": 404,
        "exception_msg": "I really failed seriously",
        "rate": 1
    }

To store the above configuration into SSM using the `AWS CLI <https://aws.amazon.com/cli>`_ do the following:

.. code:: shell

    aws ssm put-parameter --region eu-north-1 --name chaoslambda.config --type String --overwrite --value "{ \"delay\": 400, \"isEnabled\": true, \"error_code\
": 404, \"exception_msg\": \"I really failed seriously\", \"rate\": 1 }"

AWS Lambda will need to have `IAM access to SSM <https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-access.html>`_.

.. code:: json

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "ssm:DescribeParameters"
                ],
                "Resource": "*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "ssm:GetParameters",
                    "ssm:GetParameter"
                ],
                "Resource": "arn:aws:ssm:eu-north-1:12345678910:parameter/chaoslambda.config"
            }
        ]
    }


Supported Decorators:
---------------------
``chaos_lambda`` currently supports the following decorators:

* `@inject_delay` - add delay in the AWS Lambda execution
* `@inject_exception` - Raise an exception during the AWS Lambda execution
* `@inject_statuscode` - force AWS Lambda to return a specific HTTP error code

and the following class:

* `SessionWithDelay` - enabled to sub-classing requests library and call dependencies with delay

More information:
-----------------


"""

from __future__ import division, unicode_literals
from functools import wraps, partial
import os
import time
import logging
import random
import json
import requests
from ssm_cache import SSMParameter
from ssm_cache.cache import InvalidParameterError

LOGGER = logging.getLogger(__name__)

__version__ = '0.2.4'


def get_config(config_key):
    """
Retrieve the configuration from the SSM parameter store
The config always returns a tuple (value, rate)
value: requested configuration
rate: the injection probability (default 1 --> 100%)

How to use::

    >>> import os
    >>> from chaos_lambda import get_config
    >>> os.environ['CHAOS_PARAM'] = 'chaoslambda.config'
    >>> get_config('delay')
    (400, 1)
    >>> get_config('exception_msg')
    ('I really failed seriously', 1)
    >>> get_config('error_code')
    (404, 1)
    """
    param = SSMParameter(os.environ['CHAOS_PARAM'])
    try:
        value = json.loads(param.value)
        if not value["isEnabled"]:
            return 0, 0
        return value[config_key], value.get('rate', 1)
    except InvalidParameterError as ex:
        # key does not exist in SSM
        raise InvalidParameterError("{} is not a valid SSM config".format(ex))
    except KeyError as ex:
        # not a valid Key in the SSM configuration
        raise KeyError("key {} not valid or found in SSM config".format(ex))


def inject_delay(func=None, delay=None):
    """
Add delay to the lambda function - delay is returned from the SSM paramater
using ``get_config('delay')`` which returns a tuple delay, rate.

Default use::

    >>> @inject_delay
    ... def handler(event, context):
    ...    return {
    ...       'statusCode': 200,
    ...       'body': 'Hello from Lambda!'
    ...    }
    >>> handler('foo', 'bar')
    Injecting 400 of delay with a rate of 1
    Added 402.20ms to handler
    {'statusCode': 200, 'body': 'Hello from Lambda!'}

With argument::

    >>> @inject_delay(delay=1000)
    ... def handler(event, context):
    ...    return {
    ...       'statusCode': 200,
    ...       'body': 'Hello from Lambda!'
    ...    }
    >>> handler('foo', 'bar')
    Injecting 1000 of delay with a rate of 1
    Added 1002.20ms to handler
    {'statusCode': 200, 'body': 'Hello from Lambda!'}

    """
    if not func:
        return partial(inject_delay, delay=delay)

    @wraps(func)
    def wrapper(*args, **kwargs):
        _is_enabled, _ = get_config('isEnabled')
        if not _is_enabled:
            return func(*args, **kwargs)

        if isinstance(delay, int):
            _delay = delay
            rate = 1
        else:
            _delay, rate = get_config('delay')
            if not _delay:
                return func(*args, **kwargs)

        LOGGER.info(
            "Injecting %d ms of delay with a rate of %s",
            _delay, rate
        )

        start = time.time()
        if _delay > 0 and rate >= 0:
            # add latency approx rate% of the time
            if round(random.random(), 5) <= rate:
                LOGGER.debug('sleeping now')
                time.sleep(_delay / 1000.0)

        end = time.time()

        LOGGER.debug(
            'Added %.2fms to %s',
            (end - start) * 1000,
            func.__name__
        )

        return func(*args, **kwargs)
    return wrapper


def inject_exception(func=None, exception_type=None, exception_msg=None):
    """
Forces the lambda function to fail and raise an exception
using ``get_config('exception_msg')`` which returns a tuple exception_msg, rate.

Default use (Error type is Exception)::

    >>> @inject_exception
    ... def handler(event, context):
    ...     return {
    ...        'statusCode': 200,
    ...        'body': 'Hello from Lambda!'
    ...     }
    >>> handler('foo', 'bar')
    Injecting exception_type <class "Exception"> with message I really failed seriously a rate of 1
    corrupting now
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "/.../chaos_lambda.py", line 316, in wrapper
            raise _exception_type(_exception_msg)
    Exception: I really failed seriously

With Error type argument::

    >>> @inject_exception(exception_type=ValueError)
    ... def lambda_handler_with_exception_arg_2(event, context):
    ...     return {
    ...         'statusCode': 200,
    ...         'body': 'Hello from Lambda!'
    ...     }
    >>> lambda_handler_with_exception_arg_2('foo', 'bar')
    Injecting exception_type <class 'ValueError'> with message I really failed seriously a rate of 1
    corrupting now
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "/.../chaos_lambda.py", line 316, in wrapper
            raise _exception_type(_exception_msg)
    ValueError: I really failed seriously

With Error type and message argument::

    >>> @inject_exception(exception_type=TypeError, exception_msg='foobar')
    ... def lambda_handler_with_exception_arg(event, context):
    ...     return {
    ...         'statusCode': 200,
    ...         'body': 'Hello from Lambda!'
    ...     }
    >>> lambda_handler_with_exception_arg('foo', 'bar')
    Injecting exception_type <class 'TypeError'> with message foobar a rate of 1
    corrupting now
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "/.../chaos_lambda.py", line 316, in wrapper
            raise _exception_type(_exception_msg)
    TypeError: foobar

    """
    if not func:
        return partial(
            inject_exception,
            exception_type=exception_type,
            exception_msg=exception_msg
        )

    @wraps(func)
    def wrapper(*args, **kwargs):
        _is_enabled, _ = get_config('isEnabled')
        if not _is_enabled:
            return func(*args, **kwargs)

        rate = 1
        if isinstance(exception_type, type):
            _exception_type = exception_type
        else:
            _exception_type = Exception

        if exception_msg:
            _exception_msg = exception_msg
        else:
            _exception_msg, rate = get_config('exception_msg')

        LOGGER.info(
            "Injecting exception_type %s with message %s a rate of %d",
            _exception_type,
            _exception_msg,
            rate
        )

        # add injection approx rate% of the time
        if round(random.random(), 5) <= rate:
            LOGGER.debug("corrupting now")
            raise _exception_type(_exception_msg)

        return func(*args, **kwargs)
    return wrapper


def inject_statuscode(func=None, error_code=None):
    """
Forces the lambda function to return with a specific Status Code
using ``get_config('error_code')`` which returns a tuple error_code, rate.

Default use::

    >>> @inject_statuscode
    ... def handler(event, context):
    ...    return {
    ...       'statusCode': 200,
    ...       'body': 'Hello from Lambda!'
    ...    }
    >>> handler('foo', 'bar')
    Injecting Error 404 at a rate of 1
    corrupting now
    {'statusCode': 404, 'body': 'Hello from Lambda!'}

With argument::

    >>> @inject_statuscode(error_code=400)
    ... def lambda_handler_with_statuscode_arg(event, context):
    ...     return {
    ...         'statusCode': 200,
    ...         'body': 'Hello from Lambda!'
    ...     }
    >>> lambda_handler_with_statuscode_arg('foo', 'bar')
    Injecting Error 400 at a rate of 1
    corrupting now
    {'statusCode': 400, 'body': 'Hello from Lambda!'}
    """
    if not func:
        return partial(inject_statuscode, error_code=error_code)

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        _is_enabled, _ = get_config('isEnabled')
        if not _is_enabled:
            return result

        if isinstance(error_code, int):
            _error_code = error_code
            rate = 1
        else:
            _error_code, rate = get_config('error_code')
        LOGGER.info("Injecting Error %s at a rate of %d", _error_code, rate)
        # add injection approx rate% of the time
        if round(random.random(), 5) <= rate:
            LOGGER.debug("corrupting now")
            result['statusCode'] = _error_code
            return result

        return result
    return wrapper


class SessionWithDelay(requests.Session):
    """
    This is a class for injecting delay to 3rd party dependencies.
    Subclassing the requests library is useful if you want to conduct other chaos experiments
    within the library, like error injection or requests modification.
    This is a simple subclassing of the parent class requests.Session to add delay to the request method.

    Usage::

       >>> from chaos_lambda import SessionWithDelay
       >>> def dummy():
       ...     session = SessionWithDelay(delay=300)
       ...     session.get('https://stackoverflow.com/')
       ...     pass
       >>> dummy()
       Added 300.00ms of delay to GET

    """

    def __init__(self, delay=None):
        super(SessionWithDelay, self).__init__()
        self.delay = delay

    def request(self, method, url, *args, **kwargs):
        LOGGER.info('Added %.2fms of delay to %s', self.delay, method)
        time.sleep(self.delay / 1000.0)
        return super(SessionWithDelay, self).request(method, url, *args, **kwargs)
