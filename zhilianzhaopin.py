import os
import sys
import csv
import requests
from lxml import html
from http import HTTPStatus

class ZhilianZhaopin:
    URL = "https://fe-api.zhaopin.com/c/i/sou"
    def __init__(self, url=URL):
        self.url = url
        self.web = requests.session()

    def get_resume_json(self, keywords):
        params = {
                'pageSize': 90,
                'cityId': 538,
                'salary': '0,0',
                'workExperience': -1,
                'education': -1,
                'companyType': -1,
                'employmentType': -1,
                'jobWelfareTag': -1,
                'kw': keywords,
                'kt': 3,
                '_v': 0.35755599,
                'x-zp-page-request-id': 'ed2238becc2847f4aa9053d9e5871484-1566729229069-367303',
                'x-zp-client-id': '95de5370-2651-477b-d4cf-9b0dbad8c7cf'
                }

        r = self.web.get("{}".format(self.url), params=params)
        assert r.status_code == HTTPStatus.OK
        return r.json()

    def get_job_info(self, keywords):
        rows = []
        data = self.get_resume_json(keywords)
        job_info_list = data["data"]["results"]
        for n in range(len(job_info_list)):
            recruitment_company = job_info_list[n]["company"]["name"]
            recruitment_position = job_info_list[n]["jobName"]
            salary = job_info_list[n]["salary"]
            edu_level = job_info_list[n]["eduLevel"]["name"]
            detailed_page_url = job_info_list[n]["positionURL"]
            info_tuple = (
                    recruitment_company, recruitment_position, salary, edu_level,
                    detailed_page_url
                    )
            rows.append(info_tuple)
        return rows
            
    def save_csv(self, keywords):
        headers = ["招聘公司","招聘职位","薪资","学历要求","职位详细页面url"]
        rows = self.get_job_info(keywords)
        os.makedirs('./zhaopin/', exist_ok=True)
        with open("./zhaopin/{}_zhaopin.csv".format(keywords), "w", encoding="utf-8") as f: 
            f_csv = csv.writer(f)
            f_csv.writerow(headers)
            f_csv.writerows(rows)

    def run(self):
        while 1:
            keywords = input("请输入你要查询的关键字：")
            if keywords:
                print ("开始获取{}相关招聘岗位信息...".format(keywords))
                self.save_csv(keywords)
                print ("信息获取完成。")
                while 1:
                    yorn = input("是否想要继续查询(y/n)? ")
                    if yorn.lower() == "y" or yorn.lower() == "yes" or yorn == "":
                        break
                    elif yorn.lower() == "n" or yorn.lower() == "no":
                        print ("已退出查询。\n")
                        sys.exit(0)
                    else:
                        print ("你的输入无效，请重新输入...")
                        continue
            else:
                print("你的输入为空，请重新输入...")
                continue

if __name__ == "__main__":
    zhaopininfo = ZhilianZhaopin()
    zhaopininfo.run()
