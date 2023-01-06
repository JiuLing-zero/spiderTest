import random
import re
import time

import requests
from bs4 import BeautifulSoup
# 需求:爬取西游记 各章节的标题 和 各章内容
if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Mobile Safari/537.36'
    }
    url = 'https://xiyouji.5000yan.com/'
    # 获取页面源码
    page_text = requests.get(url=url,headers=headers).content.decode('utf-8')
    # 在首页中解析出章节的标题和详情页的url
    # 1、实例化BeautifulSoup对象，需要将页面源码数据加载到该对象中
    soup = BeautifulSoup(page_text,'lxml')
    # 解析章节标题和详情页的url
    li_list = soup.select('.sidamingzhu-list-mulu > ul > li')
    # 定义西游记文件的文件流
    fp = open('./西游记.txt','w',encoding='utf-8')
    for li in li_list:
        #章节标题
        title = li.a.string
        # 详情页的url
        detail_url = li.a['href']
        # 对详情页发起请求，解析出章节内容
        detail_page = requests.get(url=detail_url,headers=headers).content.decode('utf-8')
        # 解析出详情页中的相关内容
        detail_soup = BeautifulSoup(detail_page,'lxml')
        # 定位到保存正文内容的div标签
        div_tag = detail_soup.find('div',class_='grap')
        # 获取所有正文内容(处理缩进、空格、换行)
        content = div_tag.text.strip().replace(' ', '').replace('\r', '')
        content = re.sub('\n+','\n',content)
        # 持久化到文件中
        fp.write("=="*20+'\n'+title+'\n'+"=="*20+'\n'+content+'\n')
        # 爬取一章后延迟一段时间
        time.sleep(random.randint(5, 10)/10.0 + 1)
