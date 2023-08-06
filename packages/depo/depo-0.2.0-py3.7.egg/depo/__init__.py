# -*- coding: utf-8 -*-

from .resource import Order, Place
from .error import (  # noqa: F401
    APIConnectionError, APIError, DepoError, PlaceUnavailableError
)

# Configuration variables
api_credentials = None

DEPO_API_ENDPOINT = 'https://admin.depo.sk/v2/api/'
