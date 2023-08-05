"""
Decorators
==========

Decorators are the primary way Soup Stars learns about how to run your module.
"""


DATA_NAME = "data"
FOLLOW_NAME = "follow"
EXCLUDE_NAME = "exclude"
LINKS_NAME = 'links'


# Maybe we could rename this `extract` or `scrape`
def data(function):
    """
    Used to identify functions that process a web page and return relevant,
    extracted data

    ::

        from soupstars import parse

        @data
        def title(soup):
            return soup.title()

        @data
        def author(soup):
            return soup.find_class('author').text.strip()

    """

    function._soupstars = DATA_NAME
    return function


def follow(function):
    """
    Used to identify which links from the page to follow.

    ::

        from soupstars import follow

        @follow
        def follow(url):
            return url.domain == "spiderbites.nytimes.com"
    """

    function._soupstars = FOLLOW_NAME
    return function


def exclude(function):
    """
    Used to identify which pages to extract data from.

    ::

        from soupstars import include

        @include
        def include(soup):
            return soup.url.match("articles/")
    """

    function._soupstars = EXCLUDE_NAME
    return function


def links(function):
    """
    Used to control how the parser generates links from a page.

    ::

        from soupstars import links

        @links
        def link_generator(soup):
            if soup.url.domain == 'dont-crawl-me.com':
                return []
            else:
                return soup.links()
    """

    function._soupstars = LINKS_NAME
    return function
