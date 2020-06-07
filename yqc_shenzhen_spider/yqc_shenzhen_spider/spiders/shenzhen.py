# -*- coding: utf-8 -*-
import re
import datetime
import time

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from yqc_shenzhen_spider.items import YqcShenzhenSpiderItem

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


class ShenzhenSpider(CrawlSpider):
    name = 'shenzhen'
    allowed_domains = ['sz.gov.cn']
    start_urls = ['http://www.sz.gov.cn/cn/xxgk/zfxxgj/zfwj/index.html']

    rules = (
        Rule(LinkExtractor(allow=r'.*szfwj.*'), callback='parse_item', follow=False),
    )

    cont_dict = {}

    def parse_item(self, response):
        print("5. parse_item(): " + datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S.%f') + " -> " + response.url)
        title = response.xpath("//div[@class='tit']/h1/text()").get()
        cont = response.xpath("//div[@class='news_cont_d_wrap']").get()
        index_id = response.xpath("//div[@class='xx_con']/p[1]/text()").get()
        pub_org = response.xpath("//div[@class='xx_con']/p[3]/text()").get()
        pub_time = response.xpath("//div[@class='xx_con']/p[4]/text()").get()
        doc_id = response.xpath("//div[@class='xx_con']/p[6]/text()").get()
        region = str('深圳')
        update_time = datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")

        if not title:
            return

        for key in keys:
            if key in title:
                self.dict_add_one(title, response.url, re.sub('[\s+]', ' ', cont), pub_time, pub_org, index_id, doc_id, region, update_time, key)

        print("\t>>> " + title)

        item = YqcShenzhenSpiderItem(cont_dict=self.cont_dict)

        # print('>>>>')
        # print(index_id)
        # print(self.cont_dict)
        # print(self.cont_dict.__len__())

        return item

    def dict_add_one(self, title, url, cont, pub_time, pub_org, index_id, doc_id, region, update_time, doc_key):
        time.sleep(0.3)
        if title in self.cont_dict:
            self.cont_dict[title]['key_cnt'] += 1
            self.cont_dict[title]['doc_key'] = self.cont_dict[title]['doc_key'] + ',' + doc_key
        else:
            cnt_dict = {'key_cnt': 1, 'title': title, 'url': url, 'cont': cont, 'pub_time': pub_time,
                        'pub_org': pub_org, 'index_id': index_id, 'doc_id': doc_id, 'region': region,
                        'update_time': update_time, 'doc_key': doc_key}

            self.cont_dict[title] = cnt_dict