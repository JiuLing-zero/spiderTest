# -*- coding: utf-8 -*-

from common import basic_func
import requests
import re
from bs4 import BeautifulSoup

page_scroll_max = 1000  # 翻页个数
write_file = open('/Users/miayangs/Downloads/spider_wdj_app.txt', 'w')

addr = 'http://www.wandoujia.com/category/app'  # 目标网址首页
soup = basic_func.getbs(addr)
app_cate1_addr = soup.findAll('a', 'cate-link')
# app_cate1_addr = app_cate1_addr[0:1]
for cate in app_cate1_addr:  # 各一级类目
    cate1 = cate.get_text()
    addr = cate.get('href')
    cate1_id = re.findall('https://www.wandoujia.com/category/([0-9]+)', addr, re.S)[0]
    # print(cate1 + '\t' + addr + '\t' + cate1_id)
    soup = basic_func.getbs(addr)
    app_cate2_addr_par = soup.find('ul', 'switch-tab cate-tab')
    app_cate2_addr = app_cate2_addr_par.findAll('a', href=re.compile('^https://www.wandoujia.com/category/.*_'))
    # app_cate2_addr = app_cate2_addr[0:1]
    for cate in app_cate2_addr:  # 各二级类目
        cate2 = cate.get_text()
        addr = cate.get('href')
        cate2_id = re.findall('https://www.wandoujia.com/category/[0-9]+_([0-9]+)', addr, re.S)[0]
        print(cate1 + '\t' + cate2 + '\t' + addr)
        for page_num in range(1, page_scroll_max):  # 每一页
            addr = 'https://www.wandoujia.com/wdjweb/api/category/more?catId={}&subCatId={}&page={}'.format(cate1_id, cate2_id, page_num)
            # print(addr)
            page = requests.get(addr).json()
            data = page['data']['content']
            if len(data) == 0:
                print('max page is: ' + str(page_num))
                break
            soup = BeautifulSoup(data, 'html.parser')
            app_name_par = soup.findAll('h2', 'app-title-h2')
            for app in app_name_par:  # 各app名称
                app_name_addr = app.find('a', href=re.compile('^https://www.wandoujia.com/apps/'))
                app_name = app_name_addr.get_text()
                # print(app_name)
                write_file.write(cate1 + '\t' + cate2 + '\t' + app_name + '\n')

write_file.close()
