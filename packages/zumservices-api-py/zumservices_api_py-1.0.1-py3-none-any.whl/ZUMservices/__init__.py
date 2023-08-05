# Copyright (c) 2018 Fexra, The TurtleCoin Developers
# Copyright (c) 2019 ZumCoin Development Team
# Please see the included LICENSE file for more information.

import os
import requests
import json

BASE_URL = "https://api.zum.services/v1"
TOKEN = os.environ.get('ZUM_SERVICES_TOKEN')
TIMEOUT = os.environ.get('ZUM_SERVICES_TIMEOUT', 2000)

if not TOKEN:
    raise Exception('All methods require an JWT access token. See https://zum.services/documentation')

# Get Method
def _get(method):
    response = requests.get(
        BASE_URL + '/' + method,
        timeout = TIMEOUT,
        headers = { 'Authorization': 'Bearer ' + TOKEN }
    ).json()

    return response


# Post Method
def _post(method, params):
    response = requests.post(
        BASE_URL + '/' + method,
        timeout = TIMEOUT,
        headers = { 'Authorization': 'Bearer ' + TOKEN },
        json = params
    ).json()
    
    return response

# Delete Post
def _delete(method):
    response = requests.delete(
        BASE_URL + '/' + method,
        timeout = TIMEOUT,
        headers = { 'Authorization': 'Bearer ' + TOKEN },
    ).json()

    return response

from .lib import ZS