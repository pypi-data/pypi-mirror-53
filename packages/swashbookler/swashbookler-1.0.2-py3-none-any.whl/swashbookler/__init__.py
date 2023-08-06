"""Allows downloading books from Google Books and converting them to PDFs."""

from .core import download_book
from .exceptions import *

__version__ = '1.0.2'

__all__ = [
    'download_book'
]
