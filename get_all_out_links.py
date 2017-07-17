#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/17 下午10:26
# @Author  : Sylor_Huang
# @File    : get_all_out_links.py
# @Software: PyCharm
from bs4 import BeautifulSoup
import requests
import re
import random
import datetime

pages = set()
random.seed(datetime.datetime.now())

###获取所有内链的地址,并返回列表
def getinLinks(bsObj,includeUrl):
    try:
        interLinks = []   ##建立内链列表
        for links in bsObj.find_all('a',href=re.compile("^(/|.*"+includeUrl+")")):  ###查找所有内链
            if links.attrs['href'] is not None:  ##判断内链的href属性是否存在
                if links.attrs['href'] not in interLinks:   ##判断内链的href是否在内链列表里，如果不在则追加进去
                    interLinks.append(links.attrs['href'])
        return interLinks
    except:
        return None

###获取所有外链的地址，并
def getoutLinks(bsObj,excludeUrl):
    try:
        outLinks = []
        for links in bsObj.find_all('a',href=re.compile("^(http|www)((?!"+excludeUrl+").)*$")):
            if links.attrs['href'] is not None:
                if links.attrs['href'] not in outLinks:
                    outLinks.append(links.attrs['href'])

        return outLinks
    except:
        return None



#
def response(url):
    try:
        content = requests.get(url)
        if content.status_code == 200:
            return content.text
        else:
            print('链接错误')
    except:
        return None

###把链接转换为字符串，并生成列表。此函数用返回的字符串，判断是否为内链的依据。
def urltoStr(starturl):
    urlTostr = starturl.replace("http://","").split("/")
    return urlTostr[0]


##获取页面信息并根据getLinLinks()函数返回的内链列表，来调用getoutLinks()函数获取随机外链
def getrandomHtml(starturl):
    try:
        startstr = urltoStr(starturl)
        html = response(starturl)
        bsObj = BeautifulSoup(html, 'lxml')
        outlinks = getoutLinks(bsObj,startstr)
        if len(outlinks) == 0:
            inlinks = getinLinks(bsObj,startstr)
            return getrandomHtml(inlinks[random.randint(0,len(inlinks)-1)])  ##回调getrandomHtml()函数，重新获得新内链
        else:
            return outlinks[random.randint(0,len(outlinks)-1)]

    except:
        return None


def main(starturl):
    randomurl = getrandomHtml("http://oreilly.com")   ###此处用starturl的话，会返回错误。用字符串的话，返回才正常。疑问？？？是不是初始化的原因？？
    print('随机外链是：'+str(randomurl))
    main(randomurl)

if __name__ == '__main__':
    starturl = "http://oreilly.com"
    main(starturl)
