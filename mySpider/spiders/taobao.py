# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from lxml import etree

class BenlaiSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['taobao.com']
    #start_urls = ['https://s.taobao.com/search?spm=a21bo.2017.201867-links-7.2.28f411d9lPbbhb&q=%E6%B8%B8%E6%88%8F&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20181010&ie=utf8&cps=yes&ppath=165336971%3A92512&style=list']
    #游戏点卡
    #start_urls = ['https://s.taobao.com/search?q=%E6%B8%B8%E6%88%8F%E7%82%B9%E5%8D%A1&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20190121&ie=utf8']
    #qq充值
    #start_urls = ['https://s.taobao.com/search?q=QQ%E5%85%85%E5%80%BC&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20190121&ie=utf8']
    #猫零食, 磨牙
    start_urls = ['https://s.taobao.com/list?q=%E7%A3%A8%E7%89%99&cat=29%2C50007216&seller_type=taobao&spm=a217z.7278721.1000187.1&style=list', 'https://s.taobao.com/list?q=%E7%A3%A8%E7%89%99&cat=29%2C50007216&style=grid&seller_type=taobao&spm=a217z.7278721.1000187.1&cps=yes&ppath=3812461%3A132185']

    def parse(self, response):

        #soup = BeautifulSoup(response.text, "lxml")
        # html = response.text
        # selector = etree.HTML(html)
        #print(soup)
        # with open("./taobao.html", "w") as f:
        #     f.write(soup)
        # 获取所有商品标题
        #title = response.xpath('//*[@id="mainsrp-itemlist"]/div/div/div/div/div//a[@class="J_ClickStat"]')
        # 获取所有商品的div
        g_div = response.xpath('//*[@id="mainsrp-itemlist"]/div/div/div/div/div')

        g_list = []

        # for g in g_div:
        #     g_list.append(g)
        # print(title)
        #for i in title:
            #print(i.content)
            #info = i.xpath('string(.)').extract()[0]
           # print(info)
        item = {}

        item["data"] = g_div[0]

        yield item
