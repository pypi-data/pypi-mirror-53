"""
Loader
======

A simple wrapper for the `requests` library to handle loading pages.

>>> from soupstars.loaders import Loader
>>> loader = Loader()
>>> loader.load('https://www.google.com')
<Response [200]>
"""

import requests


class Loader(object):

    def __init__(self):
        self.handler = requests.request

    def load(self, url, method='get', *args, **kwargs):
        """
        :param url: the url to download and parse
        :type url: str
        """

        return self.handler(method, url, *args, **kwargs)
