from os import access


appkey = '1d8b6e7d45233436'
appSecret = '560c52ccd288fed045859ed18bffd973'
login_appkey = 'bca7e84c2d947ac6'
login_appSecrect = '60698ba2f68e01ce44738920a0ffe768'
api = {
    'getkey' : 'http://passport.bilibili.com/api/oauth2/getKey',
    'login' : 'https://passport.bilibili.com/api/v3/oauth2/login',
    'verify_sms' : 'https://api.bilibili.com/x/safecenter/tel/verify',
    'myinfo' : 'https://app.bilibili.com/x/v2/account/myinfo',
    'access_token' : 'https://passport.bilibili.com/api/v2/oauth2/access_token',
    'app_3rd_auth' : 'https://passport.bilibili.com/api/oauth2/authorizeByApp',
    'biligame_l1_login': 'https://line1-sdk-center-login-sh.biligame.net/api/client/login',
    'biligame_l1_login_v3' : 'https://line1-sdk-center-login-sh.biligame.net/api/external/login/v3',
    'biligame_l1_session_renew' : 'https://line1-sdk-center-login-sh.biligame.net/api/client/session.renew',
    'biligame_l1_user_info' : 'https://line1-sdk-center-login-sh.biligame.net/api/client/user.info',
    'biligame_l1_token_login_v3' : 'https://line1-sdk-center-login-sh.biligame.net/api/external/user.token.oauth.login/v3',
    'biligame_l1_token_oauth_login_v3' : 'https://line1-sdk-center-login-sh.biligame.net/api/external/user.token.oauth.login/v3',
    'biligame_l1_token_exchange_v3' : 'https://line1-sdk-center-login-sh.biligame.net/api/external/token.exchange/v3',
    'biligame_l3_login_v3' : 'https://line3-sdk-center-login-sh.biligame.net/api/external/login/v3',
    'biligame_l3_token_login_v3' : 'https://line3-sdk-center-login-sh.biligame.net/api/external/user.token.oauth.login/v3',
    'biligame_l3_token_oauth_login_v3' : 'https://line3-sdk-center-login-sh.biligame.net/api/external/user.token.oauth.login/v3',
    'biligame_l3_token_exchange_v3' : 'https://line3-sdk-center-login-sh.biligame.net/api/external/token.exchange/v3',
}
minor_guard_blacklist = [
    'line1-realtime-api.biligame.net',
    'line3-realtime-api.biligame.net',
]
headers = {
    'user-agent': 'Mozilla/5.0 BiliDroid/6.41.0 (bbcallen@gmail.com)'
}
basic_query_params = {
    'appkey' : appkey,
    'build' : 6410400,
    'device': 'android',
    'mobi_app' : 'android',
    'platform' : 'android',
    's_locale' : 'zh_CN',
}
basic_login_params = {
    'appkey' : login_appkey,
    'actionKey' : 'appkey',
    'build' : 6410400,
    'device': 'android',
    'mobi_app' : 'android',
    'platform' : 'android',
    's_locale' : 'zh_CN',
}
access_token_file = 'access_token'
