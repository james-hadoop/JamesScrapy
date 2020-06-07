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


class SuzhouSpider(CrawlSpider):
    name = 'suzhou'
    allowed_domains = ['suzhou.gov.cn']
    start_urls = [
        'http://www.suzhou.gov.cn/szxxgk/front/xxgk_right.jsp?sitecode=szsrmzf&channel_id=dc1a3f5691e541108d5a18bdd028949b']
    # start_urls = ['http://www.suzhou.gov.cn/']

    rules = (
        Rule(LinkExtractor(allow=r'.*zfwj/202002.*'), callback='parse_item', follow=False),
    )

    cont_dict = {}

    def parse_item(self, response):
        print("5. parse_item(): " + datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S.%f') + " -> " + response.url)
        title = response.xpath("//table[@class='xxgk_content_info1']/tbody/tr[3]/td[2]/text()").get()
        cont = response.xpath("//div[@class='content']").get()
        index_id = response.xpath("//table[@class='xxgk_content_info1']/tbody/tr[1]/td[2]/text()").get()
        pub_org = response.xpath("//table[@class='xxgk_content_info1']/tbody/tr[2]/td[2]/text()").get()
        pub_time = response.xpath("//table[@class='xxgk_content_info1']/tbody/tr[2]/td[4]/text()").get()
        doc_id = response.xpath("//table[@class='xxgk_content_info1']/tbody/tr[3]/td[4]/text()").get()
        region = str('苏州')
        update_time = datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")

        if not title:
            return

        print("\t>>> " + title)
        for key in keys:
            if key in title:
                self.dict_add_one(re.sub('[\s+]', ' ', title), response.url, re.sub('[\s+]', ' ', cont),
                                  re.sub('[\s+]', ' ', pub_time), re.sub('[\s+]', ' ', pub_org),
                                  re.sub('[\s+]', ' ', index_id), re.sub('[\s+]', ' ', doc_id),
                                  region, update_time, key)

        item = YqcSuzhouSpiderItem(cont_dict=self.cont_dict)

        yield item

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
