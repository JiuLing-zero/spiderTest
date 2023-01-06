import requests
from lxml import etree
import time
import re
import csv
import random

def save_data(data_msg):
    with open('zhushou360_data_two.csv', 'a', encoding='utf8', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerow(data_msg)
        fp.close()


#爬取应用汇网站的信息
if __name__ == "__main__":
    title = ['应用名', '分类', '应用简介']
    save_data(title)
    # 获取每个分类的url列表
    page_url="http://zhushou.360.cn/list/index/cid/1/"
    headers = {
        'referer': 'https://zhushou.360.cn/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 Edg/79.0.309.71',
    }
    # 获取网页源代码
    response = requests.get(page_url, headers=headers)
    text = response.content.decode('utf8')
    # 获取每个分类的url列表
    # 第一个获取的元素需要额外处理一下
    num = re.findall(r'<a href="/list/index/cid/(.*?)/"  >',text)
    num[0] = num[0].split("/")[-1]
    # ['11', '12', '14', '15', '16', '18', '17', '102228', '102230', '102231', '102232', '102139', '102233']
    urls = []
    for n in num:
        urls.append("http://zhushou.360.cn/list/index/cid/{}".format(n))
    # 循环每个软件的分类
    for category_url in urls:
        headers = {
            'referer': 'https://zhushou.360.cn/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 Edg/79.0.309.71',
        }
        # 获取网页源代码
        response = requests.get(category_url, headers=headers)
        text = response.content.decode('utf8')
        # 获取当前的分类名
        category = re.findall(r'class="aurr" >(.*?)</a>',text)[0]
        # 得到当前分类的最大页码值
        try:
            page_lastNum = re.findall(r'pg.pageCount = (.*?);',text)[0].split(".")[0]
        except:
            page_lastNum = ''
            print("读取页码失败，当前url为:"+category_url)
            continue
        # 得到所有页码的url值
        pages = []
        for i in range(1,int(page_lastNum)+1):
            pages.append(category_url+"/?page={}".format(i))
        # 获取 每个分类 所有页的数据
        for page in pages:
            try:
                response = requests.get(page, headers=headers)
                text = response.content.decode('utf8')
                # 得到每页所有应用的url
                html = etree.HTML(text)
                apps = html.xpath("//h3/a/@href")# ps:/detail/index/soft_id/77208
                apps_url = []
                for app in apps:
                    apps_url.append("https://zhushou.360.cn"+app)
                # 获取每个应用的信息
                for app_url in apps_url:
                    response = requests.get(app_url, headers=headers)
                    app_text = response.content.decode('utf8')
                    # 打印当前应用的分类
                    print("分类名:" + category)
                    # 应用名
                    try:
                        app_name = re.findall(r"'sname': '(.*?)',", app_text)[0]
                    except:
                        app_name = ''
                    print("应用名:"+app_name)
                    # 简介
                    try:
                        # re.S:单行模式,能将多行中匹配的结果当成一个结果
                        message = re.findall(r'<div class="breif">(.*?)<div', app_text, re.S)[0].replace("<br/>","").strip().replace(' ', '').replace('\n', '').replace('\r', '')
                    except:
                        message = ''
                    print("应用简介:"+message)

                    data_msg = []
                    data_msg.append(app_name)
                    data_msg.append(category)
                    data_msg.append(message)
                    save_data(data_msg)
                    print('*' * 50)

                    # 每个应用获取完信息暂停一会
                    time.sleep(random.randint(5,10)/10.0)
            except Exception as e:
                print(e)
            # 每一页暂停一会
            time.sleep(random.randint(5,10)/10.0)
        # 一个软件分类暂停一会
        time.sleep(random.randint(5,10)/10.0)
