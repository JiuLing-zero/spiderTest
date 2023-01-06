import requests
from lxml import etree
if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Mobile Safari/537.36'
    }
    url = 'https://hf.58.com/ershoufang/'
    page_text = requests.get(url=url,headers=headers).text
    # 数据解析
    html = etree.HTML(page_text)
    div_list = html.xpath('//section[@class="list"]/div')
    for div in div_list:
        title = div.xpath('//h3[@class="property-content-title-name"]/text()')
        print(title)
    # 写到这58同城触发反爬机制了
