import os
import requests
from http import HTTPStatus

class Weibohtml:
    DEFAULT_URL = "https://weibo.com/a/hot/realtime"

    def __init__(self, url=DEFAULT_URL):
        self.url = url
        self.web = requests.session()

    def get_weibotext(self):
        headers = {
                    "Cookie": "SINAGLOBAL=3033718095538.691.1554104481183; UM_distinctid=16aa6680ee5753-0e1eafc1a73b96-3b654406-240000-16aa6680ee698f; UOR=,,www.techug.com; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W51r5kx00Bg8YqjFvroR_rC; SUB=_2AkMqCrJCf8NxqwJRmP4QzW3qboRyyAzEieKcVkOZJRMxHRl-yj83qkEItRB6AYqcrJzt4iIO007TH_wtDrhrRmmbd3Bg; YF-Page-G0=237c624133c0bee3e8a0a5d9466b74eb|1566637651|1566637651; _s_tentry=-; Apache=7850686035890.044.1566637651929; ULV=1566637651946:9:2:1:7850686035890.044.1566637651929:1565932703868; Ugrow-G0=589da022062e21d675f389ce54f2eae7; YF-V5-G0=d30fd7265234f674761ebc75febc3a9f; WBStorage=f54cf4e4362237da|undefined; login_sid_t=5242f9c283f6d73e429067b1fce13e3b; cross_origin_proto=SSL; wb_view_log=2048*11521.25",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
                    }
        r = self.web.get("{}".format(self.url), headers=headers)
        assert r.status_code == HTTPStatus.OK
        return r.text

    def download_html(self):
        weibo_html = self.get_weibotext()
        os.makedirs('./weibo/', exist_ok=True)
        with open("./weibo/weibohot.html", 'w') as f:
            f.write(weibo_html)

    def run(self):
        print ("开始下载微博热点页面...")
        self.download_html()
        print ("页面下载完成。")

if __name__ == "__main__":
    html = Weibohtml()
    html.run()
