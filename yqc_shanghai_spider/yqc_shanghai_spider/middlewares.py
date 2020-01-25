# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from telnetlib import EC

from scrapy import signals
from selenium import webdriver
import time
from scrapy.http.response.html import HtmlResponse
import logging

import scrapy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class YqcShanghaiSpiderDownloaderMiddleware(object):
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r"/home/james/_AllDocMap/06_Software/chromedriver")
        # self.driver = webdriver.Chrome(executable_path=r"/Users/qjiang/install/chromedriver")

    def process_request(self, request, spider):
        print("1. process_request(): " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + " ->\n\t" + request.url)
        self.driver.get(request.url)

        # print("2. process_request(): " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + " -> \n" + self.driver.page_source)

        # last_page = self.driver.find_element_by_xpath("//li[@class='hidden-xs pagination_index_last']")

        next_page = None
        try:
            next_page = self.driver.find_element_by_xpath(
                "//*[@id='main']/div[1]/div/div[2]/nav/ul/li[position()=last()-1]")
        except:
            pass

        if next_page is not None:
            # print("\t>>>| %s |" % next_page.text)
            url = str(next_page.find_element_by_xpath("./a").get_attribute('href'))
            # print("\t>>>| %s |" % str(next_page.find_element_by_xpath("./a").get_attribute('href')))

            time.sleep(2)

            source = self.driver.page_source

            response = HtmlResponse(url=url, body=source, request=request, encoding="utf-8")

            print("3. finish process_request(): " + time.strftime('%Y-%m-%d %H:%M:%S',
                                                                  time.localtime()) + " next_page is NOT None!!!\n\t" + request.url)
            return response
        else:
            print("3. finish process_request(): " + time.strftime('%Y-%m-%d %H:%M:%S',
                                                                  time.localtime()) + " next_page is None!!!\n\t" + request.url)
            response = HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, request=request,
                                    encoding="utf-8")
            return response
