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
    sim_oauth_login()
