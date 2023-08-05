"""
Soup Stars is a framework for building web parsers with Python. It is designed
to make building, deploying, and scheduling web parsers easier by simplifying
what you need to get started.
"""

from .version import __version__
from .api import run, fetch, parse
from .parsers import BeautifulSoupStar, Url
from .decorators import data, follow, exclude, links
from .clients import Client
