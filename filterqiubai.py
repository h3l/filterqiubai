#!/usr/bin/pytho
#coding=utf-8

"""
    author:xidianlz
    data:6.7

过滤糗事百科的某些关键字，并过滤掉图片以及广告等
"""

import urllib2
import re
from BeautifulSoup import BeautifulSoup


def filter_enter(data):
    """传入为一个文件的列表,该列表使用readlines获得,过滤掉其中的空格换行等"""
    temp = [line.strip() for line in data]
    return "".join(temp)


def filter_keywords_pic(data):
    """过滤掉含有指定关键字和含有图片的条目"""
    key_words = [u"鬼", u"恐怖", u"吓死了"]
    #在有指定关键字的后面添加delete以便后面删除
    for item in data:
        for key in key_words:
            if key in item.contents[2].next:
                item.append("delete")
                break
    data_filter_keys = [item for item in data if "delete" not in item]
    #过滤掉含有图片的条目,
    data_filter_pic = [item for item in data_filter_keys \
                        if "pictures" not in str(item)]
    return data_filter_pic


def create_html(url, html_num):
    """传入要生成html文件的url地址，生成一个html文件"""
    content = urllib2.urlopen(url).readlines()
    text_without_enter = filter_enter(content)
    soup = BeautifulSoup(text_without_enter)
    #找出所有的糗事条目
    items = soup.findAll("div", attrs={"class": "block untagged mb15 bs2"})
    filter_data = filter_keywords_pic(items)
    #过滤出最终糗事的部分
    final_data = []
    for item in filter_data:
        to_encode_text = item.findAll("div", title=re.compile(".*"))[0].contents
        encoded_text = [unicode(i) for i in to_encode_text]
        final_data.append("".join(encoded_text))
    #生成html文件
    final_html = ["<p>"+i+"</p><hr>" for i in final_data]
    text_result = "".join(final_html)
    #为生成的html添加头部信息，包括编码以及css文件的链接
    text_result = u'<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><link href="qiubai.css" rel="stylesheet" type="text/css"></head>'+text_result
    text_result += u"<a href=" + unicode(html_num + 1) + u".html>下一页</a>"
    html_name = u"/home/yourname/youpath"+str(html_num)+u".html"
    result = open(html_name, "w")
    result.write(text_result.encode("utf8"))
    result.close()

if __name__ == "__main__":
    base_url = "http://qiushibaike.com/8hr/page/"
    for page_num in range(1, 36):
        url = base_url + str(page_num)
        print url
        create_html(url, page_num)
