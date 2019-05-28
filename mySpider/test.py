import json

import requests
from lxml import etree
import random
import threading

def rIp():
    ip_list = []
    f = open("./ip.json", 'r')
    #print(json.load(f))
    line = f.readline()
    while line:
        ip_list.append(json.loads(line))
        line = f.readline()
    f.close()
    print(len(ip_list))
    #print(ip_list)
    return ip_list

def valVer(proxys):
    badNum = 0
    goodNum = 0
    good=[]
    for proxy in proxys:
        try:
            proxy_host = proxy
            protocol = 'https' if 'https' in proxy_host else 'http'
            proxies = {protocol: proxy_host}
            response = requests.get('http://www.baidu.com', proxies=proxies, timeout=2)
            if response.status_code != 200:
                badNum += 1
                print (proxy_host, 'bad proxy')
            else:
                goodNum += 1
                good.append(proxies)
                with open("./ip.json", "a") as f:
                    json.dump(proxy_host, f)
                    f.write("\n")
                    print("加载入文件完成...")
                print (proxy_host, 'success proxy')
        except Exception as e:
            print(proxy_host, 'bad proxy')
            print(e)
            # print proxy_host, 'bad proxy'
            badNum += 1
            continue
    print ('success proxy num : ', goodNum)
    print( 'bad proxy num : ', badNum)
    return good


def get_ip_list(url,headers):

    rlt = requests.get(url=url, headers=headers)
    #print(rlt.text)
    html = etree.HTML(rlt.text)
    print(html)
    ip_list = html.xpath('//*[@id="ip_list"]//tr//td[2]/text()')

    ip_prot = html.xpath('//*[@id="ip_list"]//tr//td[3]/text()')
    print(len(ip_list), len(ip_prot))
    print(ip_list)
    print(ip_prot)
    proxys = []
    for i in range(len(ip_prot)):
        proxys.append({'https':ip_list[i]+":"+ip_prot[i]})

    #return proxys
    valVer(proxys)


def get_ip():
    PROXIES = rIp()
    proxy = random.choice(PROXIES)

    return proxy

def thread_get_ip_list(url,headers):
    t = threading.Thread(target=get_ip_list, args=(url,headers))
    t.start()


if __name__ == '__main__':
    proxys = [
            {'https':"125.123.141.201:9999"},
            {'https':'144.123.71.35:9999'}
            ]
    USER_AGENTS = [
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
    ]

    #valVer(proxys)
    import time
    # 开始时间
    start_time = time.time()
    for i in range(1, 200):
        time.sleep(0.2)
        header = {'User-Agent': random.choice(USER_AGENTS)}
        url = "https://www.xicidaili.com/wn/%d"%i
        thread_get_ip_list(url, header)
        #proxys = get_ip_list(url, header)
        # valVer(proxys)
        #proxys = rIp()
        #valVer(proxys)

    end_time = time.time()
    print("一共花费：", end_time-start_time)