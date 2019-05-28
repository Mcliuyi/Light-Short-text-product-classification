# -*- coding: utf-8 -*-
import scrapy

import re

from mySpider.items import JDurlspiderItem


class JdurlSpider(scrapy.Spider):
    name = 'jdurl'
    allowed_domains = ['jd.com']
    start_urls = ['https://www.jd.com/allSort.aspx']

    def parse(self, response):
        urls_obj = response.xpath("//div[@class='items']//dd/a/@href")
        url_list = []
        item = JDurlspiderItem()
        item['name'] = 'jdurl'
        item['url'] = url_list

        url = response.url
        print("当前访问url: ", url)
        rlt = re.search('.html$', url)
        print("rlt: ", rlt)
        if rlt != None:
            urls_obj1 = response.xpath("//ul[@class='i-ext']//a/@href")
            urls_obj2 = response.xpath("//div[@class='ext']/p//a/@href")
            urls_obj3 = response.xpath("//div[@class='item']//p[@class='item_header_sublinks']/a/@href")
            print("urls_obj1:", urls_obj1)
            print("urls_obj2", urls_obj2)
            for urls in urls_obj1:
                url = urls.extract()
                url_list.append(url)

            for urls in urls_obj2:
                url = urls.extract()
                url_list.append(url)
        else:
            for urls in urls_obj:

                url = urls.extract()
                # 如果url结尾包含.html代表还有下一级分类
                rlt = re.search('.html$', url)

                if rlt != None:
                    url = "https:" + url
                    print("重写访问url：", url)
                    yield scrapy.Request(url=url, callback=self.parse)

                else:

                    rlt =re.search('.com/$', url)
                    rlt2 =re.search('^//piao', url)
                    if rlt == None and rlt2 == None:
                        url_list.append(url)

        yield item

