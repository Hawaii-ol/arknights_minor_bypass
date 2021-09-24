import json
import os
import platform
import subprocess
import mitmproxy.http

from bilibili_config import *
from bilibili_api import api_myinfo

class BilibiliBypass:
    """
    supports both oauth2 login with Bilibili app and legacy login with username and password
    """
    def __init__(self):
        self.disposable_access_token = None
        self.token_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), access_token_file)

    def clear_token(self):
        self.disposable_access_token = None
        if os.path.exists(self.token_path):
            os.remove(self.token_path)
    
    def fill_user_info(self, data, access_key):
        print('Fetching myinfo with access_key=' + access_key)
        data['access_key'] = access_key
        data['expires'] = int(data['timestamp']) + 7776000
        myinfo = api_myinfo(access_key)
        data['auth_name'] = data.get('auth_name', 'hacked')
        data['face'] = myinfo['face']
        data['realname_verified'] = 1
        data['message'] = ''
        data['remind_status'] = 0
        data['s_face'] = myinfo['face']
        data['uid'] = myinfo['mid']
        data['uname'] = myinfo['name']
        data['code'] = 0
    
    def request(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.host in minor_guard_blacklist:
            flow.kill()
            print('Blocked: ' + flow.request.url)
    
    def response(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.url in (api['biligame_l1_login_v3'], api['biligame_l3_login_v3']):
            print('URL: ' + flow.request.url)
            resjson = flow.response.json()
            print('Original response:')
            print(resjson)
            # check if we are blocked by anti-addiction policies
            # 500002: 用户名或密码错误
            if int(resjson['code']) in [500051, 500002]:
                if not self.disposable_access_token:
                    # check if we have access_token file
                    if os.path.exists(self.token_path):
                        with open(self.token_path, 'r') as f:
                            self.disposable_access_token = f.read()
                if self.disposable_access_token:
                    # since we are blocked from login,
                    # we need to work around and obtain user info from Bilibili main site
                    self.fill_user_info(resjson, self.disposable_access_token)
                    print('Manipulated response:')
                    print(resjson)
                    flow.response.set_text(json.dumps(resjson))
                    self.clear_token()
                else:
                    # we don't have access_token yet so we have to login first
                    # prompt user to login via script
                    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bilibili_login.py')
                    if platform.system() == 'Windows':
                        subprocess.Popen(['python', script_path, '--mitm'],
                            creationflags=subprocess.CREATE_NEW_CONSOLE)
                    elif platform.system() == "Darwin":
                        os.system(r"""osascript -e 'tell application "Terminal" to do script "python3 \"%s\""'"""
                            % script_path)
        elif flow.request.url.startswith(api['app_3rd_auth']):
            # Record app's access token
            # Make sure we always use Bilibili app's token rather than
            # the temporary token we got from this api
            # otherwise myinfo api will fail with code=61000
            self.disposable_access_token = flow.request.urlencoded_form['access_token']
            print('access_token=' + self.disposable_access_token)
        elif flow.request.url in (
            api['biligame_l1_token_login_v3'],
            api['biligame_l1_token_oauth_login_v3'],
            api['biligame_l1_token_exchange_v3'],
            api['biligame_l3_token_login_v3'],
            api['biligame_l3_token_oauth_login_v3'],
            api['biligame_l3_token_exchange_v3']
            ):
            print('URL: ' + flow.request.url)
            resjson = flow.response.json()
            print('Original response:')
            print(resjson)
            if int(resjson['code']) == 500051:
                if not self.disposable_access_token:
                    self.disposable_access_token = flow.request.urlencoded_form['access_key']
                self.fill_user_info(resjson, self.disposable_access_token)
                print('Manipulated response:')
                print(resjson)
                flow.response.set_text(json.dumps(resjson))
                self.clear_token()

addons = [
    BilibiliBypass(),
]
