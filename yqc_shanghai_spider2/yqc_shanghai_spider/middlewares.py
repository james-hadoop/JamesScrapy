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
import os

import scrapy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class YqcShanghaiSpiderDownloaderMiddleware(object):

    def __init__(self):
        os_info = os.uname()
        if os_info.sysname == 'Darwin':
            chrome_path = r"/Users/qjiang/install/chromedriver"
        else:
            chrome_path = r"/home/james/_AllDocMap/06_Software/chromedriver"
        self.driver = webdriver.Chrome(executable_path=chrome_path)
        self.count = 2

    def process_request(self, request, spider):
        if(self.count<0):
            return
        self.count += 1
        print(">>> process_request(): " + str(request.url))
        self.driver.get(request.url)

        # last_page = self.driver.find_element_by_xpath("//li[@class='hidden-xs pagination_index_last']")

        next_page = None
        try:
            next_page = self.driver.find_element_by_xpath(
                "//*[@id='pageList']/div/ul/li[@class='action']")

        except:
            pass

        if next_page is not None:
            print("=>| %s |" % next_page.text)
            url = str(next_page.find_element_by_xpath("./a").get_attribute('href'))
            title = str(next_page.find_element_by_xpath("./a").get_attribute('title'))
            print("\ttitle=>| %s |" % title)
            print("=>| %s |" % url)

            time.sleep(2)

            source = self.driver.page_source
            response = HtmlResponse(url=url, body=source, request=request, encoding="utf-8")

            return response
