"""
Writers control where the results of crawls are stored.
"""

import csv
import importlib
import json
import os

from .clients import Client


class Writer(object):

    @classmethod
    def from_string(klass, string, url=None):
        class_name = f"{string.capitalize()}Writer"
        module = importlib.import_module('soupstars.writers')
        _Writer = getattr(module, class_name)
        return _Writer(url=url)

    def __init__(self, url=None):
        self.url = url


# I think we could do a TextWriter that optionally logs to the current direcfory
# or the soupstars home directory
class JsonWriter(Writer):
    def write(self, result):
        with open(self.url, 'a') as o:
            json.dump(result, o)
            o.write('\n')


class CsvWriter(Writer):
    def flatten(self, result):
        _result = {}
        errors = {f'{k}_error': v for k, v in result['errors'].items()}
        data = {k: str(v) for k, v in result['data'].items()}
        _result.update(url=result['url'])
        _result.update(status_code=result['status_code'])
        _result.update(data)
        _result.update(errors)
        return _result

    def write(self, result):
        result = self.flatten(result)
        with open(self.url, 'a') as o:
            _writer = csv.DictWriter(o, fieldnames=result.keys(), delimiter='\t')
            if o.tell() == 0:
                _writer.writeheader()
            _writer.writerow(result)


class CloudWriter(Writer):
    def __init__(self, url=None, parser_id=None, run_id=None):
        super().__init__(url=url)
        self.parser_id = parser_id
        self.run_id = run_id
        self.client = Client()

    def write(self, result):
        return self.client.create_result(
            run_id=self.run_id,
            parser_id=self.parser_id,
            data=result['data'],
            url=result['url'],
            status_code=result['status_code'],
            errors=result['errors']
        )
