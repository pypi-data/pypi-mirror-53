# -*- coding: utf-8 -*-

from .error import (  # noqa: F401
    APIConnectionError, APIError, DepoError, PlaceUnavailableError
)
from .resource import Order, Place
from .utils import JSONEncoder

# Configuration variables
api_credentials = None

DEPO_API_ENDPOINT = 'https://admin.depo.sk/v2/api/'
