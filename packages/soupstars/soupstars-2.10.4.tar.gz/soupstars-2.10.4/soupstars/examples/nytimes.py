"""
Extract article links and metadata from nytimes.com
"""

from soupstars import data, follow, exclude


url = "https://www.nytimes.com"


@follow
def follow(url):
    return (url.domain == "www.nytimes.com") and (url.match("\d{4}\/\d{2}\/\d{2}"))


@exclude
def exclude(soup):
    return not soup.url.match("\d{4}\/\d{2}\/\d{2}")


@data
def title(soup):
    return soup.title()
