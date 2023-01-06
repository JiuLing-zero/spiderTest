import requests
# 爬取搜狗首页的页面数据
if __name__ == '__main__':
    # 1、指定url
    url = 'https://www.sogou.com/'
    # 2、发起请求
    # get方法会返回一个响应对象
    response = requests.get(url=url)
    # 3、获取响应数据。text返回的是字符串形式的响应数据
    page_text = response.text
    print(page_text)
    with open('./sogou.html','w',encoding='utf-8') as fp:
        fp.write(page_text)
    print("爬取数据结束......")