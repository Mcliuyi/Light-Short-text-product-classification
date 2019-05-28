import pymysql
import logging
import time
import string
from urllib.parse import quote
class Mysql:

    def __init__(self):

       self.conn = pymysql.connect(host='139.199.222.121', port=3306, database='fc', user='root', password='mysql123',
                               charset='utf8')

       self.cur = self.conn.cursor()

       self.sql = ''

    def add(self, param):
        self.conn.ping(reconnect=True)
        self.sql =  "insert into pcdata (title ,price, type) values(%s, %s, %s)"
        ret = self.cur.executemany(self.sql, param)
        self.conn.commit()
        print("执行结果：", ret)

    def addurl(self, url):
        self.sql = "insert into url (url) values(%s);"
        ret = self.cur.execute(self.sql, [url])
        self.conn.commit()
        #print("执行结果：", ret)

    def addSuNingUrl(self, url):
        self.conn.ping(reconnect=True)
        self.sql = "insert into suning_url (url) values(%s);"
        ret = self.cur.execute(self.sql, [url])
        self.conn.commit()
        print("执行结果：", ret)

    def queryUrl(self):
        self.sql = "select id, url, tpage from url where status=0 limit 0, 1"
        self.cur.execute(self.sql)
        urls_list = []
        id_list = []
        page = 0
        rlt = True
        while rlt:
            rlt = self.cur.fetchone()
            if rlt != None:
                if "https:" in rlt[1]:
                    urls_list.append(rlt[1])
                else:
                    urls_list.append("https:" + rlt[1])
                page = rlt[2]
                self.update(rlt[0])
                id_list.append(rlt[0])
        #logging.info("Mysql urls: ", urls_list)

        print("Mysql urls: ", urls_list)

        return urls_list, page

    def queryAllUrl(self):
        self.sql = "select id, url from url where tpage is null"
        self.cur.execute(self.sql)
        urls_list = []
        id_dict = {}
        rlt = True
        while rlt:
            rlt = self.cur.fetchone()
            if rlt != None:
                if "https:" in rlt[1]:
                    url = quote(rlt[1], safe=string.printable)
                    urls_list.append(url)
                    id_dict[url] = rlt[0]
                else:
                    url = quote(rlt[1], safe=string.printable)
                    urls_list.append("https:" + url)
                    id_dict["https:" + url] = rlt[0]



        return urls_list, id_dict


    def querySuNingUrl(self):
        self.sql = "select id, url from suning_url where status=0 limit 0, 1"
        self.cur.execute(self.sql)
        urls_list = []
        rlt = True
        while rlt:
            rlt = self.cur.fetchone()
            if rlt != None:
                if "https:" in rlt[1]:
                    urls_list.append(rlt[1])
                else:
                    urls_list.append("https:" + rlt[1])
                self.updateSuNing(rlt[0])
        #logging.INFO("Mysql urls: ", urls_list)
        print("Mysql urls: ", urls_list)
        return urls_list

    def updatePage(self, tpage, id):
        print("修改url页数")
        self.sql = "update url set tpage=%s where id=%s"
        rlt = self.cur.execute(self.sql, [tpage, id])
        self.conn.commit()
        print(rlt)


    def updateSuNing(self, id):
        print("修改")
        #self.sql = "update url set status=1 where url=%s;"
        self.sql = "update suning_url set status=1,end_time=%s where id=%s;"
        end_time = "".join(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(type(end_time))
        rlt = self.cur.execute(self.sql, [end_time, id])
        self.conn.commit()
        print(rlt)

    def updatePage(self, page, id):
        self.sql = "update url set page=%s where id=%s;"
        self.conn.ping(reconnect=True)
        rlt = self.cur.execute(self.sql, [page, id])
        self.conn.commit()
        # print(rlt)


    def update(self, id):
        print("修改")
        #self.sql = "update url set status=1 where url=%s;"
        self.sql = "update url set status=1, end_time=%s where id=%s;"
        end_time = "".join(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        rlt = self.cur.execute(self.sql, [end_time, id])
        self.conn.commit()
        print(rlt)

    def delUrl(self, id):
        print("删除无用url")
        self.sql = "delete from url where id=%s"
        rlt = self.cur.execute(self.sql, id)
        self.conn.commit()
        print(rlt)

    def close(self):

        self.conn.close()
        self.cur.close()

def Rurl():
    sql = Mysql()
    with open("./SuNingurl.txt", 'r') as f:
        urls_list = f.readlines()
        for i in  urls_list:
            sql.addSuNingUrl(i.strip())
            #print(i.strip())



if __name__ == "__main__":

    sql = Mysql()

    #sql.add("测试", '0', '测试')
    name = "//list.jd.com/list.html?cat=1713,4855,4859"
   # print(sql.update(name))
   #  for i in range(4408, 4413):
   #      sql.delUrl(i)
   #  sql.delUrl(4992)
   #  sql.delUrl(4913)
   #  sql.delUrl(4909)
    # sql.delUrl(4362)
    # urls_list, id_dict = sql.queryAllUrl()
    param = []
    for i in range(0, 5):
        param.append(["ceshi", "0", "0"])
    sql.add(param)

    # print(sql.queryUrl())
    # sql.addurl("//list.jd.com/list.html?cat=9987,653,659")
    # sql.addurl("//list.jd.com/list.html?cat=9987,6880,6881")
    sql.close()
   #  Rurl()