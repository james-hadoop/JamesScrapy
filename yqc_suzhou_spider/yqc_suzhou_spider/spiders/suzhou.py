# -*- coding: utf-8 -*-
import re
import datetime

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from yqc_suzhou_spider.items import YqcSuzhouSpiderItem

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
        '实施方案',
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
        '深化']


class SuzhouSpider(CrawlSpider):
    name = 'suzhou'
    allowed_domains = ['suzhou.gov.cn']
    start_urls = ['http://www.suzhou.gov.cn/xxgk/zdgcjsxmssjz/sbj_11124/']

    rules = (
        Rule(LinkExtractor(allow=r'.*suzhou.gov.cn/xxgk/zdgcjsxmssjz.*'), callback='parse_item', follow=False),
    )

    cont_dict = {}

    def parse_item(self, response):
        title = response.xpath("//div[@class='con2 clearfix']/h1/text()").get()
        cont = response.xpath("//div[@class='TRS_Editor']").get()
        index_id = "_NULL"
        pub_org = response.xpath("//div[@class='con2 clearfix']/h4/text()").get()
        pub_time = response.xpath("//div[@class='con2 clearfix']/h4/text()").get()
        doc_id = "_NULL"
        region = str('苏州')
        update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(str(">>> ") + str(title) + str(pub_time))

        if not title:
            return

        if not '2019' in pub_time:
            return

        for key in keys:
            if key in title:
                self.dict_add_one(re.sub('[\s+]', ' ', title), response.url, re.sub('[\s+]', ' ', cont),
                                  re.sub('[\s+]', ' ', pub_time), pub_org, index_id, doc_id, region, update_time)

        item = YqcSuzhouSpiderItem(cont_dict=self.cont_dict)

        # print('>>>>')
        # print(index_id)
        # print(self.cont_dict)
        # print(self.cont_dict.__len__())

        return item

    def dict_add_one(self, title, url, cont, pub_time, pub_org, index_id, doc_id, region, update_time):
        if title in self.cont_dict:
            self.cont_dict[title]['key_cnt'] += 1
        else:
            cnt_dict = {'key_cnt': 1, 'title': title, 'url': url, 'cont': cont, 'pub_time': pub_time,
                        'pub_org': pub_org, 'index_id': index_id, 'doc_id': doc_id, 'region': region,
                        'update_time': update_time}

            self.cont_dict[title] = cnt_dict
