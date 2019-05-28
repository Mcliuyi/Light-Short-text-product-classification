# -*- coding: utf-8 -*-
import scrapy

from mySpider.Mysql import Mysql
import re
import logging

class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    current_page = 164
    # mysql = Mysql()
    # urls_list, page  = mysql.queryUrl()
    # now_page = 0
    page = 206
    #logging.INFO("[info] jd urls_list", urls_list)
    # start_urls = urls_list
    start_urls = ['https://list.jd.com/list.html?cat=1320,1585,1601&page=165&sort=sort_totalsales15_desc&trans=1&JL=6_0_0']
    # start_urls = ['https://list.jd.com/list.html?cat=9987,830,13659&page=2&sort=sort_totalsales15_desc&trans=1&JL=6_0_0']

    def parse(self, response):
        print("开始队列的url: ", self.start_urls)
        print("处理数据， 当前url: ", response.url)
        # 商品名
        title_objs = response.xpath("//*[@id='plist']/ul/li/div/div[@class='p-name']/a/em/text()")
        try:
            # 一级分类
            first_type = response.xpath('//*[@id="J_crumbsBar"]/div/div/div/div[1]/a/text()').extract()[0]
        except Exception as e:
            print("无一级分类", e)
            first_type = ""

        try:
            # 二级和三级分类
            secon_third_type = response.xpath("//span[@class='curr']/text()")
            type_info = first_type
            for i in range(len(secon_third_type)):
                type_info += "--" + secon_third_type[i].extract()
        except Exception as e:
            print("爬去二级三级失败")
            if first_type == "":
                type_info = response.xpath("/html/head/title/text()").extract()


        print("商品和价格数量")
        print(len(title_objs))
        print("当前分类为：", type_info)
        title_lists = []

        for i in range(len(title_objs)):

            title_lists.append(title_objs[i].extract().strip())

       # print(title_lists)
        item = {}
        item['data'] = {'title_list':title_lists, 'type_info':type_info}
        item['name'] = 'jd'

        try:
            self.current_page += 1
            url = 'https://list.jd.com' + response.xpath("//a[@class='pn-next']/@href").extract()[0]

            # old  = re.search("(page=)(.*?)(&)", response.url)
            new = re.search("(page=)(.*?)(&)", url)

            # if old:
            if self.current_page > int(new[2]):
                url = re.sub("(?P<n1>page=)(?P<n2>.*?)(?P<n3>&)", r"\g<n1>%s&" %self.current_page, url)

                # elif int(old[2]) >= int(new[2]):
                #     url = re.sub("(?P<n1>page=)(?P<n2>.*?)(?P<n3>&)", r"\g<n1>%s&"%(int(old[2])+1), url)
            print("当前页数：", new[2], "总页数: ", self.page, "current_page ", self.current_page)
            print("新的url为：", url)
            # self.now_page = new[2]
            # 发送新的url请求加入待爬队列，并调用回调函数 self.parse
            yield scrapy.Request(url, callback=self.parse)

        except Exception as e:
            print("当前分类爬取完毕", e)
            self.current_page = 0
            try:
                mysql = Mysql()
                urls_list, self.page = mysql.queryUrl()
                print("下个分类url: ", urls_list)
                mysql.close()
                if urls_list != None:
                    yield scrapy.Request(url=urls_list[0], callback=self.parse)
            except Exception as e:
                print("查询下一个链接失败", e)

        yield item


    # def __del__(self):
    #
    #     self.mysql.close()