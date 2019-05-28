# -*- coding: utf-8 -*-
import scrapy


class DangdangSpider(scrapy.Spider):
    name = 'dangdang'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://category.dangdang.com/cp01.38.01.00.00.00.html']

    def parse(self, response):
        type_info = ''
        url = response.url
        print("*"*100)
        print(url)
        if url == self.start_urls[0]:
            type_info = "图书杂志--传记--财经人物"
        print("类型为：", type_info)
        title_obj = response.xpath("//li//p[@name='title']/a/text()")
        price_obj = response.xpath("//li//p[@class='price']/span[1]/text()")
        title_list = []
        price_list = []
        print("商品长度：", len(title_obj), " 价格长度：", len(price_obj))
        for i in range(len(title_obj)):
            title_list.append(title_obj[i].extract())
            price_list.append(price_obj[i].extract()[1:])

        item = {}
        item['data'] = {"title_list": title_list, "price_list": price_list, "type_info": type_info}
        item['name'] = 'dangdang'
        item["type_info"] = type_info
        print("处理结束-------------------------")
        yield item
