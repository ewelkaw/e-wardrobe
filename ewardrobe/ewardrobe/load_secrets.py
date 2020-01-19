import json
from pathlib import Path

# JSON based secrets module
from django.core.exceptions import ImproperlyConfigured

BASEDIR = Path(__file__).absolute().parent
try:
    with open(BASEDIR.joinpath("secrets.json")) as f:
        secrets = json.loads(f.read())
except FileNotFoundError:
    secrets = {}


def get_secret(setting, secrets=secrets):
    """ Trying to get setting key from secrets file if added"""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)
