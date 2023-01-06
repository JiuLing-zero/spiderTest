import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Mobile Safari/537.36'
}
urls = [
    'http://pic.netbian.com/4kfengjing/',
    'http://pic.netbian.com/4kdongman/',
    'http://pic.netbian.com/4kyingshi/'
]

def get_contene(url):
    print('正在爬取:',url)
    # get方法是一个会阻塞的方法
    response = requests.get(url=url,headers=headers)
    if response.status_code == 200 :
        return response.content

def parse_content(content):
    print('响应数据的长度为:',len(content))

for url in urls:
    content = get_contene(url)
    parse_content(content)