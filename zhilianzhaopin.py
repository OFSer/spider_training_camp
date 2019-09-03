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

    def get_job_details_page(self, detailed_page_url):
        url = detailed_page_url
        job_web = requests.session()
        headers = {
            "cookie": "acw_tc=2760822a15674931644908161ed6c579e97432d934c6b7eaf17ee0a95306fe; x-zp-client-id=37717ded-b773-4768-90ae-67c16e763675; sts_deviceid=16cf5df9498a90-068abd41b66171-3b654406-2359296-16cf5df9499a00; sajssdk_2015_cross_new_user=1; sts_sg=1; sts_chnlsid=Unknown; zp_src_url=https%3A%2F%2Fjobs.zhaopin.com%2FCC000636993J00233315504.htm; jobRiskWarning=true; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216cf5df956e1b1-00ec3edfe9766b-3b654406-2359296-16cf5df956f983%22%2C%22%24device_id%22%3A%2216cf5df956e1b1-00ec3edfe9766b-3b654406-2359296-16cf5df956f983%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24latest_referrer_host%22%3A%22www.google.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; dywec=95841923; urlfrom=121114584; urlfrom2=121114584; adfcid=www.google.com; adfcid2=www.google.com; adfbid=0; adfbid2=0; __utmc=269921210; sou_experiment=psapi; LastCity=%E4%B8%8A%E6%B5%B7; LastCity%5Fid=538; ZP_OLD_FLAG=false; CANCELALL=0; dywea=95841923.1071362239820432300.1567494674.1567494674.1567499845.2; dywez=95841923.1567499845.2.2.dywecsr=google.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/; dyweb=95841923.1.10.1567499845; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1567494674,1567499845; sts_sid=16cf6457d30aef-090166fc059649-3b654406-2359296-16cf6457d31a1f; __utma=269921210.2042484508.1567494675.1567494675.1567499846.2; __utmz=269921210.1567499846.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; __utmb=269921210.1.10.1567499846; acw_sc__v2=5d6e264a6d038823d74d556af87e43ff62d1882c; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1567500126; ZL_REPORT_GLOBAL={%22jobs%22:{%22recommandActionidShare%22:%2207cc5a3c-3167-4475-9bea-a98ef3e3570f-job%22%2C%22funczoneShare%22:%22dtl_best_for_you%22}%2C%22sou%22:{%22actionid%22:%226fe85488-bf5e-44c6-b4b8-dbb04a9b6aa3-sou%22%2C%22funczone%22:%22smart_matching%22}}; sts_evtseq=24",

            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
                }
        req = job_web.get("{}".format(url), headers=headers)
        assert req.status_code == HTTPStatus.OK
        tree = html.fromstring(req.text)
        info_list = tree.xpath('//div[@class="describtion"]/div/p/span/text()')
        info = ' '.join(info_list)
        return info

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
            detailed_page_content = self.get_job_details_page(detailed_page_url)
            info_tuple = (
                    recruitment_company, recruitment_position, salary, edu_level,
                    detailed_page_url, detailed_page_content
                    )
            rows.append(info_tuple)
        return rows
            
    def save_csv(self, keywords):
        headers = ["招聘公司","招聘职位","薪资","学历要求","职位详细页面url","职位详细内容"]
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
