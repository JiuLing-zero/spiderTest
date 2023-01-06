import requests
from bs4 import BeautifulSoup
import lxml

# 1.实例化一个BeautifulSoup对象,并且将页面源码数据加载到对象中
# 2.通过调用实例化对象的相关属性或方法 进行标签定位和数据提取
if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Mobile Safari/537.36'
    }
    url = 'http://pic.netbian.com/4kfengjing/'

    # 获取网页的源代码
    page = requests.get(url=url,headers=headers).content.decode('gbk')
    soup = BeautifulSoup(page,'lxml')
    # print(soup)
    # print(soup.a) # 返回的是html中第一次出现的a标签
    # print(soup.find('a')) # 同上一行一样
    # print(soup.find('a',class_='nav-link')) # class_ 的下划线是防止被识别为关键字
    # print(soup.find_all('a')) # 找到所有a标签,返回列表
    # print(soup.select('.gotop')) # 类选择器(返回标签的类名属性class匹配的 整个标签)
    # print(soup.select('.kf-trop > p')) # 层级选择器, < 表示一个层级
    # print(soup.select('.gotop p')) # 如果标签之间是空格,表示多个层级
    # print(soup.find('div',class_='gotop').text) # 获取目标标签下的所有文本内容
    # print(soup.select('.gotop')[0]['class']) # 获取标签的属性class的值
