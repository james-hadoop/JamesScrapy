# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from telnetlib import EC

from scrapy import signals
from selenium import webdriver
import time
import datetime
from scrapy.http.response.html import HtmlResponse
import traceback
import logging
import os

import scrapy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


# class YqcNanchangSpiderSpiderMiddleware(object):
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.
#
#         # Should return None or raise an exception.
#         return None
#
#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.
#
#         # Must return an iterable of Request, dict or Item objects.
#         for i in result:
#             yield i
#
#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.
#
#         # Should return either None or an iterable of Request, dict
#         # or Item objects.
#         pass
#
#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.
#
#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)


class YqcNanchangSpiderDownloaderMiddleware(object):
    url_prefix = 'http://www.nc.gov.cn'

    def __init__(self):
        os_info = os.uname()
        if os_info.sysname == 'Darwin':
            chrome_path = r"/Users/qjiang/install/chromedriver"
        else:
            chrome_path = r"/home/james/_AllDocMap/06_Software/chromedriver"
        self.driver = webdriver.Chrome(executable_path=chrome_path)

    def process_request(self, request, spider):
        url = request.url
        print(
            "1. process_request(): " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') + " -> " + url)
        self.driver.get(url)
        source = self.driver.page_source

        if str('currentPage') not in url:
            print("3. if finish process_request(): " + datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S.%f') + " -> " + url)
            # if str('REPORT_NDOC_006051') in url or str('REPORT_NDOC_006010') in url:
            #     print(">>> debug: " + url)
            #     print(source)

            response = HtmlResponse(url=url, body=source, request=request, encoding="utf-8")
            return response

        else:
            next_page = self.driver.find_element_by_xpath(
                "//*[@id='4864']/table/tbody/tr/td/table/tbody/tr/td[8]/a")
            url = str(next_page.find_element_by_xpath("./a").get_attribute('href'))

            print("3. else finish process_request(): " + datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S.%f') + " -> " + url)

            response = HtmlResponse(url=url, body=source, request=request, encoding="utf-8")
            return response