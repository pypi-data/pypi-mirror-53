"""
CFFI loader for Judy.
"""

from __future__ import absolute_import

from judyz_cffi.internal import _load

_load()

from .exceptions import JudyError  # noqa
from .judy1 import *  # noqa
from .judyl import *  # noqa
from .judysl import *  # noqa
