# -*- coding: utf-8 -*-

"""Utilities for PyBEL-CX."""

from .constants import VERSION

__all__ = [
    'get_version',
]


def get_version():
    """Get the version of PyBEL-CX."""
    return VERSION
