# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import time
import random
from mySpider.Mysql import Mysql


class MyspiderPipeline(object):

    def __init__(self):
        print("-----保存数据------")
        self.csvFile = open("./JDdata.csv", "a", encoding="utf-8")
        self.writer = csv.writer(self.csvFile)
        self.fileHeader = ["title", "type", 'price', 'num']
        self.writer.writerow(self.fileHeader)
        self.mysql = Mysql()


    def process_item(self, item, spider):

        print("-----准备写入数据------")
        #商品信息列表
        time.sleep(random.randint(1, 3))
        print('-'*20)
        print(item.get('name'))
        print('-'*20)
        if item.get('name') == 'suning':
            g = item.get("data").get("g_list")
            print("开始写入数据--------------")
            param = []
            for i in range(len(g)):
                #print("存储数据：", g[i],  '0', item['type_info'])
                param.append([g[i], '0', item['type_info'] ])
            self.mysql.add(param)

               # self.writer.writerow([g[i], item['type_info'], '0', '0'])

        elif item.get('name') == 'taobao':
            g = item.get("data").get("g_list")
            price_list = item.get("data").get("price_list")
            # 获取价格
            price = g.xpath('//strong/text()').extract()
            tag_title = g.xpath('//a[@class="J_ClickStat"]')
            # 获取标题文本
            title = tag_title.xpath('string(.)').extract()
            # 销量
            num = g.xpath("//p[@class='deal-cnt']").xpath('string(.)').extract()
            # g_dict["price"] = price
             # g_dict['title'] = title
             # g_dict['num'] = num
            # print("商品数据： ", g_dict)
            for i in range(len(title)):
                line = [title[i], "本地生活--游戏充值--游戏点卡", price[i], num[i]]
                self.writer.writerow(line)

        elif item.get('name') == 'benlai':
            BenLai(item.get("data"), self.writer)

        elif item.get('name') == 'dangdang':
            DangDang(item.get("data"), self.writer)

        elif item.get('name') == 'jd':
            JD(item.get("data"), self.mysql)

        elif item['name'] == 'jdurl':
            JDurl(item["url"], self.mysql)
        elif item['name'] == 'suning_url':
            SuNingurl(item["url"], self.mysql)
        return item

    def close_spider(self, spider):
        self.csvFile.close()
        self.mysql.close()



"""
data: 商品数据字典
"""
def BenLai(data, file_obj):

    title_list = data.get("title")
    price_list = data.get("price")
    type_info = data.get("type_info")
    for i in range(len(title_list)):

        file_obj.writerow([title_list[i], type_info, price_list[i], '0'])


def DangDang(data, file_obj):
    title_list = data.get("title_list")
    price_list = data.get("price_list")
    type_info = data.get("type_info")
    for i in range(len(title_list)):
        file_obj.writerow([title_list[i], type_info, price_list[i], '0'])

def JD(data, mysql):
    title_list = data.get("title_list")
    type_info = data.get("type_info")
    param = []
    for i in range(len(title_list)):
        param.append([title_list[i], '0', type_info])

    mysql.add(param)


def JDurl(data, mysql):
    url_list = data
    print("正在保存数据到mysql")
    for url in url_list:

        mysql.addurl(url)

def SuNingurl(data, mysql):
    url_list = data
    print("正在保存数据到mysql")
    for url in url_list:

        mysql.addSuNingUrl(url.extract())
