# -*- coding: utf-8 -*-

from .error import CardbergError, APIConnectionError, APIError  # noqa: F401
from .resource import Card  # noqa: F401

# Configuration variables
api_credentials = None
timeout = 30

CARDBERG_API_ENDPOINT = "http://loys.cardberg.com/api/"
