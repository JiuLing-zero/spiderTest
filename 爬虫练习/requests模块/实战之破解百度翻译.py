import json
import requests
# post请求(携带了参数)
# 响应数据是一组json诉苦
# 只能查一个单词或一个中文词语
if __name__ == '__main__':
    # 1、指定url
    post_url = 'https://fanyi.baidu.com/sug'
    # 2、post请求参数处理
    word = input('输入要查询的单词:')
    data = {
        'kw':word
    }
    # 3、进行UA伪装
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    # 请求发送
    response = requests.post(url=post_url, data=data, headers=headers)
    # 获取响应数据:json()方法返回的是obj对象(如果确认响应数据是json类型，才可以使用json()方法)
    dic_obj = response.json()
    print(dic_obj)
    # 持久化存储
    fileName = word+'.json'
    fp = open(fileName,'w',encoding='utf-8')
    # ensure_ascii=False表示不使用ASCLL码，因为json中有中文
    json.dump(dic_obj,fp=fp,ensure_ascii=False)
    print("爬取翻译内容完成......")