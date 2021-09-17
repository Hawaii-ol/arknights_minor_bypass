import argparse
import os
import requests
import time
import webbrowser
from urllib.parse import urlparse, parse_qs

from bilibili_config import *
from bilibili_api import signature, getkey, encryptpwd, api_verify_sms

def cli_get_user():
    username = input('输入用户名/邮箱/手机号：')
    password = input('输入密码：')
    return username, password

def cli_get_captcha():
    captcha = input('请填写图片中的验证码：')
    return captcha

def cli_get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mitm', action='store_true')
    return parser

def mitm_decorator(func):
    def wrapper(*args, **kwargs):
        print('您似乎正试图通过账号密码登录游戏，但显然失败了')
        print('请在下面的脚本中填写您的账号密码以实现自动登录')
        token_info = func(*args, **kwargs)
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), access_token_file)
        with open(file_path, 'w') as f:
            f.write(token_info['access_token'])
        print('设置成功！请重新回到游戏并在登录界面输入任意账号密码即可')
        return token_info
    return wrapper

def sim_oauth_login():
    print('--- BiliBili 自动登录脚本 ---')
    username, password = cli_get_user()
    params = basic_login_params.copy()
    params['username'] = username
    params['password'] = encryptpwd(password)
    params['ts'] = int(time.time())
    params['sign'] = signature(secret=login_appSecrect, **params)

    response = requests.post(api['login'], params=params, headers=headers)
    response.raise_for_status()
    rjson = response.json()
    if rjson['code'] != 0:
        raise requests.exceptions.HTTPError(
            'Login failed, server responds with "%s"' % rjson['message'])
    
    # SMS Validation
    data = rjson['data']
    if data['status'] == 2 and 'url' in data:
        print(data['message'])
        print('请将获取到的手机验证码填写在本程序中而不是获取页面中！！')
        print('按回车键跳转到验证码获取页面...')
        input()
        webbrowser.open_new(data['url'])
        code = input('请填写获取到的手机验证码：')
        qs = parse_qs(urlparse(data['url']).query)
        tmp_code = qs['tmp_token'][0]
        request_id = qs['requestId'][0]
        api_verify_sms(code, tmp_code, request_id)
        login_info = access_token_login(tmp_code)
        # print(login_info)
        token_info = login_info['token_info']
    else:
        token_info = data['token_info']
    print('登陆成功，您的uid为%d，access_token为%s，refresh_token为%s' % (
        token_info['mid'], token_info['access_token'], token_info['refresh_token']))
    print('请妥善保管好您的用户凭据！')
    return token_info

def access_token_login(code):
    params = basic_login_params.copy()
    params['code'] = code
    params['grant_type'] = 'volatile_code'
    params['ts'] = int(time.time())
    params['sign'] = signature(secret=login_appSecrect, **params)

    response = requests.get(api['access_token'], params=params, headers=headers)
    response.raise_for_status()
    rjson = response.json()
    if rjson['code'] != 0:
        raise requests.exceptions.HTTPError(
            'Login failed, server responds with "%s"' % rjson['message'])
    
    return rjson['data']


if __name__ == '__main__':
    parser = cli_get_parser()
    args = parser.parse_args()
    if args.mitm:
        sim_oauth_login = mitm_decorator(sim_oauth_login)
    sim_oauth_login()
