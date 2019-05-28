# -*- coding: utf-8 -*-
import scrapy

from mySpider.Mysql import Mysql


class JdUrlCleanSpider(scrapy.Spider):
    name = 'jd_url_clean'
    allowed_domains = ['jd.com']
    mysql = Mysql()
    url_list, id_dict = mysql.queryAllUrl()
    start_urls = url_list

    def parse(self, response):

        url = response.url

        if url == "https://www.jd.com/error.aspx":

           pass

        else:
            # 当前分类页数
            page = response.xpath('//*[@id="J_topPage"]/span/i/text()').extract()
            print("url: ", url, " page : ", page)
            id = self.id_dict.get(url)

            url_list = url.split("#")
            print(url_list)
            l = len(url_list)
            if id == None:
                if l >= 2:
                    end_url = url_list[1]

                    if end_url == "#J_crumbsBar":

                        url = url_list[0] + "#J_main"
                    elif end_url == "#J_main":

                        url = url_list[0] + "#J_crumbsBar"
                    id = self.id_dict.get(url)
                else:

                    url  = url_list[0] + "#J_main"
                    id = self.id_dict.get(url)
                    if id == None:
                        url = url_list[0] + "#J_crumbsBar"
                        id = self.id_dict.get(url)
                    if id == None:
                        url = url_list[0] + "#J_searchWrap"
                        id = self.id_dict.get(url)


            if page :
                self.mysql.updatePage(page, id)

            print("当前分类页数， id, url ", page, id, url)


