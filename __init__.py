from os import getenv
from os.path import join

from flask import Blueprint

from webapi.libs.config import Config
from webapi.libs.log import Logger

description: str = "Upload and tag files"

bp: Blueprint = None
name: str = None
logger: Logger = None
config: Config = None
provides_pages: list = [
    ('Files', 'dashboard')
]


def set_blueprint(blueprint: Blueprint):
    global bp
    bp = blueprint

    from . import routes
