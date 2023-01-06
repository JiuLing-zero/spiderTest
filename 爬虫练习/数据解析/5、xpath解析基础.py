from lxml import etree
if __name__ == '__main__':
    # 传入本地的html文件
    # parse方法 默认使用的是“XML”解析器,这里使用自定义的utf-8解析器parser,否则会报错
    parser = etree.HTMLParser(encoding='utf-8')
    tree = etree.parse('西游记小说.html',parser=parser)
    # title = tree.xpath('/html/head/title') # 左侧的/表示从根节点(标签最外层)开始,之后的一个/表示一个层级
    # title = tree.xpath('/html//title') # //表示多个层级
    # title = tree.xpath('//title') # 最左侧//表示找到所有title标签
    # # 属性定位
    # site_description = tree.xpath('//p[@class="site-description"]') # 寻找某个class类名的标签
    # # 索引定位
    # six_Hui = tree.xpath('//ul[@class="paiban"]/li[6]') # 获取第六回的标签(索引从1开始)
    # # 取文本 text()
    # six_Hui_text = tree.xpath('//ul[@class="paiban"]/li[6]/a/text()')[0] # text()即取出标签的内容
    # six_Hui_text = tree.xpath('//ul[@class="paiban"]//text()') # 也可以通过//跨级获取内容
    # # 取属性值 @
    # href = tree.xpath('//ul[@class="paiban"]/li[6]/a/@href') # 通过 @属性名 获取属性的值

    # 使用 | 可以在xpath()方法中匹配多个条件(ps: xpath(//div[@class="a"]/a | //div[@class="a"]/div))