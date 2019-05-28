# -*- coding: utf-8 -*-
import scrapy
from mySpider.items import SuNingurlspiderItem

class SuningUrlSpider(scrapy.Spider):
    name = 'suning_url'
    allowed_domains = ['suning.com']
    start_urls = ['https://list.suning.com/#20089']

    def parse(self, response):
        item = SuNingurlspiderItem()
        url_list = response.xpath('//div[@class="title-box clearfix"]//div[@class="t-right fl clearfix"]//a/@href')
        print("一共获取{}个标签分类url。".format(len(url_list)))

        item["name"] = "suning_url"
        item["url"] = url_list

        yield item
