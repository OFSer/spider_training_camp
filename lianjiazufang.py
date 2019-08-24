import os
import csv
import requests
from http from HTTPStatus
from lxml from html

class LianjiaZufang:
    URL = "https://sh.lianjia.com/zufang/"

    def __init__(self):
        self.url = url
        self.web = requests.session()

    def get_info(self, types):
        headers = {
                'Cookie': 'lianjia_ssid=63f199e2-5a51-4650-8d9c-b696ef59707a; lianjia_uuid=6092a227-b7c3-40b7-93f6-fbea48a6993c; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiZTVlYTk2MDliOGUwZDQ4Yjc2ZWUzNzE4ZWFiM2ZjMDY0ZGFlZGE3ZWFiN2YxODllZGJlMGQ4OGU3YTQzN2M1YTIwMTJlZjZiNDY1MmZlMzgzMmE2NGZiZTU0ZjBjMTJmNjU5MmQzYTQ4YjdkZTZmMDBkNjA2ZDUwYjdiNmVlMWQ2NjEyZmI3NDE2YWNmYTE5ZDViMjUxNjI5YWI4ZGVlMjk1OGViODdhMTUxYzMyZjEzYmU0NDYwOTgyNzFlN2E5NDYyYTM5NDhlMDZkMTUyMDBkNmU2ZGYzMjZmZmYwMTY5MTBjOWZmMmY4NDAxYzBjYzdlMjA3MjljODhkOGQ0ZTIzMzlmYzRhYjk3ZjFjYmI0NjI3YjdkYzNiYmI3OWUyN2Q1ZmE3N2Q2MjA5ZjUxZDE5NDBiMzMyNzhmZGQwYjRcIixcImtleV9pZFwiOlwiMVwiLFwic2lnblwiOlwiNmExZDBlOGJcIn0iLCJyIjoiaHR0cHM6Ly9zaC5saWFuamlhLmNvbS96dWZhbmcvIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0=',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
                }

        r = self.web.get("{}/{}".format(self.url, types), headers=headers)

