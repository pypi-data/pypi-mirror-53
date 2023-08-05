"""
Parsers
=======

Parsers transform the modules defined by a user into an object usable by
the workers to actually parse a web page.
"""

import os
import re
import importlib
from urllib.parse import urlparse
from typing import Tuple, Dict, List, Callable

from bs4 import BeautifulSoup

from .decorators import DATA_NAME, FOLLOW_NAME, EXCLUDE_NAME, LINKS_NAME


class Url(str):
    """
    An enhanced string object to simplify handling URLs
    """

    @property
    def netloc(self):
        """
        The netloc (more commonly called the domain) of the url
        """

        return urlparse(self).netloc

    @property
    def domain(self):
        """
        Alias for netloc
        """

        return self.netloc

    @property
    def scheme(self):
        """
        The scheme of the url, for example `http` or `https`
        """

        return urlparse(self).scheme

    @property
    def path(self):
        """
        The path of the url, excluding any anchors or query params
        """

        return urlparse(self).path

    @property
    def query(self):
        """
        The query string on the url
        """

        return urlparse(self).query

    def match(self, search):
        return re.search(search, self) is not None


class BeautifulSoupStar(BeautifulSoup):
    """
    An enhanced BeautifulSoup object, with additional helper methods
    """

    def __init__(self, response):
        self.response = response
        self.request = self.response.request
        self.status_code = response.status_code
        self.url = Url(self.request.url)
        super().__init__(markup=self.response.text, features='html.parser')

    def find_text(self, text):
        result = self.find(text=re.compile(text))
        if result:
            return result.parent

    def find_class(self, klass):
        regex = re.compile(klass)
        return self.find_all(attrs={'class': regex})

    def harmonize(self, url):
        url = Url(url)
        # If the link is relative, use the domain from the original request
        # Actually I think we can just use the netloc without any formatting
        netloc = url.netloc or self.url.netloc

        # Remove starting slashes from path, they'll be added later
        if url.path.startswith('/'):
            path = url.path[1:]
        else:
            path = url.path

        if url.query:
            query = f'?{url.query}'
        else:
            query = ''

        return Url(f"{self.url.scheme}://{netloc}/{path}{query}")

    def links(self):
        return [self.harmonize(a['href']) for a in self.find_all(href=True)]

    def title(self):
        return self.find('title').text


class Parser(object):
    """
    Responsible for applying a user's parser module to the response from a
    loader.
    """

    @classmethod
    def from_string(klass, string):
        string = string.replace('.py', '').replace(os.path.sep, '.')
        module = importlib.import_module(string)
        return klass(module)

    def __init__(self, module):
        self.module = module

    def _get_soupstars_attr(self, name: str, multiple: bool = False):
        results = []
        for k, v in vars(self.module).items():
            if hasattr(v, '_soupstars') and v._soupstars == name:
                attr = v
                if multiple:
                    results.append(v)
                else:
                    return v
        else:
            return results

    def parsers(self) -> Dict:
        """
        A dictionary containing
        """

        parsers = list(self._get_soupstars_attr(DATA_NAME, multiple=True))
        return {p.__name__: p for p in parsers}

    def seeds(self) -> List:
        """
        A list of urls defined by the parser, used as the starting points when
        running a crawler.
        """

        seeds = getattr(self.module, 'seeds', [])
        seeds.extend(getattr(self.module, 'urls', []))
        if hasattr(self.module, 'url'):
            seeds.append(self.module.url)
        return [Url(s) for s in seeds]

    def exclude(self, soup: BeautifulSoupStar) -> bool:
        """
        A function pulled from the module to determine if the page's data
        should be excluded from the run
        """

        excludor = self._get_soupstars_attr(EXCLUDE_NAME)
        if not excludor:
            excludor = lambda x: False
        return excludor(soup)

    def follow(self, url: Url) -> bool:
        """
        A function pulled from the module to determine if a particular link
        should be followed (ie downloaded)
        """

        validator = self._get_soupstars_attr(FOLLOW_NAME)
        if not validator:
            validator = lambda x: True
        return validator(url)

    def data(self, soup: BeautifulSoupStar) -> Dict:
        """
        Loads the data and any associated errors from applying the user's
        parsing function.
        """

        data = {}
        errors = {}
        for k, v in self.parsers().items():
            try:
                data[k] = v(soup)
                errors[k] = None
            except Exception as err:
                data[k] = None
                errors[k] = str(err)
        else:
            return {
                "data": data,
                "errors": errors,
                "url": soup.url,
                "status_code": soup.status_code
            }

    def links(self, soup: BeautifulSoupStar) -> List[Url]:
        """
        Uses the `links` function defined on the parser to pull links from
        the response.
        """

        for k,v in vars(self.module).items():
            if hasattr(v, '_soupstars') and v._soupstars == LINKS_NAME:
                links = v(soup)
                break
        else:
            links = soup.links()

        items = list(filter(self.follow, links))
        return items

    def parse(self, response):
        soup = BeautifulSoupStar(response)
        if self.exclude(soup):
            data = None
        else:
            data = self.data(soup)
        links = self.links(soup)
        return data, links
