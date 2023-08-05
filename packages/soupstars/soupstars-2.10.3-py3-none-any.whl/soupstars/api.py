"""
API
===

Entrypoints for some of the functionality exposed by the package
"""

from .runners import Runner
from .loaders import Loader
from .parsers import BeautifulSoupStar, Url


def run(parser, **kwargs):
    """
    Executes a parser, returning the data from the run
    """

    return Runner(parser, **kwargs).run()


# I think we should rename the associated methods on the loader and parser
def fetch(url) -> BeautifulSoupStar:
    """
    Downloads a url and converts it into a BeautifulSoupStars object
    """

    loader = Loader()
    load = loader.load(url)
    soup = BeautifulSoupStar(load)
    return soup


# I think we should rename the associated methods on the loader and parser
def parse(parser, url):
    """
    Download a url and process it with a parser, returning the data and links
    discovered by the parsers
    """

    loader = Loader()
    load = loader.load(url)
    data, links = parser.parse(load)
    return data, links
