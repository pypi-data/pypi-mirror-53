# btrdb_admin.utils
# Utilities for the btrdb_admin database library.
#
# Author:   PingThings
# Created:  Mon Dec 17 15:23:25 2018 -0500
#
# For license information, see LICENSE.txt
# ID: utils.py [] allen@pingthings.io $

"""
Utilities for the btrdb_admin database library.
"""

##########################################################################
## Imports
##########################################################################

import os
import yaml
import warnings
from functools import wraps

from btrdb_admin.exceptions import ProfileNotFound, CredentialsFileNotFound


##########################################################################
## Module Variables
##########################################################################

BTRDB_ADMIN_ENDPOINTS = "BTRDB_ADMIN_ENDPOINTS"
BTRDB_ADMIN_USERNAME = "BTRDB_ADMIN_USERNAME"
BTRDB_ADMIN_PASSWORD = "BTRDB_ADMIN_PASSWORD"

CONFIG_DIR = ".predictivegrid"
CREDENTIALS_FILENAME = "credentials.yaml"


##########################################################################
## Functions
##########################################################################

def filter_none(f):
    """
    decorator for removing dict items with None as value
    """
    @wraps(f)
    def inner(*args, **kwargs):
        return  { k: v for k, v in f(*args, **kwargs).items() if v is not None }
    return inner


def get_credentials_path():
    """
    Returns the abspath to the credentials at ~/.predictivegrid/credentials.yaml
    """
    try:
        return os.path.join(os.environ["HOME"], CONFIG_DIR, CREDENTIALS_FILENAME)
    except KeyError:
        raise CredentialsFileNotFound("no home directory to locate credentials")


def load_credentials_from_file():
    """
    Returns a dict of the credentials file contents

    Returns
    -------
    dict
        A dictionary of profile connection information
    """
    try:
        with open(get_credentials_path(), 'r') as stream:
            return yaml.safe_load(stream)
    except FileNotFoundError as exc:
        raise CredentialsFileNotFound(
            "Cound not find `{}`".format(get_credentials_path())
        ) from exc


@filter_none
def credentials_by_profile(name=None):
    if not name:
        name = os.environ.get("BTRDB_PROFILE", 'default')

    # load from credentials yaml file
    try:
        creds = load_credentials_from_file()
    except PermissionError:
        warnings.warn("Permission denied '{}'".format(get_credentials_path()))
        return {}
    except CredentialsFileNotFound as e:
        warnings.warn(str(e))
        return {}

    if name not in creds.keys():
        if name == 'default':
            return {}
        raise ProfileNotFound("Profile `{}` not found in credentials file.".format(name))

    return creds[name]["admin"]


@filter_none
def credentials_by_env():
    """
    Returns the BTrDB connection information (as dict) using BTRDB_ADMIN_ENDPOINTS

    Returns
    -------
    dict
        A dictionary containing connection information
    """
    return {
        "endpoint": os.environ.get(BTRDB_ADMIN_ENDPOINTS, None),
        "username": os.environ.get(BTRDB_ADMIN_USERNAME,  None),
        "password": os.environ.get(BTRDB_ADMIN_PASSWORD, None),
    }


def credentials(endpoint=None, username=None, password=None):
    """
    Returns the BTrDB connection information (as dict)

    Parameters
    ----------
    endpoint: str
        server address
    username: str
        admin account username
    password: str
        admin account password

    Returns
    -------
    dict
        A dictionary of the requested profile's connection information

    """
    creds = {}
    credentials_by_arg = filter_none(lambda: { "endpoint": endpoint, "username": username, "password": password, })
    pipeline = (credentials_by_profile, credentials_by_env, credentials_by_arg)
    [creds.update(func()) for func in pipeline]
    return creds


def require_credentials(creds):
    """
    Raises an error if credentials are missing.

    Parameters
    ----------
    creds : dict
        A dictionary containing AdminAPI connection information

    Returns
    -------
    creds : dict
        The unmodified connection information

    raises : ValueError
        If a required parameter is missing or is otherwise invalid
    """
    envmap = {
        "endpoint": BTRDB_ADMIN_ENDPOINTS,
        "username": BTRDB_ADMIN_USERNAME,
        "password": BTRDB_ADMIN_PASSWORD,
    }

    for key, envvar in envmap.items():
        if key not in creds or not creds[key]:
            raise ValueError(
                "missing required credential '{}' please set ${}".format(key, envvar)
            )

    return creds