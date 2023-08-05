import click
import os
import sys
import textwrap
import getpass

from ..clients import Client
from .printers import jsonify, pythonify


@click.group()
@click.option('--token', '-t', help="Token to use. Default None")
@click.option('--host', '-h', default="https://soupstars-cloud.herokuapp.com", help="Host to use. Default https://soupstars-cloud.herokuapp.com")
@click.pass_context
def cloud(context, token, host):
    """
    Commands to interact with SoupStars cloud.
    """

    context.obj = Client(token=token, host=host)


@cloud.command()
@click.pass_obj
def health(client):
    """
    Print the status of the SoupStars api
    """

    resp = client.health()
    jsonify(resp.json())


@cloud.command()
@click.pass_obj
def login(client):
    """
    Log in with an existing email
    """

    email = input('Email: ')
    password = getpass.getpass(prompt='Password: ')
    resp = client.login(email=email, password=password)

    if resp.ok:
        client.config.token = resp.json()['token']
        client.config.save()

    jsonify(resp.json())


@cloud.command()
@click.pass_obj
def ls(client):
    """
    Show the parsers uploaded to SoupStars cloud
    """

    resp = client.ls()
    jsonify(resp.json())


@cloud.command()
@click.pass_obj
def register(client):
    """
    Register a new account on SoupStars cloud
    """

    email = input('Email: ')
    password = getpass.getpass(prompt='Password: ')
    password2 = getpass.getpass(prompt='Confirm password: ')

    if password != password2:
        print("Passwords did not match.")
        return

    resp = client.register(email=email, password=password)

    if resp.ok:
        client.config.token = resp.json()['token']
        client.config.save()

    jsonify(resp.json())


@cloud.command()
@click.pass_obj
def whoami(client):
    """
    Print the email address of the current user
    """

    resp = client.profile()
    jsonify(resp.json())


@cloud.command()
@click.option('--module', '-m', required=True, help="Name of the parser to push")
@click.pass_obj
def push(client, module):
    """
    Push a parser to SoupStars cloud
    """

    resp = client.push(module)
    jsonify(resp.json())


@cloud.command()
@click.option('--module', '-m', required=True, help="Name of the parser to pull")
@click.pass_obj
def pull(client, module):
    """
    Pull a parser from SoupStars cloud into a local module
    """

    resp = client.pull(module)
    data = resp.json()
    with open(data['parser']['name'], 'w') as o:
        o.write(data['module'])
    jsonify({"state": "done", "response": data})


@cloud.command()
@click.option('--module', '-m', required=True, help="Name of the parser to create")
@click.pass_obj
def run(client, module):
    """
    Run a parser on SoupStars cloud
    """

    resp = client.run(module)
    jsonify(resp.json())


@cloud.command()
@click.option('--module', '-m', required=True, help="Name of the parser to show")
@click.option('--json/--no-json', default=False, help="Show parser details in JSON")
@click.pass_obj
def show(client, module, json):
    """
    Show the contents of a parser on SoupStars cloud
    """

    resp = client.pull(module)

    if json:
        jsonify(resp.json())
    else:
        pythonify(resp.json()['module'])


@cloud.command()
@click.option('--module', '-m', required=True, help="Name of the parser to test")
@click.pass_obj
def results(client, module):
    """
    Print results of a parser
    """

    resp = client.results(module)
    jsonify(resp.json())
