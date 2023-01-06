import requests

# UA:User-Agent(请求载体的身份标识)
# UA检测:门户网站的服务器会检测对应请求的载体身份标识，如果检测到的载体身份标识为某一款浏览器说明该请求是正常的请求。
#       但如果检测到的载体身份标识不是基于某款浏览器的，则该请求是不正常的请求(爬虫)，服务器有可能拒绝该请求

# UA伪装:让爬虫对应的请求载体身份标识，伪装成某一款浏览器
if __name__ == '__main__':
    url = 'https://www.sogou.com/web'
    # 处理url所携带的参数————封装到字典中
    kw = input('输入查询内容:')
    param = {
        'query':kw
    }
    # UA伪装:将对应的User-Agent封装到一个字典中
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    # 对指定url发起的请求，对应的url是携带参数的，并且请求过程中处理了参数
    response = requests.get(url=url, params=param, headers=headers)
    page_text = response.text
    fileName = kw + '.html'
    with open(fileName,'w',encoding='utf-8') as fp:
        fp.write(page_text)
    print(fileName,"保存成功......")
