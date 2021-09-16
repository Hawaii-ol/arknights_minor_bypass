import json
import mitmproxy.http

from bilibili_config import *
from bilibili_api import api_myinfo

class BilibiliBypass:
    """
    By now we only support oauth2 login with the bilibili app
    You have to manually get your access token if you want to login with username and password!
    """
    def __init__(self):
        self.disposable_access_token = None
    
    def request(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.host in minor_guard_blacklist:
            flow.kill()
            print('Blocked: ' + flow.request.url)
    
    def response(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.url.startswith(api['app_3rd_auth']):
            # Record app's access token
            if not self.disposable_access_token:
                self.disposable_access_token = flow.request.urlencoded_form['access_token']
        elif flow.request.url.startswith(api['biligame_session_renew']):
            print('URL: ' + flow.request.url)
            resjson = flow.response.json()
            print('Original response:')
            print(resjson)
            # check if we are blocked by anti-addiction policies
            if resjson['code'] != 0 and resjson['user_limit_status'] == 2:
                # the access key we got from authorizeByApp api cannot be recognized by the server
                # resjson['access_key'] = flow.request.urlencoded_form['access_key']
                resjson['access_key'] = self.disposable_access_token
                resjson['expires'] = int(resjson['timestamp']) + 7776000
                resjson['h5_paid_download'] = 1
                resjson['h5_paid_download_sign'] = ''
                resjson['code'] = 0
                resjson['user_limit_status'] = 0
                print('Manipulated response:')
                print(resjson)
                flow.response.set_text(json.dumps(resjson))
        elif flow.request.url.startswith(api['biligame_user_info']):
            print('URL: ' + flow.request.url)
            resjson = flow.response.json()
            print('Original response:')
            print(resjson)
            # check if we are blocked by anti-addiction policies
            if resjson['code'] != 0 and resjson['user_limit_status'] == 2:
                # since we are blocked from login, we need to work around
                # and obatin user info from the bilibili app
                if not self.disposable_access_token:
                    self.disposable_access_token = flow.request.urlencoded_form['access_key']
                myinfo = api_myinfo(self.disposable_access_token)
                resjson['auth_name'] = 'hacked'
                resjson['face'] = myinfo['face']
                resjson['h5_paid_download'] = 1
                resjson['h5_paid_download_sign'] = ''
                resjson['realname_verified'] = 1
                resjson['remind_status'] = 0
                resjson['s_face'] = myinfo['face']
                resjson['uid'] = myinfo['mid']
                resjson['uname'] = myinfo['name']
                resjson['code'] = 0
                resjson['user_limit_status'] = 0
                print('Manipulated response:')
                print(resjson)
                flow.response.set_text(json.dumps(resjson))
                self.disposable_access_token = None

addons = [
    BilibiliBypass(),
]
