import base64
import hashlib
import requests
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from urllib.parse import urlencode

from bilibili_config import *

def signature(secret=appSecret, **kwargs):
    params = urlencode(sorted(kwargs.items()))
    params += secret
    md5 = hashlib.md5()
    md5.update(params.encode('utf-8'))
    return md5.hexdigest()

def getkey():
    params = {'appkey' : appkey, 'sign': signature(appkey=appkey)}
    response = requests.post(api['getkey'], params=params, headers=headers)
    response.raise_for_status()
    rjson = response.json()
    if rjson['code'] != 0:
        raise requests.exceptions.HTTPError(
            'Failed to get key, server responds with "%s"' % rjson['message'])
    return rjson['data']

def encryptpwd(pwd):
    data = getkey()
    salted = data['hash'] + pwd
    pubkey = RSA.import_key(data['key'])
    cipher = PKCS1_v1_5.new(pubkey)
    pwd = cipher.encrypt(salted.encode('utf-8'))
    return base64.b64encode(pwd).decode('utf-8')

def api_verify_sms(code, tmp_code, request_id):
    params = {
        'code': code,
        'request_id': request_id,
        'tmp_code': tmp_code,
        'type': 17
    }
    response = requests.post(api['verify_sms'], params=params, headers=headers)
    response.raise_for_status()
    rjson = response.json()
    if rjson['code'] != 0:
        raise requests.exceptions.HTTPError(
            'Verify SMS failed, server responds with "%s"' % rjson['message'])

def api_myinfo(access_key):
    params = basic_query_params.copy()
    params['access_key'] = access_key
    params['ts'] = int(time.time())
    params['sign'] = signature(**params)
    response = requests.get(api['myinfo'], params=params, headers=headers)
    response.raise_for_status()
    rjson = response.json()
    if rjson['code'] != 0:
        raise requests.exceptions.HTTPError(
            'Get myinfo failed, server responds with "%s"' % rjson['message'])
    return rjson['data']
