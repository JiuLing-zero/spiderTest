import re
import requests
import os
# 需求:爬取图片网站上所有的图片
if __name__ == '__main__':
    url = "http://pic.netbian.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Mobile Safari/537.36'
    }
    # 通过爬虫爬取整张页面
    page_text = requests.get(url=url,headers=headers).text
    # 使用正则表达式对所有图片链接进行提取(只要下面字符串内 括号里的部分)
    ex ='<li><a href=".*?<img src="(.*?)".*?</li>'
    img_src_list = re.findall(ex,page_text,re.S)

    # 创建一个文件夹来保存图片
    if not os.path.exists("./壁纸图片"):
        os.mkdir("./壁纸图片")

    for src in img_src_list:
        src = "http://pic.netbian.com"+src
        # 请求到图片的二进制数据
        img_data = requests.get(url=src,headers=headers).content
        # 生成图片名称(根据图片的url)
        img_name = src.split("/")[-1]
        # 图片的存储路径
        img_Path = "./壁纸图片/" + img_name
        with open(img_Path,"wb") as fp:
            fp.write(img_data)
            print(img_name,'下载成功')
