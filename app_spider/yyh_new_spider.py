import csv
import json
import random
import time
from multiprocessing import Pool,Lock
import requests
from lxml import etree


my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 Edg/79.0.309.71"
    ]


# 追加保存数据到文件里
def save_data(data_msg):
    with open('yyh_data.csv', 'a', encoding='utf8', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerow(data_msg)
        fp.close()


# 获取Ajax局部刷新的json数据
def get_ajax_json(url, ajax_headers):
    response = session.get(url=url, headers=ajax_headers)
    # 设置访问间隔
    time.sleep(random.randint(1, 3) / 10.0)
    return response.json()


session = requests.Session()
lock = Lock()


# 获取当前分类的所有app数据
def get_category_data(category_url):
    headers = {
        'User-Agent': random.choice(my_headers)
    }
    # 从第一页开始
    page_num = 1

    # if(category_url.split("/")[-1] == "303"):
    #     page_num = 27

    now_url = category_url + "/" + page_num.__str__()
    # 获取第一页的json内容
    list_data = get_ajax_json(now_url, headers)
    # nextPage为空时当前分类到达最后一页
    while (list_data["nextPage"] != None):

        # 获取得到的json数据的长度
        app_len = list_data['list'].__len__()
        # 对每个app进行数据获取
        for i in range(app_len):
            # 包名
            package = list_data['list'][i]['packageName']
            # app名
            app_name = list_data['list'][i]['name']
            # 根据包名得到当前app的url
            app_url = 'http://m.appchina.com/app/' + package

            response = session.get(url=app_url, headers=headers)

            while (response.status_code != 200):
                print(f"访问:{app_url}未成功")
                response = session.get(url=app_url, headers=headers)

            text = response.content.decode('utf8')
            html = etree.HTML(text)

            # 设置访问间隔
            time.sleep(random.randint(1, 3) / 10.0)

            # 分类名称
            try:
                category = html.xpath('//div[@class="breadcrumb"]/a[2]/text()')[0]
            except:
                category = ''
            # 简介
            try:
                message = html.xpath('//div[@class="app-details-appdes"]/h3/text()')[0]
            except:
                message = ''
            # 详细介绍
            try:
                details = html.xpath(
                    '//div[@class="App_SpreadContent App_Introduce"]/span/text() | //div[@class="App_SpreadContent App_Introduce"]/span/a/text()')
                message_detail = ''
                for detail in details:
                    message_detail = message_detail + detail
            except:
                message_detail = ''

            lock.acquire()

            print("应用名:" + app_name)
            print("包名:" + package)
            print("分类类别:" + category)
            print("简介:" + message)
            print("详细介绍:" + message_detail)
            data = []
            data.append(app_name)
            data.append(package)
            data.append(category)
            data.append(message)
            data.append(message_detail)
            save_data(data)
            print('*' * 50)

            lock.release()
            # break # 当前页的每一个app

        page_num += 1
        # 获取下一页的json数据
        now_url = category_url + "/" + page_num.__str__()
        list_data = get_ajax_json(now_url, headers)
        print("开始爬取第" + page_num.__str__() + "页的数据")

        # break # 遍历每一页的数据

    print("当前分类已爬取完毕")


# 爬取应用汇新网站的ajax信息
if __name__ == '__main__':
    title = ['应用名称', '应用包名', '分类', '应用简介', '详细介绍']
    save_data(title)
    # 发起ajax请求的公共url部分
    url_public = 'http://m.appchina.com/ajax/cat/'
    # 获取所有分类的url列表,序号301-314
    urls = []
    for i in range(301, 315):
        urls.append(url_public + i.__str__())

    # 设置三个进程跑爬虫任务
    pool = Pool(processes=4)
    pool.map(get_category_data, urls)
    pool.close()

