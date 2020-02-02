# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from selenium import webdriver
import datetime
from scrapy.http.response.html import HtmlResponse


class YqcHangzhouSpiderDownloaderMiddleware(object):
    def __init__(self):
        # self.driver = webdriver.Chrome(executable_path=r"/home/james/_AllDocMap/06_Software/chromedriver")
        self.driver = webdriver.Chrome(executable_path=r"/Users/qjiang/install/chromedriver")

    def process_request(self, request, spider):
        url = request.url
        print(
            "1. process_request(): " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') + " -> " + url)
        self.driver.get(url)
        source = self.driver.page_source

        print("3. finish process_request(): " + datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S.%f') + " -> " + url)
        response = HtmlResponse(url=url, body=source, request=request, encoding="utf-8")
        return response

        # a_list=self.driver.find_elements_by_xpath("//*[@id='div1345230']/table/tbody/tr/td/table[2]/tbody/tr/td[2]/a")
        # for a in a_list:
        #     url = a.xpath("./a/@href").get()

