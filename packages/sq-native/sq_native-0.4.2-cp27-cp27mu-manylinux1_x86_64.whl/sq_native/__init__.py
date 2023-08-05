# -*- coding: utf-8 -*-
# Copyright (c) 2016, 2017, 2018, 2019 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
"""Sqreen Python Native Module"""
import ctypes
import logging
import os
import sys

try:
    import pkg_resources
except ImportError:
    pkg_resources = None  # pragma: no cover

from .__about__ import __lib_version__

LOGGER = logging.getLogger(__name__)


class C_PWVersion(ctypes.Structure):

    _fields_ = [
        ("major", ctypes.c_uint16),
        ("minor", ctypes.c_uint16),
        ("patch", ctypes.c_uint16)
    ]

    def as_tuple(self):
        """Return the version as a tuple."""
        return int(self.major), int(self.minor), int(self.patch)

    def __str__(self):
        """Return the version as a string."""
        return ".".join([str(x) for x in self.as_tuple()])


def _get_lib_path(name):
    """Return the path of the library called `name`."""
    if os.name == "posix" and sys.platform == "darwin":
        prefix, ext = "lib", ".dylib"
    elif sys.platform == "win32":
        prefix, ext = "", ".dll"
    else:
        prefix, ext = "lib", ".so"
    fn = None
    if pkg_resources is not None:
        fn = pkg_resources.resource_filename("sq_native", prefix + name + ext)
    if fn is None:
        root_dir = os.path.dirname(os.path.abspath(__file__))
        fn = os.path.join(root_dir, prefix + name + ext)
    return fn


def _load_library(name):
    """Load a native library located in this module."""
    path = _get_lib_path(name)
    LOGGER.debug("Loading %s", path)
    return ctypes.cdll.LoadLibrary(path)


LOG_LEVEL_MAP = [
    None,
    logging.DEBUG,
    logging.INFO,
    logging.WARNING,
    logging.ERROR
]


LOG_FUNC_TYPE = ctypes.CFUNCTYPE(
    None, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p,
    ctypes.c_int, ctypes.c_char_p, ctypes.c_size_t)


@LOG_FUNC_TYPE
def _log_callback(level, func, filename, line, msg, msg_len):
    try:
        level = LOG_LEVEL_MAP[level]
        if level is not None:
            LOGGER.log(level, "%s:%d:%s %s", filename.decode("utf-8"), line,
                       func.decode("utf-8"), msg.decode("utf-8"))
    except Exception:
        LOGGER.warning("Log callback from the native library has failed")


NOT_LOADED = object()
lib = NOT_LOADED


def get_lib():
    """Get an instance of the Sqreen library."""
    global lib

    if lib is None or lib is NOT_LOADED:
        lib = _load_library("Sqreen")
        lib.powerwaf_getVersion.argstype = []
        lib.powerwaf_getVersion.restype = C_PWVersion

        lib_version = str(lib.powerwaf_getVersion())
        if lib_version != __lib_version__:
            raise RuntimeError("Native library version mismatch: {} != {}"
                               .format(lib_version, __lib_version__))

        lib.powerwaf_setupLogging.argstype = [LOG_FUNC_TYPE, ctypes.c_int]
        lib.powerwaf_setupLogging.restype = ctypes.c_bool
        # It is expensive to callback to Python code, set the default
        # log level to WARNING except if it was configured with something else.
        level = 1 if "SQREEN_WAF_LOG_LEVEL" in os.environ else 3
        if not lib.powerwaf_setupLogging(_log_callback, level):
            raise RuntimeError("Native library logging error")

    return lib


def get_lib_version():
    """Return the Sqreen library version or None if absent."""
    path = _get_lib_path("Sqreen")
    if path is not None and os.path.exists(path):
        return __lib_version__
    return None


__all__ = ["get_lib", "get_lib_version"]
