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

import scrapy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class YqcShanghaiSpiderDownloaderMiddleware(object):
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r"/home/james/_AllDocMap/06_Software/chromedriver")
        # self.driver = webdriver.Chrome(executable_path=r"/Users/qjiang/install/chromedriver")

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
                "//*[@id='main']/div[1]/div/div[2]/nav/ul/li[position()=last()-1]")
            url = str(next_page.find_element_by_xpath("./a").get_attribute('href'))

            print("3. else finish process_request(): " + datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S.%f') + " -> " + url)

            response = HtmlResponse(url=url, body=source, request=request, encoding="utf-8")
            return response
