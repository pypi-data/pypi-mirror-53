""" Linq for Python """

__version__ = '1.1.0'

try:
    from py_linq import Enumerable  # noqa
except ImportError:
    from py_linq.py_linq3 import Enumerable3 as Enumerable  # noqa
