import json
import requests
#读取豆瓣电影某个类型的排行榜
if __name__ == '__main__':
    # 排行榜网站(自行拷贝到浏览器看)
    html = 'https://movie.douban.com/chart'
    # 发起get请求的url
    url = 'https://movie.douban.com/j/chart/top_list'
    # 下面参数是剧情片类型的Ajax请求参数
    param = {
        'type':'11',
        'interval_id':'100:90',
        'action':'',
        'start':'0',# 从库中的第几部电影去取
        'limit':'20'# 一次取出的个数
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    # 获取Ajax局部刷新的json数据
    response = requests.get(url=url, params=param, headers=headers)
    list_data = response.json()
    # 进行持久化存储
    fp = open('./豆瓣电影剧情类型排行榜.json','w',encoding='utf-8')
    json.dump(list_data,fp=fp,ensure_ascii=False)
    print("爬取豆瓣排行榜结束......")