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
        # self.driver = webdriver.Chrome(executable_path=r"/home/james/_AllDocMap/06_Software/chromedriver")
        self.driver = webdriver.Chrome(executable_path=r"/Users/qjiang/install/chromedriver")

    def process_request(self, request, spider):
        url = request.url
        source = self.driver.page_source

        print(
            "1. process_request(): " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') + " -> " + request.url)
        self.driver.get(request.url)

        # print("2. process_request(): " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') + " -> \n" + self.driver.page_source)

        # last_page = self.driver.find_element_by_xpath("//li[@class='hidden-xs pagination_index_last']")

        next_page = None
        try:
            next_page = self.driver.find_element_by_xpath(
                "//*[@id='main']/div[1]/div/div[2]/nav/ul/li[position()=last()-1]")
        except Exception as e:
            print("\t>>> except: " + self.driver.current_url)
            print("\n\t<<< " + str(e))
        finally:
            if next_page is not None:
                url = str(next_page.find_element_by_xpath("./a").get_attribute('href'))
            else:
                url = self.driver.current_url

            time.sleep(0.5)
            response = HtmlResponse(url=url, body=self.driver.page_source, request=request, encoding="utf-8")
            # print(next_page)
            print(next_page is not None)
            # print(url)
            # print(self.driver.page_source)

            print("3. finish process_request(): " + datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S.%f') + "\n\t" + url)
            if str('REPORT_NDOC_006051') in url or str('REPORT_NDOC_006010') in url:
                print(">>> debug: " + url)
                print(">>> debug: " + request.url)
                print(">>> debug: " + response.url)
                print(self.driver.page_source)
            # self.driver.quit()
            return response
