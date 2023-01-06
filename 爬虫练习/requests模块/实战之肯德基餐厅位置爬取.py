import requests
# 这里指定了获取杭州的信息,也可以input动态获取任何城市的信息
if __name__ == '__main__':
    # 原网站(自行拷贝到浏览器看)
    html = 'http://www.kfc.com.cn/kfccda/storelist/index.aspx'
    # 发起post请求的url
    url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'
    data = {
        'cname':'',
        'pid':'',
        'keyword': '杭州',
        'pageIndex': '1',
        'pageSize': '10'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    # 获取Ajax局部刷新的数据text数据
    response = requests.post(url=url,data=data,headers=headers)
    page_text = response.text
    with open('./肯德基餐厅位置信息.txt','w',encoding='utf-8') as fp:
        fp.write(page_text)