import os
import csv
import requests
from http import HTTPStatus
from lxml import html

class LianjiaZufang:
    URL = "https://sh.lianjia.com/zufang/"

    def __init__(self, url=URL):
        self.url = url
        self.web = requests.session()

    def get_info(self, zone, price=""):
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
                }

        r = self.web.get("{}/{}/{}".format(self.url, zone, price), headers=headers)
        assert r.status_code == HTTPStatus.OK
        tree = html.fromstring(r.text)
        rows = []
        zufang_info_list  = tree.xpath('//div[@class="content__list--item"]/a/@title')
        zufang_imgs_list  = tree.xpath('//div[@class="content__list--item"]/a/img/@src')
        zufang_link_list  = tree.xpath('//div[@class="content__list--item"]/a/@href')
        zufang_zone_list  = tree.xpath('//div[@class="content__list--item"]//div//p/a[2]/text()')
        zufang_space_list = tree.xpath('//div[@class="content__list--item"]//div//p[2]/text()[5]')
        zufang_direction_list = tree.xpath('//div[@class="content__list--item"]//div//p[2]/text()[6]')
        zufang_hosttype_list  = tree.xpath('//div[@class="content__list--item"]//div//p[2]/text()[7]')
        num = len(zufang_info_list)
        for i in range(num):
            info_tuple = (zufang_info_list[i],zufang_imgs_list[i],"https://sh.lianjia.com{0}".format(zufang_link_list[i]),
                          zufang_zone_list[i],zufang_space_list[i],zufang_direction_list[i],
                          zufang_hosttype_list[i]
                         )
            rows.append(info_tuple)
        return rows

    def save_csv(self, zone, price):
        headers = ["信息","图片","链接","区域","面积","朝向","户型"]
        rows = self.get_info(zone, price)
        os.makedirs('./lianjia/', exist_ok=True)
        with open('./lianjia/lianjia.csv','w') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(headers)
            f_csv.writerows(rows)

    def run(self):
        zone = input("输入需要查询的区域拼音(松江:songjiang):")
        price = input("输入需要查询的价格区间(<=1000:rp1,1000-1500:rp2,1500-2000:rp3,2000-3000:rp4):\n")
        print ("开始获取链家查询信息...")
        self.save_csv(zone, price)
        print ("信息获取完成。")

if __name__ == "__main__":
    lianjiainfo = LianjiaZufang()
    lianjiainfo.run()

