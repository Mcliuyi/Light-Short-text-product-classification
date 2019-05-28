# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import base64
import random
from .test import get_ip
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from selenium.webdriver.common.keys import Keys

from .Util import *


class MyspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ChromeDriverDownloaderMiddleware(object):
    """
    改为chromedirver访问
    """

    def process_request(self, request, spider):
        print("----ChromeDriverDownloaderMiddleware---")
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        import time
        chrome_options = Options()
        #设置无头
        #chrome_options.add_argument('--headless')
        # 禁止图片加载
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url=request.url)
        # 记录内容
        content = driver.page_source
        #滑动页面到下一页的位置
        #js = "var q=document.documentElement.scrollTop=6000"
        for i in range(2, 101):
            print("当前访问url: " , driver.current_url)
            #driver.execute_script(js)
            time.sleep(5)
            #点击下一页
            try:
                #page = driver.find_elements_by_xpath("//a[contains(.,'下一页')]")[-1]
                #driver.find_element_by_xpath("//input[@aria-label='页码输入框']").send_keys(i)
                driver.find_element_by_xpath("//span[@class='btn J_Submit']").click()
                # if(page == None):
                #     page = driver.find_element_by_xpath("//button[contains(.,'下一页')]")
                # page.click()
                content += driver.page_source
            except Exception as e:
                print("点击下一页失败{}, 第{}页：".format(e, i))
                time.sleep(1000)
                break
        #driver.quit()
        return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)


class SuNingDownloaderMiddleware(object):
    """
    改为chromedirver访问
    """

    def process_request(self, request, spider):
        print("----ChromeDriverDownloaderMiddleware---")

        chrome_options = Options()
        #设置无头
        chrome_options.add_argument('--headless')
        # 禁止图片加载
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url=request.url)
        content = ''
        #滑动页面到下一页的位置
        js = "var q=document.documentElement.scrollTop=12000"
        for i in range(1, 100):
            print("当前访问url: " , driver.current_url)
            time.sleep(random.randint(1, 3))
            driver.execute_script(js)
            time.sleep(random.randint(2, 4))
            # 记录内容
            content += driver.page_source
            #点击下一页
            try:
                #page = driver.find_elements_by_xpath("//a[contains(.,'下一页')]")[-1]
                #driver.find_element_by_xpath("//input[@aria-label='页码输入框']").send_keys(i)
                #driver.find_element_by_id("nextPage").click()
                driver.find_element_by_id("nextPage").send_keys(Keys.ENTER)
                content += driver.page_source
            except Exception as e:
                print("点击下一页失败{}, 第{}页：".format(e, i))
                #time.sleep(1)
                break
        driver.quit()
        print("-----请求结束----")
        print("*"*100)
        return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)

class SuNingUrlDownloaderMiddleware(object):
    """
    改为chromedirver访问
    """

    def process_request(self, request, spider):
        print("----SuNingUrlDownloaderMiddleware---")

        chrome_options = Options()
        #设置无头
        chrome_options.add_argument('--headless')
        # 禁止图片加载
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url=request.url)
        content = ''
        #滑动页面到下一页的位置
        js = "var q=document.documentElement.scrollTop=12000"
        for i in range(1, 100):
            print("当前访问url: " , driver.current_url)
            time.sleep(random.randint(1, 3))
            driver.execute_script(js)
            time.sleep(random.randint(2, 5))
            # 记录内容
            content += driver.page_source
            #点击下一页
            try:
                #page = driver.find_elements_by_xpath("//a[contains(.,'下一页')]")[-1]
                #driver.find_element_by_xpath("//input[@aria-label='页码输入框']").send_keys(i)
                #driver.find_element_by_id("nextPage").click()
                driver.find_element_by_id("nextPage").send_keys(Keys.ENTER)
                content += driver.page_source
            except Exception as e:
                print("点击下一页失败{}, 第{}页：".format(e, i))
                #time.sleep(1)
                break
        driver.quit()
        print("-----请求结束----")
        print("*"*100)
        return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)



class BenLaiDownloaderMiddleware(object):
    """
    改为chromedirver访问
    """

    def process_request(self, request, spider):
        print("----ChromeDriverDownloaderMiddleware---")

        chrome_options = Options()
        #设置无头
        #chrome_options.add_argument('--headless')
        # 禁止图片加载
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=chrome_options)
        url = request.url
        driver.get(url=url)
        city = driver.find_element_by_id("city_recommended")
        if city != None:
            city.click()
            time.sleep(3)
            driver.find_element_by_xpath('//dl[5]/dd/div/ul/li[6]/div[1]/a').click()
        #time.sleep(100)
        content = ''
        #滑动页面到下一页的位置
        #js = "var q=document.documentElement.scrollTop=6500"
        for i in range(1, 100):
            print("当前访问url: " , driver.current_url)
            #time.sleep(random.randint(1, 3))
            #driver.execute_script(js)
            time.sleep(random.randint(2, 5))
            # 记录内容
            content += driver.page_source
            #点击下一页
            try:
                #下一页
                driver.find_element_by_xpath('//a[@data-type="pagenext"]').click()
                content += driver.page_source
            except Exception as e:
                print("点击下一页失败{}, 第{}页：".format(e, i))
                #time.sleep(1)
                break
        driver.quit()
        print("-----请求结束----")
        print("*"*100)
        return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)


class DangDangDownloaderMiddleware(object):
    """
    改为chromedirver访问
    """

    def process_request(self, request, spider):
        print("----ChromeDriverDownloaderMiddleware---")

        chrome_options = Options()
        #设置无头
        chrome_options.add_argument('--headless')
        # 禁止图片加载
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url=request.url)
        content = ''
        #滑动页面到下一页的位置
        js = "var q=document.documentElement.scrollTop=15000"

        print("当前访问url: " , driver.current_url)
        time.sleep(random.randint(1, 3))
        driver.execute_script(js)
        time.sleep(random.randint(2, 5))
        # 记录内容
        content += driver.page_source
        driver.quit()
        print("-----请求结束----")
        print("*"*100)
        return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)


class JDDownloaderMiddleware(object):


    def process_request(self, request, spider):
        print("----JDDownloaderMiddleware---")
        time.sleep(random.randint(1, 3))
        return None





# 随机的User-Agent
class RandomUserAgent(object):
    def process_request(self, request, spider):
        useragent = random.choice(USER_AGENTS)

        request.headers.setdefault("User-Agent", useragent)


class RandomProxy(object):



    def process_request(self, request, spider):


        ip =  get_ip().get('https')
        print("当前使用代理", ip)
        request.meta['proxy'] = "https://" + ip


    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:

            ip = get_ip().get('https')
            print("当前ip被拒绝访问，重写请求 ", ip)
            print("当前使用代理", ip)
            request.meta['proxy'] = "https://" + ip
            return request
        return response

    def process_exception(self, request, exception, spider):
        # 出现异常时（超时）使用代理
        ip = get_ip().get('https')
        print("当前ip访问异常，重新请求 ", request.meta['proxy'])
        print("重新获取的ip ", ip)

        request.meta['proxy'] = "https://" + ip
        return request