import requests
from lxml import etree
import time
import re
import csv
import json
# from selenium import webdriver
# from selenium.webdriver import Chrome
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.common.action_chains import ActionChains
#
#
# options = webdriver.ChromeOptions()
# options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
# browser = webdriver.Chrome()
# wait = WebDriverWait(browser,20)
#
#
# # 破解验证
# def break_validation(url):
#     browser.get(url)
#     browser.maximize_window()
#     time.sleep(2)
#     distance = 300
    # try:
    #     slider = wait.until(EC.presence_of_element_located((By.ID, 'nc_1_n1z')))  # 找到滑块
    #     if slider:
    #         print("====有滑块验证=====")
    #         action_chains = webdriver.ActionChains(browser)
    #         # 点击，准备拖拽
    #         action_chains.click_and_hold(slider)
    #         action_chains.pause(0.2)
    #         for i in range(distance/10):
    #             action_chains.move_by_offset(10, 0)
    #             action_chains.pause(0.2)
    #         # action_chains.pause(0.2)
    #         #
    #         # action_chains.move_by_offset(distance / 2, 0)
    #         action_chains.release()
    #         action_chains.perform()  # 释放滑块
    #     else:
    #         print("===没有滑块验证===")
    # except Exception as e:
    #     print("===" + str(e))


def save_data(data_msg):
    with open('wdj_all_url.csv', 'a', encoding='utf8', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerow(data_msg)
        fp.close()


if __name__ == "__main__":
    # title = ['应用名称', '应用包名', '一级分类', '二级分类', '应用简介', '应用介绍']
    title = ['应用名称', '应用包名', '分类', '应用简介']
    # save_data(title)
    # 目标网站
    page_url = 'https://www.wandoujia.com/category/app'
    headers = {
        'referer': 'https://www.wandoujia.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 Edg/79.0.309.71',
    }
    # 获取网页源代码
    response = requests.get(page_url, headers=headers)
    text = response.content.decode('utf8')
    # 将爬取的网页数据再生成标准网页格式数据
    html = etree.HTML(text)
    # 获取每个分类的url列表
    urls = html.xpath("//li[@class='parent-cate']/div/a/@href")
    for category_url in urls:
        id = re.findall(r'category/(\w+)_(\w+)', category_url, re.S)
        # 一级分类的数字
        catId = id[0][0]
        # 二级分类的数字
        subCatId = id[0][1]
        base_url = 'https://www.wandoujia.com/wdjweb/api/category/more?catId={}&subCatId={}&page={}&ctoken=ybV4FcepvlzuaEP4kXEBBWzd'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 Edg/79.0.309.71',
        }
        #获取全部页的数据
        for i in range(1, 10000):
            # 第i页的url
            url = base_url.format(catId, subCatId, i)
            try:
                # 获取源代码
                response = requests.get(url, headers=headers)# proxies={"HTTPS":"60.173.35.198:8499"}
                text = response.content.decode('utf8')
                json_data = json.loads(text)
                msg = json_data['data']['content']
                # 判断当前url是否遍历完毕
                if len(msg) == 0:
                    print('max page is: ' + str(i))
                    break
                test_html = etree.HTML(msg)
                lis = test_html.xpath("//li")
                for li in lis:
                    li = etree.tostring(li, encoding='utf8').decode()
                    # 应用包名
                    # try:
                    #     package_name = re.findall(r'data-pn="(.*?)"', li)[0]
                    # except:
                    #     package_name = ''

                    package_name = re.findall(r'data-pn="(.*?)"', li)[0]
                    url = re.findall(r'href="(.*?)"', li, re.S)[0]

                    result = []
                    result.append(package_name)
                    result.append(url)
                    save_data(result)


                    # print(package_name)
                    # # 应用名称
                    # try:
                    #     app_name = re.findall(r'title="(.*?)"', li)[0]
                    # except:
                    #     app_name = ''
                    # print(app_name)
                    # # 一级分类
                    # try:
                    #     category = re.findall(r'<a class="tag-link".*?>(.*?)</a>', li)[0]
                    # except:
                    #     category = ''
                    # print(category)
                    # # 应用描述
                    # try:
                    #     msg = re.findall(r'<div class="comment">(.*?)</div>', li)[0]
                    # except:
                    #     msg = ''
                    # print(msg)
                    # 详情页(应用界面)
                    # try:
                    #     url = re.findall(r'href="(.*?)"', li, re.S)[0]
                    #     headers = {
                    #         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47',
                    #     }
                    #     response = requests.get(url, headers=headers)
                    #     text = response.content.decode('utf8')
                    #     #判断是否有拦截验证条界面
                    #     if(re.findall("集团通用处置模板", text).__len__() !=0):
                    #         print(url)
                    #         print("需要解除验证")
                    #         # break_validation(url)
                    #         # response = requests.get(url)
                    #         # text = response.content.decode('utf8')
                    #         # print(text)
                    #     # 二级分类
                    #     try:
                    #         category_two = re.findall(r'data-track="detail-click-appTag">(.*?)</a>', text)[0]
                    #     except:
                    #         category_two = ''
                    #     print(category_two)
                    #     # 应用介绍
                    #     try:
                    #         msg_two = re.findall(r'<div data-originheight="40" class="con" itemprop="description"><div>(.*?)</div>', text)[0]
                    #     except:
                    #         msg_two = ''
                    #     print(msg_two)
                    # except:
                    #     category_two = ''
                    #     msg_two = ''
                    # data_msg = []
                    # data_msg.append(app_name)
                    # data_msg.append(package_name)
                    # data_msg.append(category)
                    # data_msg.append(msg)
                    # # data_msg.append(msg_two)
                    # save_data(data_msg)
                    # print('*' * 50)
                    # time.sleep(0.2)

            except Exception as e:
                print(e)

