#!/usr/bin/python
#coding=utf-8

""" author:xidianlz
    data:6.7

过滤糗事百科的某些关键字，并过滤掉图片以及广告等
"""

import urllib2
import chardet
import re
from BeautifulSoup import BeautifulSoup


def filter_enter(data):
    """传入为一个文件的列表,过滤掉其中的空格换行等"""
    temp = [line.strip() for line in data]
    return "".join(temp)

def filter_keywords_pic(data):
    """过滤掉含有指定关键字和含有图片的条目"""
    keys = [u"鬼",u"恐怖",u"吓死了"]
    
    for item in data:
        for key in keys:
            if key in item.contents[2].next:
                item.append("delete")
                break
    data_filter_keys = [item for item in data if "delete" not in item]

    data_filter_pic = [item for item in data_filter_keys \
    if "pictures" not in str(item)]
    return data_filter_pic

def create_html(url, html_num):
    content = urllib2.urlopen(url).readlines()
    final = filter_enter(content)
    soup = BeautifulSoup(final)
    items = soup.findAll("div", attrs={"class":"block untagged"})
    filter_data = filter_keywords_pic(items)

    final_data = []
    for item in filter_data:
        to_encode_text = item.findAll("div",title=re.compile(".*"))[0].contents
        encoded_text = [unicode(i) for i in to_encode_text]
        final_data.append("".join(encoded_text))

    final_html = ["<p>"+i+"</p><br>" for i in final_data]
    text_tesult = "".join(final_html)
    text_tesult += u"<a href=" + unicode(html_num + 1) + u".html>下一页</a>"
    html_name = u"/home/xidianlz/code/python/"+str(html_num)+u".html"
    result = open(html_name,"w")
    result.write(text_tesult.encode("utf8"))
    result.close()

if __name__ == "__main__":
    base_url = "http://qiushibaike.com/hot/page/"
    for page_num in range(1,36):
        url = base_url + str(page_num)
        print url
        create_html(url,page_num)
#     content = urllib2.urlopen(base_url).readlines()
# #    content = open("/home/xidianlz/b.html").readlines()
#     final = filter_enter(content)

#     soup = BeautifulSoup(final)
#     items = soup.findAll("div", attrs={"class":"block untagged"})
#     filter_data = filter_keywords_pic(items)

#     final_data = []
#     for item in filter_data:
#         to_encode_text = item.findAll("div",title=re.compile(".*"))[0].contents
#         encoded_text = [unicode(i) for i in to_encode_text]
#         final_data.append("".join(encoded_text))

#     final_html = ["<p>"+i+"</p><br>" for i in final_data]
#     text_tesult = "".join(final_html)
#     result = open("/home/xidianlz/code/python/result.html","w")
#     result.write(text_tesult.encode("utf8"))
