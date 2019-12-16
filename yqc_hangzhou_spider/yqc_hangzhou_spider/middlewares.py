# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from selenium import webdriver
import time
from scrapy.http.response.html import HtmlResponse


class YqcHangzhouSpiderDownloaderMiddleware(object):
    def __init__(self):
        # self.driver = webdriver.Chrome(executable_path=r"/home/james/_AllDocMap/06_Software/chromedriver")
        self.driver = webdriver.Chrome(executable_path=r"/Users/qjiang/install/chromedriver")

    def process_request(self, request, spider):
        print(">>> process_request(): " + str(request.url))
        self.driver.get(request.url)

        # last_page = self.driver.find_element_by_xpath("//li[@class='hidden-xs pagination_index_last']")

        next_page = None
        try:
            next_page = self.driver.find_element_by_xpath(
                "//*[@class='btn_page']/text()")

            # // *[ @ id = "currpage"]
            # //*[@id="div1345230"]/table/tbody/tr/td/table[2]/tbody/tr/td[3]/table/tbody/tr/td[4]/input
        except:
            pass

        if next_page is not None:
            print("=>| %s |" % next_page.text)
            url = str(next_page.find_element_by_xpath("./a").get_attribute('href'))
            print("=>| %s |" % str(next_page.find_element_by_xpath("./a").get_attribute('href')))

            time.sleep(2)

            source = self.driver.page_source
            response = HtmlResponse(url=url, body=source, request=request, encoding="utf-8")

            return response
