# -*- coding: utf-8 -*-

__title__ = "mygeotab-python"
__author__ = "Aaron Toth"
__version__ = "0.8.5"

import sys

from .api import Credentials
from .exceptions import MyGeotabException, AuthenticationException, TimeoutException

try:
    from .py3.api_async import API, server_call_async
except (SyntaxError, ImportError):
    from .api import API, server_call

__all__ = ["API", "Credentials", "MyGeotabException", "AuthenticationException", "TimeoutException", "server_call"]

py_version = sys.version_info[:3]
if py_version >= (3, 5, 0):
    __all__.append("server_call_async")
