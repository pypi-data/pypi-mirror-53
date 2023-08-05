"""
Command Line Interface
======================

Soup Stars comes installed with a CLI to simplify various tasks.
"""


from .base import base
from .cloud import cloud

base.add_command(cloud)
