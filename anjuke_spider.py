#!/usr/bin/env python
#coding:utf-8

import requests
from bs4 import BeautifulSoup
import time
from random import randint
import platform

import sys
reload(sys)

sys.setdefaultencoding('utf-8')

Agent = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50',
         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/13.10586',
         'Mozilla/5.0 (Windows NT 6.3; Win64, x64; Trident/7.0; rv:11.0) like Gecko',
         'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)',
         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:46.0) Gecko/20100101 Firefox/46.0',
         'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:46.0) Gecko/20100101 Firefox/46.0']


"""
只爬取住宅新楼盘
url: http://cd.fang.anjuke.com/loupan/all/p{}_s6_w1/
排序方式： 开盘时间

url: http://cd.fang.anjuke.com/loupan/all/p{}_w1/
排序方式： 默认排序

url: http://cd.fang.anjuke.com/loupan/all/p{}_s2/
排序方式： 价格排序
"""

# 开盘时间
#urls = ['http://cd.fang.anjuke.com/loupan/all/p{}_s6_w1/'.format(str(i)) for i in range(1, 21)]

new_house_url = ['http://cd.fang.anjuke.com/loupan/all/p{}_s6_w1/', 'http://cd.fang.anjuke.com/loupan/all/p{}_w1/', 'http://cd.fang.anjuke.com/loupan/all/p{}_s2/']


"""
武侯区 http://chengdu.anjuke.com/sale/wuhou/o5-p{}/
锦江区 http://chengdu.anjuke.com/sale/jinjiang/o5-p{}/
青羊区 http://chengdu.anjuke.com/sale/qingyang/o5-p{}/
金牛区 http://chengdu.anjuke.com/sale/jinniu/o5-p{}/
成华区 http://chengdu.anjuke.com/sale/chenghua/o5-p{}/
高新区 http://chengdu.anjuke.com/sale/gaoxin/o5-p{}/
"""
#old_urls = ['http://chengdu.anjuke.com/sale/gaoxin/o5-p{}/'.format(str(i)) for i in range(1, 51)]
loc_urls = ['http://chengdu.anjuke.com/sale/wuhou/o5-p{}/', 'http://chengdu.anjuke.com/sale/jinjiang/o5-p{}/', 'http://chengdu.anjuke.com/sale/qingyang/o5-p{}/',
             'http://chengdu.anjuke.com/sale/jinniu/o5-p{}/', 'http://chengdu.anjuke.com/sale/chenghua/o5-p{}/', 'http://chengdu.anjuke.com/sale/gaoxin/o5-p{}/']

house_urls = []

house_info = []

#二手房所有连接
used_urls = []

used_info = []

def get_house_urls(url, headers):
    web_data = requests.get(url,headers = headers)
    if str(web_data.status_code) == '200':
        time.sleep(2)
        Soup = BeautifulSoup(web_data.text, 'lxml')
        infos = Soup.select('div.infos > div.lp-name > h3 > a')
        for info in infos:
            house_urls.append(info.get('href'))
    else:
        pass

def get_house_info(url, headers):
    print 'Get house info :' + str(url)
    web_data = requests.get(url, headers = headers)
    if str(web_data.status_code) == '200':
        Soup = BeautifulSoup(web_data.text, 'lxml')
        title = Soup.select('#j-triggerlayer')[0].get_text()
        types = Soup.select('ul.info-left > li:nth-of-type')[1].get_text()
        location = Soup.select('div.basic-parms-wrap > dl > dd:nth-of-type > span')[0].get_text()
        sales_status = Soup.select('div.lp-tit > i')[0].get_text()
        price = Soup.select('div.basic-parms-wrap > dl > dd.price > p > em')[0].get_text()
        open_time = Soup.select('ul.info-left > li:nth-of-type')[0].get_text()
        end_time = Soup.select('ul.info-right > li:nth-of-type > span')[0].get_text()

        data = {
            'title':title,
            'url' : url,
            'type' : types,
            'location':location,
            'status' : sales_status,
            'price' : price,
            'open_time' : open_time,
            'end_time' : end_time
        }

        house_info.append(data)
    else:
        pass

def get_used_house_urls(url, headers):
    web_data = requests.get(url, headers=headers)
    if str(web_data.status_code) == '200':
        time.sleep(2)
        Soup = BeautifulSoup(web_data.text, 'lxml')
        infos = Soup.select('div.house-title > a')
        for info in infos:
            used_urls.append(info.get('href'))
    else:
        pass

def get_used_house_info(url, headers):
    web_data = requests.get(url, headers = headers)
    if str(web_data.status_code) == '200':
        print "Get used house info form: " + url
        Soup = BeautifulSoup(web_data.text, 'lxml')
        title = Soup.select('h3.long-title')[0].get_text()
        issue = Soup.select('#content > div.wrapper > div.wrapper-lf.clearfix > div.houseInfoBox > h4')[0].get_text()
        price = Soup.select('div.basic-info.clearfix > span.info-tag')[0].get_text()
        per_price = Soup.select('div.houseInfo-detail.clearfix > div.third-col.detail-col > dl')[1].get_text()
        rooms = Soup.select('div.basic-info.clearfix > span.info-tag')[1].get_text()
        size = Soup.select('div.basic-info.clearfix > span.info-tag.no-border')[0].get_text()
        plot = Soup.select('div.first-col.detail-col > dl > dd > a')[0].get_text()
        plot_url = Soup.select('div.first-col.detail-col > dl > dd > a')[0].get('href')
        fit = Soup.select('div.houseInfo-detail.clearfix > div.third-col.detail-col > dl')[0].get_text()
        location = Soup.select('div.houseInfo-detail.clearfix > div.first-col.detail-col > dl > dd > p.loc-text')[0].get_text()

        data = {
            'url' : url,
            'title':title,
            'plot' : plot,
            'plot_url' : plot_url,
            'issue' : issue,
            'price' : price,
            'per_price' : per_price,
            'rooms' : rooms,
            'size' : size,
            'fit' : fit,
            'location' : location
        }

        used_info.append(data)
    else:
        pass


def get_Agent():
    i = randint(0, 8)
    headers = {
        'User-Agent':Agent[i]
    }
    return headers




# url = 'http://cd.fang.anjuke.com/loupan/414095.html?from=AF_RANK_1'

def get_new_house():
	index = 0
	page = 1
	if platform.system() == 'Windows':
		index = int(raw_input(u'请选择排序方式(0 开盘时间, 1 默认排序, 2 价格) '.encode('GBK')))
		page = int(raw_input(u'请选择爬取数量（1-20) '.encode('GBK')))
	else:
		index = int(raw_input(u'请选择排序方式(0 开盘时间, 1 默认排序, 2 价格) '))
		page = int(raw_input(u'请选择爬取数量（1-20) '))

	urls = [new_house_url[index].format(str(i)) for i in range(1, page + 1)]
	print 'Scrping new house informations, be patient....'
	for url in urls:
		headers = get_Agent()
		time.sleep(8)
		get_house_urls(url, headers)

	for url in house_urls:
		time.sleep(randint(5, 20))
		headers = get_Agent()
		get_house_info(url, headers)

	f = open('new_house.txt', 'a+')
	for house in house_info:
		f.write(house['title'] + ' ' + house['url'] + ' ' + house['type'] + ' ' + house['location'] + ' ' +
                house['status'] +' 预计均价： ' +house['price'] + ' ' + house['open_time'] + ' 交房时间: ' + house['end_time'] + '\n')

	f.close()

def get_used_house():
	index = 0
	page = 1
	if platform.system() == 'Windows':
		index = int(raw_input(u'请选择爬取区域，每次只能选一个区域(0 武侯区, 1 锦江区, 2 青羊区, 3 金牛区, 4 成华区, 5 高新区) '.encode('gbk')))
		page = int(raw_input(u'请选择爬取数量（1-50) '.encode('gbk')))
	else:
		index = int(raw_input(u'请选择爬取区域，每次只能选一个区域(0 武侯区, 1 锦江区, 2 青羊区, 3 金牛区, 4 成华区, 5 高新区) '))
		page = int(raw_input(u'请选择爬取数量（1-50) '))

	old_urls = [loc_urls[index].format(str(i)) for i in range(1, page + 1)]
	print 'Scrping used house informations, be patient....'
	for url in old_urls:
		time.sleep(8)
		headers = get_Agent()
		get_used_house_urls(url, headers)

	for url in used_urls:
		url = str(url).split('?')[0]
		time.sleep(randint(5, 20))
		headers = get_Agent()
		get_used_house_info(url, headers)

	f = open('used_house.txt', 'a+')
	for info in used_info:
		f.write(info['url'] + ' ' + info['title'] + info['plot'] + ' ' + info['plot_url'] + ' ' + info['issue'] + ' ' + info['price'] + ' ' + info['per_price'] + ' ' + info['rooms']
                + ' ' + info['size'] + ' ' + info['fit'] + ' ' + info['location'] + '\n')

	f.close()

def print_error():
	if platform.system() == 'Windows':
		print u'请输入正确的信息!\n'
	else:
		print '请输入正确的信息!\n'



# #houselist-mod > li.list-item.fst-li > div.house-details > div.house-title > a

def main():
	get = ''
	if platform.system() == 'Windows':
		get = str(raw_input(u"获取新房或二手房信息(new or used?) ".encode('gbk')))
		pass
	else:
		get = str(raw_input(u"获取新房或二手房信息(new or used?) "))
		pass

	if get.lower() == 'new':
		get_new_house()
	elif get.lower() == 'used':
		get_used_house()
	else:
		print_error()
		main()


if __name__ == '__main__':
    main()