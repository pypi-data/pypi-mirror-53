import os
import json


class Config(object):
    token = None
    host = "https://soupstars-cloud.herokuapp.com"
    home = os.path.join(os.path.expanduser('~'), '.soupstars')
    fname = 'config.json'


    def __init__(self, host=None, token=None, home=None, fname=None):
        self.name =  fname or os.environ.get('SOUPSTARS_FNAME') or self.fname
        self.home =  home or os.environ.get('SOUPSTARS_HOME') or self.home
        self.path = os.path.join(self.home, self.name)
        self.logs = os.path.join(self.home, 'logs')

        if not os.path.exists(self.home):
            os.mkdir(self.home)
        if not os.path.exists(self.logs):
            os.mkdir(self.logs)

        config = self.load()
        self.host = host or os.environ.get('SOUPSTARS_HOST') or config['host']
        self.token = token or os.environ.get('SOUPSTARS_TOKEN') or config['token']  # noqa

    def to_dict(self):
        return {
            "host": self.host,
            "token": self.token
        }

    def save(self):
        with open(self.path, 'w') as o:
            json.dump(self.to_dict(), o, indent=2)

    def load(self):
        if not os.path.exists(self.path):
            self.save()
        with open(self.path) as o:
            return json.load(o)
