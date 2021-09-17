import json
import mitmproxy.http
import random

target_url = 'https://as.hypergryph.com/online/v1/ping'

class HypergryphBypass:
    def response(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.url == target_url:
            print('URL: ' + flow.request.url)
            resjson = flow.response.json()
            print('Original response:')
            print(resjson)
            if resjson['result'] in [2, 3]:
                resjson = {
                    'result' : 0,
                    'message' : 'OK',
                    'interval' : random.randint(1800, 3600),
                    'timeLeft' : -1,
                    'alertTime' : 600,
                }
                print('Manipulated response:')
                print(resjson)
                flow.response.set_text(json.dumps(resjson))

addons = [
    HypergryphBypass()
]
