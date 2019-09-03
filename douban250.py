import os
import csv
import json
import requests
from http import HTTPStatus

class Doubanfilm:
    DEFAULT_URL = "https://api.douban.com"
    DEFAULT_KEY = "0df993c66c0c636e29ecbb5344252a4a"

    def __init__(self, url=DEFAULT_URL, key=DEFAULT_KEY):
        self.url = url
        self.key = key
        self.web = requests.session()

    def get_sxk_poster_data(self):
        params = {'apikey': self.key}
        r = self.web.get("{}/v2/movie/1292052".format(self.url), params=params)
        assert r.status_code == HTTPStatus.OK
        data = r.json()
        return data["image"]

    def download_sxk_poster(self):
        poster_url = self.get_sxk_poster_data()
        poster_data = self.web.get(poster_url)
        os.makedirs('./poster/', exist_ok=True)
        with open("./poster/xsk_poster.jpg", 'wb') as f:
            f.write(poster_data.content)

    def get_douban_top_data(self):
        rows = []
        for page in range(0, 250, 20):
            params = {
                        'start': page,
                        'apikey': self.key
                     }
            r = self.web.get("{}/v2/movie/top250".format(self.url), params=params)
            assert r.status_code == HTTPStatus.OK
            movie_data = r.json()
            movie_info = movie_data['subjects']
            for i in range(len(movie_info)):
                tmp_dict = {}
                tmp_list = []
                tmp_dict["名称"] = movie_info[i]['title']
                tmp_dict["类型"] = ','.join(movie_info[i]['genres'])
                for j in range(len(movie_info[i]['casts'])):
                    tmp_list.append(movie_info[i]['casts'][j]['name'])
                names = ','.join(tmp_list)
                tmp_dict["主演"] = names
                tmp_dict["评分"] = movie_info[i]['rating']['average']
                rows.append(tmp_dict)
        return rows

    def csv(self):
        headers = ["名称", "类型", "主演", "评分"]
        rows = self.get_douban_top_data()
        with open("./poster/poster.csv", "w") as f:
            f_csv = csv.DictWriter(f, headers)
            f_csv.writeheader()
            f_csv.writerows(rows)

    def run(self):
        print ("开始下载肖申克的救赎海报...")
        self.download_sxk_poster()
        print ("海报下载完成。")
        print ("开始获取豆瓣电影250保存到本地...")
        self.csv()
        print ("保存完成，请查看csv文件。")

if __name__ == "__main__":
    film = Doubanfilm()
    film.run()

