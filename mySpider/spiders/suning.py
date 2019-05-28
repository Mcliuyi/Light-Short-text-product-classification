# -*- coding: utf-8 -*-
import scrapy

from mySpider.Mysql import Mysql


class SuningSpider(scrapy.Spider):
    name = 'suning'
    allowed_domains = ['suning.com']
    # mysql = Mysql()
    # url_list = mysql.querySuNingUrl()
    # start_urls = url_list
    # start_urls = ["https://list.suning.com/0-505930-0.html"]
    def parse(self, response):
        print("！"*100)
        print("处理数据中----")

        tyep_info = ""
        url = response.url
        print("start_urls ", self.start_urls)
        print("url ", url)
        first_type_infos = response.xpath('//*[@id="search-path"]/a[2]/text()').extract()[0]

        second_type_info = response.xpath('//*[@id="search-path"]/dl[1]/dt/a/text()').extract()[0]
        try:
            thrid_type_info  = response.xpath('//*[@id="search-path"]/dl[2]/dt/a/text()').extract()[0]
        except Exception as e:
            print("切换三级分类规则: ", e)
            thrid_type_info = response.xpath('(//*[@id="search-path"]/a[@class="result-right"]/text())[2]').extract()[0]

        tyep_info = first_type_infos + "--" + second_type_info + "--" + thrid_type_info
        print("当前分类为：", tyep_info)
        print(response.url)
        item = {}
        g_list = []
        print("-" * 100)
        print("处理商品")
        g_li = response.xpath("//li[@doctype=1]//img/@alt")
        print("-"*100)

        print("商品长度：", len(g_li))
        #print("价格长度：", len(price_li))
        for i in range(len(g_li)):
            info = g_li[i].extract()
            #print(info)
            if info != "":
                g_list.append(info)


        item['data'] = {"g_list":g_list, "type_info":tyep_info}
        item['name'] = 'suning'
        item["type_info"] = tyep_info
        print("处理结束-------------------------")
        mysql = Mysql()
        urls_list = mysql.querySuNingUrl()
        mysql.close()
        yield scrapy.Request(url=urls_list[0], callback=self.parse)

        yield item

    def __del__(self):
        # self.mysql.close()
        pass

