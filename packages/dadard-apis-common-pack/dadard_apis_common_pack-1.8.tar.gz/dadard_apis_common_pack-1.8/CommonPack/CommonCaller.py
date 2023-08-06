import json

import requests

BASE_URL = 'http://dadard.fr:7000/api/v1/'
SUB_CHECK_ENDPOINT = 'sub'
PROFILE_CHECK_ENDPOINT = 'profile/infos'
STATUS_OK = 'ok'
STATUS_KO = 'ko'
TRUE = 'true'
FALSE = 'false'


def get_auth_header(profile_key):
    return {
        "Authorization": profile_key
    }

def check_profile_key(profile_key):
    headers = get_auth_header(profile_key)
    url = f"{BASE_URL}{PROFILE_CHECK_ENDPOINT}?{params}"

    r = requests.get(url, headers)
    status = json.loads(r.content.decode())['status']
    if status == STATUS_OK:
        return True

    return False


def call_sub(profile_key, api_name):
    headers = get_auth_header(profile_key)
    params = "api_name={an}".format(an=api_name)
    url = f"{BASE_URL}{SUB_CHECK_ENDPOINT}?{params}"

    r = requests.get(url, headers)
    return json.loads(r.content.decode())


def check_is_subscribed(profile_key, api_name):
    response = call_sub(profile_key, api_name)
    status = response['status']
    if status == STATUS_OK:
        is_subscribed = response['content']['is_subscribed']
        if is_subscribed == TRUE:
            return True

    return False


def check_is_not_subscribed(profile_key, api_name):
    response = call_sub(profile_key, api_name)
    status = response['status']
    if status == STATUS_OK:
        is_subscribed = response['content']['is_subscribed']
        if is_subscribed == FALSE:
            return True

    return False
