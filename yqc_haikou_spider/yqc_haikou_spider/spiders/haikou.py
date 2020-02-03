# -*- coding: utf-8 -*-
import datetime
import time

import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from yqc_haikou_spider.items import YqcHaikouSpiderItem

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



class HaikouSpider(CrawlSpider):
    name = 'haikou'
    allowed_domains = ['haikou.gov.cn']
    start_urls = [
        'http://www.haikou.gov.cn/xxgk/szfbjxxgk/zcfg/bmgfxwj/']

    rules = (
        Rule(LinkExtractor(allow=r'.*haikou.gov.cn/xxgk/szfbjxxgk/zcfg/bmgfxwj.*'),
             callback='parse_page',
             follow=False),
    )

    cont_dict = {}

    def parse_item(self, response):
        print("5. parse_item(): " + datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S.%f') + " -> " + response.url)
        title = response.xpath("/html/body/div[3]/div/div[1]/div[2]/h1/text()").get()
        cont = response.xpath("//*[@id='zl_Articel']").get()
        index_id = str('_NULL')
        pub_org = str('_NULL')

        pub_time = response.xpath("/html/body/div[3]/div/div[1]/div[2]/div[1]/div[3]/div[2]/text()").get()
        doc_id = str('_NULL')
        region = str('海口')
        update_time = datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")

        if not title:
            return

        print("\t" + title)
        for key in keys:
            if key in title:
                self.dict_add_one(re.sub('[\s+]', ' ', title), response.url, re.sub('[\s+]', ' ', cont),
                                  re.sub('[\s+]', ' ', pub_time), pub_org, index_id, doc_id, region, update_time)

        item = YqcHaikouSpiderItem(cont_dict=self.cont_dict)

        yield item

    def dict_add_one(self, title, url, cont, pub_time, pub_org, index_id, doc_id, region, update_time):
        time.sleep(0.3)
        if title in self.cont_dict:
            self.cont_dict[title]['key_cnt'] += 1
        else:
            cnt_dict = {'key_cnt': 1, 'title': title, 'url': url, 'cont': cont, 'pub_time': pub_time,
                        'pub_org': pub_org, 'index_id': index_id, 'doc_id': doc_id, 'region': region,
                        'update_time': update_time}

            self.cont_dict[title] = cnt_dict

    def parse_page(self, response):
        url = response.url

        print("4. parse_page(): " + datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S.%f') + " -> " + url)

        url_prefix = 'http://service.haikou.gov.cn/xingzhengwendangku/'

        if str('REPORT_NDOC_006051') in url or str('REPORT_NDOC_006010') in url:
            print("\t>>> debug: " + url)

        if str('currentPage') in url:
            tr_list = response.xpath("//*[@id='main']/div[1]/div/div[2]/table/tbody//tr")

            for tr in tr_list:
                # print(tr)
                url = tr.xpath("./td[1]/a/@href").get()
                full_url = url_prefix + url

                yield scrapy.Request(full_url, callback=self.parse_item)

        else:
            if str('REPORT_NDOC_006051') in url or str('REPORT_NDOC_006010') in url:
                print('\t>>> no currentPage')

            title = response.xpath("/html/body/div[3]/div/div[1]/div[2]/h1/text()").get()
            cont = response.xpath("//*[@id='zl_Articel']").get()
            index_id = str('_NULL')
            pub_org = str('_NULL')

            pub_time = response.xpath("/html/body/div[3]/div/div[1]/div[2]/div[1]/div[3]/div[2]/text()").get()
            doc_id = str('_NULL')
            region = str('海口')
            update_time = datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")

            if not title:
                return

            print("\t" + title)
            for key in keys:
                if key in title:
                    self.dict_add_one(re.sub('[\s+]', ' ', title), response.url, re.sub('[\s+]', ' ', cont),
                                      re.sub('[\s+]', ' ', pub_time), pub_org, index_id, doc_id, region, update_time)

            item = YqcHaikouSpiderItem(cont_dict=self.cont_dict)

            print("6. parse_page(): " + datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S.%f') + " -> " + url)

            yield item