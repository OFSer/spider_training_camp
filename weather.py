import sys
import json
import requests
from http import HTTPStatus


class Weather:
    DEFAULT_KEY = "bb18bc76597a48e5ac978ea7aac9448b"
    DEFAULT_URL = "https://free-api.heweather.com"

    def __init__(self, url=DEFAULT_URL, key=DEFAULT_KEY):
        self.url = url
        self.key = key
        self.web = requests.session()

    def get_weather(self, wtype, location):
        value = {
                 'location': location,
                 'key': self.key
                }
        r = self.web.get("{}/s6/weather/{}".format(self.url, wtype), params=value)
        assert r.status_code == HTTPStatus.OK
        return r.json()

    def now_weather(self, wtype, location):
        data = self.get_weather(wtype, location)
        info = data['HeWeather6'][0]
        print ("当前城市：{}".format(info['basic']['location']))
        print ("当前时间：{}".format(info['update']['loc']))
        print ("天气状况：{}".format(info['now']['cond_txt']))
        print ("体感温度：{}℃".format(info['now']['fl']))
        print ("室外温度：{}℃".format(info['now']['tmp']))
        print ("相对湿度：{}".format(info['now']['hum']))
        print ("大气压强：{}".format(info['now']['pres']))
        print ("风向:{}".format(info['now']['wind_dir']))
        print ("风力:{}级".format(info['now']['wind_sc']))
        print ("风速:{}公里/小时".format(info['now']['wind_spd']))
        print ("降水量:{}".format(info['now']['pcpn']))
        print ("能见度:{}公里\n".format(info['now']['vis']))

    def lifestyle_weather(self, wtype, location):
        data = self.get_weather(wtype, location)
        info = data['HeWeather6'][0]
        print ("当前城市：{}".format(info['basic']['location']))
        print ("当前时间：{}".format(info['update']['loc']))
        for i in range(6):
            tmp = info['lifestyle'][i]
            if tmp['type'] == "comf":
                print ("舒适指数：{}，{}".format(tmp['brf'], tmp['txt']))
            elif tmp['type'] == "drsg":
                print ("穿衣指数：{}，{}".format(tmp['brf'], tmp['txt']))
            elif tmp['type'] == "flu":
                print ("感冒指数：{}，{}".format(tmp['brf'], tmp['txt']))
            elif tmp['type'] == "sport":
                print ("运动指数：{}，{}".format(tmp['brf'], tmp['txt']))
            elif tmp['type'] == "trav":
                print ("旅游指数：{}，{}".format(tmp['brf'], tmp['txt']))
            elif tmp['type'] == "cw":
                print ("洗车指数：{}，{}\n".format(tmp['brf'], tmp['txt']))
            
    def forecast_weather(self, wtype, location):
        data = self.get_weather(wtype, location)
        info = data['HeWeather6'][0]['daily_forecast']
        for i in range(1,3):
            print ("预报日期:{}".format(info[i]['date']))
            print ("日出时间:{}".format(info[i]['sr']))
            print ("日落时间:{}".format(info[i]['ss']))
            print ("月升时间:{}".format(info[i]['mr']))
            print ("月落时间:{}".format(info[i]['ms']))
            print ("最高温度:{}".format(info[i]['tmp_max']))
            print ("最低温度:{}".format(info[i]['tmp_min']))
            print ("白天天气状况:{}".format(info[i]['cond_txt_d']))
            print ("夜晚天气状况:{}".format(info[i]['cond_txt_n']))
            print ("风向:{}".format(info[i]['wind_dir']))
            print ("风力:{}".format(info[i]['wind_sc']))
            print ("风速:{}公里/小时".format(info[i]['wind_spd']))
            print ("相对湿度:{}".format(info[i]['hum']))
            print ("降水量:{}".format(info[i]['pcpn']))
            print ("降水概率:{}".format(info[i]['pop']))
            print ("大气压强:{}".format(info[i]['pres']))
            print ("紫外线强度:{}".format(info[i]['uv_index']))
            print ("能见度:{}公里\n".format(info[i]['vis']))

    def run(self):
        select = {
                  1: "now",
                  2: "lifestyle",
                  3: "forecast"
                 }
        while 1:
            inquire = input("请输入你想查询的城市(汉字/拼音):")
            print ("""
                   1. 当前天气状况
                   2. 当前生活指数
                   3. 未来两天天气预报
                   """)
            s = int(input("请选择你要查询的类型:"))
            if select[s] == 'now':
                self.now_weather(select[s], inquire)
            elif select[s] == 'forecast':
                self.forecast_weather(select[s], inquire)
            elif select[s] == 'lifestyle':
                self.lifestyle_weather(select[s], inquire)
            continue_query = input("你是否想要继续查询?(Y/N) ")
            if continue_query.lower() == "y":
                continue
            else:
                print ("已退出，欢迎再次使用！")
                sys.exit(0)


if __name__ == "__main__":
    wea = Weather()
    wea.run()
    

