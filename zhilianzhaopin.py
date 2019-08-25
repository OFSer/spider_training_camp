import os
import csv
import requests
from lxml import html
from http import HTTPStatus

class ZhilianZhaopin:
    URL = "https://fe-api.zhaopin.com/c/i/sou"
    def __init__(self, url=URL):
        self.url = url
        self.web = requests.session()

    def get_resume_json(self):
        params = {
                'pageSize': 90,
                'cityId': 538,
                'salary': '0,0',
                'workExperience': -1,
                'education': -1,
                'companyType': -1,
                'employmentType': -1,
                'jobWelfareTag': -1,
                'kw': 'python',
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
            "cookie": "x-zp-client-id=95de5370-2651-477b-d4cf-9b0dbad8c7cf; dywec=95841923; sts_deviceid=16cc81873183f3-01c728dc733fc3-3e385b04-1327104-16cc81873195b3; sts_sg=1; sts_chnlsid=Unknown; zp_src_url=https%3A%2F%2Fcrossincode.com%2Fvip%2Fhomework%2F30%2F; sajssdk_2015_cross_new_user=1; __utmc=269921210; jobRiskWarning=true; sou_experiment=unexperiment; ZP_OLD_FLAG=false; CANCELALL=1; acw_tc=2760821715667267691841507efbed55865b7b8809ed88acb6252a74afde0e; LastCity=%E4%B8%8A%E6%B5%B7; LastCity%5Fid=538; dywea=95841923.3255782403685369300.1566725141.1566725141.1566728151.2; dywez=95841923.1566728151.2.2.dywecsr=baidu|dyweccn=(organic)|dywecmd=organic; __utma=269921210.1359516800.1566725141.1566725141.1566728151.2; __utmz=269921210.1566728151.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1566725141,1566725188,1566728151; adfbid=0; adfbid2=0; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216cc8187349403-0041ac70981f97-3e385b04-1327104-16cc818734a3e8%22%2C%22%24device_id%22%3A%2216cc8187349403-0041ac70981f97-3e385b04-1327104-16cc818734a3e8%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; urlfrom=121126445; urlfrom2=121126445; adfcid=none; adfcid2=none; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1566729230; ZL_REPORT_GLOBAL={%22sou%22:{%22actionid%22:%22db997143-e7b3-495a-8050-2981de1fae31-sou%22%2C%22funczone%22:%22smart_matching%22}%2C%22jobs%22:{%22recommandActionidShare%22:%22ba5dcea8-f7ee-4cf5-9b80-fbe658c92247-job%22%2C%22funczoneShare%22:%22dtl_best_for_you%22}}; sts_sid=16cc88891d065-01ab358d9e300b-3e385b04-1327104-16cc88891d15d4; sts_evtseq=2",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
                }
        req = job_web.get("{}".format(url), headers=headers)
        assert req.status_code == HTTPStatus.OK
        tree = html.fromstring(req.text)
        info_list = tree.xpath('//div[@class="describtion"]/div/p/span/text()')
        info = ' '.join(info_list)
        return info

    def get_job_info(self):
        rows = []
        data = self.get_resume_json()
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
            
    def save_csv(self):
        headers = ["招聘公司","招聘职位","薪资","学历要求","职位详细页面url","职位详细内容"]
        rows = self.get_job_info()
        os.makedirs('./zhaopin/', exist_ok=True)
        with open("./zhaopin/zhaopin.csv", "w") as f:
            f_csv = csv.writer(f)
            f_csv.writerow(headers)
            f_csv.writerows(rows)

    def run(self):
        print ("开始获取python招聘岗位信息...")
        self.save_csv()
        print ("信息获取完成。")

if __name__ == "__main__":
    zhaopininfo = ZhilianZhaopin()
    zhaopininfo.run()
