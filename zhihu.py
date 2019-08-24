import os
import csv
import requests
from http import HTTPStatus 

class ZhihuRecommend:
    URL = "https://www.zhihu.com/api/v3/feed/topstory/recommend"

    def __init__(self, url=URL):
        self.url = url
        self.web = requests.session()

    def get_page_data(self):
        headers = {
                'cookie': '_zap=43eaded6-a732-4ee7-85b4-c7ac8c2614c5; d_c0="ABDnkMYHMQ-PTui_mptmfL3t4WcTSx9KIug=|1553768410"; _xsrf=Zgy0cAoMKmR8LXorsOrwWH9688apvRiV; z_c0="2|1:0|10:1554286165|4:z_c0|92:Mi4xOGdxRUFnQUFBQUFBRU9lUXhnY3hEeVlBQUFCZ0FsVk5WZFNSWFFBMTBWX1F5Q1gyUHl5dF9KM0J2Z0Vhc01udzdR|3e8f2f8fa63645be91387e6b259b8dfdc6dd278f9c99a010b500b2c860a1e49b"; q_c1=77ff3c79cc414cd6980fc4df6367c896|1563535619000|1556448479000; tst=r; __utma=51854390.1825543909.1565075465.1565075465.1565075465.1; __utmz=51854390.1565075465.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/napoleon-lee/collections; __utmv=51854390.100-1|2=registration_date=20160124=1^3=entry_date=20160124=1; tgw_l7_route=66cb11',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
                }
        params = {
                'session_token': 'b3b8777f76c7d1d0e2717ddca35d9aae',
                'desktop': 'true',
                'page_number': 2,
                'limit': 6,
                'action': 'down',
                'after_id': 5
                }
        r = self.web.get("{}".format(self.url), headers=headers, params=params)
        return r.json()

    def save_csv(self):
        rows = []
        headers = ["id","type","offset","verb","created_time","updated_time","target","brief","uninterest_reasons",
                "attached_info","actors","show_actor_time","action_text","action_text_tpl","action_card"]
        data = self.get_page_data()
        for i in range(len(data['data'])):
            rows.append(data['data'][i])
        os.makedirs('./zhihu/', exist_ok=True)
        with open("./zhihu/zhihu.csv", "w") as f:
            f_csv = csv.DictWriter(f, headers)
            f_csv.writeheader()
            f_csv.writerows(rows)

    def run(self):
        print ("开始获取知乎时间线内容...")
        self.save_csv()
        print ("获取完成。")


if __name__ == "__main__":
    zhihu = ZhihuRecommend()
    zhihu.run()
