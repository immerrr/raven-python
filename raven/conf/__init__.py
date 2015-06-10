"""
raven.conf
~~~~~~~~~~

:copyright: (c) 2010-2012 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

import logging
import re

__all__ = ['setup_logging']

EXCLUDE_LOGGER_DEFAULTS = (
    'raven',
    'gunicorn',
    'south',
    'sentry.errors',
    'django.request',
)


class ExcludeLoggersByName(logging.Filter):
    """
    Don't log messages coming from specified loggers and their descendants.
    """
    def __init__(self, excluded_loggers):
        super(ExcludeLoggersByName, self).__init__()
        pattern = '|'.join(map(re.escape, excluded_loggers))
        self.excluded_logger_re = re.compile('(%s)(\\.|$)' % pattern)

    def filter(self, record):
        """Return True if record is to be logged."""
        return not self.excluded_logger_re.match(record.name)


def setup_logging(handler, exclude=EXCLUDE_LOGGER_DEFAULTS):
    """
    Configures logging to pipe to Sentry.

    - ``exclude`` is a list of loggers that shouldn't go to Sentry.

    For a typical Python install:

    >>> from raven.handlers.logging import SentryHandler
    >>> client = Sentry(...)
    >>> setup_logging(SentryHandler(client))

    Within Django:

    >>> from raven.contrib.django.handlers import SentryHandler
    >>> setup_logging(SentryHandler())

    Returns a boolean based on if logging was configured or not.
    """
    logger = logging.getLogger()
    if handler.__class__ in map(type, logger.handlers):
        return False

    handler.addFilter(ExcludeLoggersByName(EXCLUDE_LOGGER_DEFAULTS))
    logger.addHandler(handler)
    return True
