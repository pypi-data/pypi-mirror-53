"""
Client
======

Wrapper for the SoupStars web API.

>>> from soupstars import Client
>>> client = Client()
>>> resp = client.status()
>>> resp.json['healthy']
True

"""

import os
import requests
import json

from .config import Config


class Routes(object):
    health = "/health"
    login = "/token"
    register = '/register'
    ls = '/list'
    profile = '/profile'
    pull = '/pull'
    push = '/push'
    run = '/run'
    results = '/results'
    results_create = '/results/create'


class Client(object):
    routes = Routes()

    def __init__(self, token=None, **kwargs):
        self.config = Config(token=token, **kwargs)
        self.token = self.config.token

    def send(self, path, method='POST', data=None, files=None):
        url = self.config.host + path
        headers = {'Authorization': self.token}
        resp = requests.request(
            url=url,
            method=method,
            json=data,
            headers=headers,
            files=files
        )
        return resp

    def register(self, email, password):
        data = {
            'email': email,
            'password': password
        }
        return self.send(self.routes.register, data=data)

    def login(self, email, password):
        data = {
            'email': email,
            'password': password
        }
        return self.send(self.routes.login, data=data)

    def health(self):
        return self.send(self.routes.health, method='GET')

    def ls(self):
        return self.send(self.routes.ls)

    def profile(self):
        return self.send(self.routes.profile)

    def push(self, module):
        file_data = open(module, 'rb').read()
        files = {module: file_data}
        return self.send(self.routes.push, files=files)

    def pull(self, module):
        data = {'name': module}
        return self.send(self.routes.pull, data=data)

    def run(self, module, _async=False):
        data = {'name': module, 'async': _async}
        return self.send(self.routes.run, data=data)

    def results(self, module):
        data = {'name': module}
        return self.send(self.routes.results, data=data)

    def create_result(self, run_id, parser_id, data, status_code, url, errors):
        return self.send(self.routes.results_create, data={
            'result': {
                'run_id': run_id,
                'parser_id': parser_id,
                'data': data,
                'status_code': status_code,
                'url': url,
                'errors': errors
            }
        })
