# -*- coding: utf-8 -*-
import datetime
import time

import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from yqc_shanghai_spider.items import YqcShanghaiSpiderItem

keys = ['创新',
        '创业',
        '改革',
        '促进',
        '发展',
        '措施',
        '进一步',
        '扩大',
        '培育',
        '工作方案',
        '行动计划',
        '专项资金',
        '鼓励',
        '扶持',
        '加快',
        '管理',
        '推动',
        '激发',
        '实施',
        '推广',
        '产业',
        '推进',
        '加强',
        '改进',
        '提升',
        '规划',
        '落实',
        '政策',
        '征集',
        '建设',
        '构建',
        '行动方案',
        '实现',
        '开展',
        '开放',
        '总体方案',
        '投资',
        '补贴',
        '申报',
        '征收',
        '引导基金',
        '资助',
        '降低',
        '深化',
        '科技']

count = 1


class ShanghaiSpider(CrawlSpider):
    name = 'shanghai'
    allowed_domains = ['shanghai.gov.cn']
    # start_urls = ['http://service.shanghai.gov.cn/xingzhengwendangku/XZGFList.aspx']
    start_urls = [
        'http://service.shanghai.gov.cn/xingzhengwendangku/XZGFList.aspx?testpara=0&kw=&issueDate_userprop8=&status=0&departid=&wenhao=&issueDate_userprop8_end=&excuteDate=&excuteDate_end=&closeDate=&closeDate_end=&departtypename=&typename=&zhutitypename=&zhuti=&currentPage=1&pagesize=10']

    rules = (
        Rule(LinkExtractor(allow=r'.*xingzhengwendangku.*'),
             callback='parse_page',
             follow=False),
    )

    cont_dict = {}

    def parse_item(self, response):
        print("5. parse_item(): " + time.strftime('%Y-%m-%d %H:%M:%S',
                                                  time.localtime()) + "\n" + response.url)
        title = response.xpath("//*[@id='main']/div[1]/div/div[1]/div[1]/dl/dd/text()").get()
        cont = response.xpath("//*[@id='ivs_content']").get()
        index_id = str('_NULL')
        pub_org = response.xpath("//*[@id='main']/div[1]/div/div[1]/div[2]/dl[1]/dd/text()").get()

        pub_time = response.xpath("//*[@id='main']/div[1]/div/div[1]/div[3]/dl[1]/dd/text()").get()
        doc_id = response.xpath("//*[@id='main']/div[1]/div/div[1]/div[2]/dl[1]/dd/text()").get()
        region = str('上海')
        update_time = datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")

        print(title)

        # self.log(cont, level=logging.INFO)

        if not title:
            return

        for key in keys:
            if key in title:
                self.dict_add_one(re.sub('[\s+]', ' ', title), response.url, re.sub('[\s+]', ' ', cont),
                                  re.sub('[\s+]', ' ', pub_time), pub_org, index_id, doc_id, region, update_time)

        item = YqcShanghaiSpiderItem(cont_dict=self.cont_dict)

        return item

    def dict_add_one(self, title, url, cont, pub_time, pub_org, index_id, doc_id, region, update_time):
        if title in self.cont_dict:
            self.cont_dict[title]['key_cnt'] += 1
        else:
            cnt_dict = {'key_cnt': 1, 'title': title, 'url': url, 'cont': cont, 'pub_time': pub_time,
                        'pub_org': pub_org, 'index_id': index_id, 'doc_id': doc_id, 'region': region,
                        'update_time': update_time}

            self.cont_dict[title] = cnt_dict

    def parse_page(self, response):
        url_prefix = 'http://service.shanghai.gov.cn/xingzhengwendangku/'

        global count
        count += 1

        tr_list = response.xpath("//*[@id='main']/div[1]/div/div[2]/table/tbody//tr")
        # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) +tr_list)

        for tr in tr_list:
            # print(tr)
            url = tr.xpath("./td[1]/a/@href").get()
            full_url = url_prefix + url
            print("4. parse_page(): " + time.strftime('%Y-%m-%d %H:%M:%S',
                                                      time.localtime()) + "\n" + response.url + "\n\t" + full_url)

            yield scrapy.Request(full_url, callback=self.parse_item)

    # def process_spider_input(self, response):
