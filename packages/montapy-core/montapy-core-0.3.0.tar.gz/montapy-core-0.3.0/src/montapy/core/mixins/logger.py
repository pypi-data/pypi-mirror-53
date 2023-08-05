# pylint: disable=too-few-public-methods
"""
This module contains a mixin which adds a logging functionality to the
target class
"""
from logging import getLogger, Logger


class LoggerMixin:
    """ LoggerMixin mixin adds logger property to the target class. """
    @property
    def logger(self) -> Logger:
        if not hasattr(self, "_logger_instance_"):
            self._logger_instance_ = getLogger(self.__class__.__name__)

        return self._logger_instance_
