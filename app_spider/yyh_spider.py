import requests
from lxml import etree
import time
import re
import csv
import json
from multiprocessing import Pool,Lock

# -*-coding:utf-8-*-

import urllib.request
import random


my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 Edg/79.0.309.71"
    ]


def save_data(data_msg):
    with open('yyh_all_url.csv', 'a', encoding='utf8', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerow(data_msg)
        fp.close()


# def save_false(data_msg):
#     with open('yyh_url_false.csv', 'a', encoding='utf8', newline='') as fp:
#         writer = csv.writer(fp)
#         writer.writerow(data_msg)
#         fp.close()


# lock = Lock()


# 爬取每一页
# def get_page_detail(url_page):



#爬取应用汇网站的信息
if __name__ == "__main__":
    # title = ['应用名称', '应用包名', '一级分类', '二级分类', '应用简介', '应用介绍']
    title = ['应用名称', '应用包名', '分类', '应用简介', '详细介绍']
    # save_data(title)
    # 获取从1到3307页的url
    urls=[]
    for i in range(1,3308):
        urls.append(f'http://www.appchina.com/category/30/{str(i)}_1_1_3_0_0_0.html')

    for url_page in urls:
        # 页码
        page_num = url_page.split('/')[-1].split('_')[0]
        # 未读取到的页码
        # now_page = 2937
        # # 跳过前n-1页的以及第n页的前m-1个应用
        # if int(page_num) < now_page:
        #     continue

        # print(f"url:{url_page}")
        headers = {
            'referer': 'http://www.appchina.com',
            'user-agent': random.choice(my_headers)
        }
        try:
            # 获取网页源代码
            response = requests.get(url=url_page, headers=headers)
            time.sleep(10)
            while (response.status_code != 200):
                print(f"访问第{url_page.split('/')[-1].split('_')[0]}页未成功")
                print(f"url:{url_page}")
                time.sleep(180)
                response = requests.get(url=url_page, headers=headers)
            text = response.content.decode('utf8')
            # 设置访问间隔
            # time.sleep(0.5)
            html = etree.HTML(text)

            # 获取每个app的html列表
            apps = html.xpath('//li[@class="has-border app"]')
            flag = 0
            # 得到每个app的信息
            for app in apps:
                if(flag == 30):
                    break


                # # 未读取到的个数
                # now_num = 11
                # if page_num == str(now_page) and flag + 1 < now_num:
                #     flag = now_num - 1
                #     continue

                # 记录当前是第几个app(下标)
                print(f"第{page_num}页的第{flag + 1}个app")

                # # 应用名
                # try:
                #     app_name = app.xpath('//div[@class="app-info"]//a/text()')[flag]
                # except:
                #     app_name = ''
                #
                # # 简介
                # try:
                #     message = app.xpath('//div[@class="app-intro"]/span/text()')[flag]
                # except:
                #     message = ''

                # 得到当前app的url
                app_url = "http://www.appchina.com" + app.xpath('//div[@class="app-info"]//a/@href')[flag]
                print("app的url:" + app_url)
                flag += 1

                # 包名
                try:
                    package = app_url.split("/")[-1]
                except:
                    package = ''

                result = []
                result.append(app_url)
                result.append(package)
                save_data(result)

                # # 获取当前应用的详细信息
                # response = requests.get(url=app_url, headers=headers)
                # while(response.status_code != 200):
                #     print(f"访问:{app_url}未成功")
                #     # save_false(url_page+"/t"+app_url)
                #     # continue
                #     time.sleep(180)
                #     response = requests.get(url=app_url, headers=headers)
                # text = response.content.decode('utf8')
                # # 设置访问间隔
                # # time.sleep(2)
                # app_html = etree.HTML(text)
                #
                # # 分类类别
                # try:
                #     # category = app_html.xpath('//div[@class="main-right"]/div[1]//p[6]/text()')[0].split("：")[-1]
                #     category = re.findall('class="art-content">分类：(.*?)</p>', text ,re.S)[0]
                # except:
                #     category = ''
                #
                # # 详细介绍
                # try:
                #     details = app_html.xpath('//p[@class="art-content"]/text() | //p[@class="art-content"]/a/text()')
                #     # details = app_html.xpath('//div[@class="App_SpreadContent App_Introduce"]/span/text() | //div[@class="App_SpreadContent App_Introduce"]/span/a/text()')
                #     message_detail = ''
                #     for detail in details:
                #         message_detail = message_detail + detail
                # except:
                #     message_detail = ''
                #
                # # lock.acquire()
                #
                # print("应用名:" + app_name)
                # print("包名:" + package)
                # print("分类类别:" + category)
                # print("简介:" + message)
                # print("详细介绍:" + message_detail)
                # data = []
                # data.append(app_name)
                # data.append(package)
                # data.append(category)
                # data.append(message)
                # data.append(message_detail)
                # # 保存文件
                # save_data(data)
                # print('*' * 50)
                #
                # # lock.release()
                # # break # 每个app

        except Exception as e:
            print(e)



    # # 设置四个进程跑爬虫任务
    # pool = Pool(processes=4)
    # pool.map(get_page_detail, urls)
    # pool.close()

