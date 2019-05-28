# -*- coding: utf-8 -*-
import scrapy


class BenlaiSpider(scrapy.Spider):
    name = 'benlai'
    allowed_domains = ['benlai.com']
    # 海产干货
    start_urls = ['https://www.benlai.com/list-2800-2885.html']


    def parse(self, response):
        type_info = ""
        if self.start_urls[0] ==  response.url:
            type_info = "生鲜水果--海鲜水产--海产干货"


        #商品标题
        goods_title = response.xpath("//p[@class='name']//font/text()")
        goods_price = response.xpath("//p[@class='price']/text()")

        titles_list = []
        prices_list = []
        for i in range(len(goods_title)):

            title = goods_title[i].extract()
            price = goods_price[i].extract()
            titles_list.append(title)
            prices_list.append(price)

        item = {}
        item['name'] = "benlai"
        item["data"] = {'title':titles_list, 'price':prices_list, "type_info":type_info}
        yield item


