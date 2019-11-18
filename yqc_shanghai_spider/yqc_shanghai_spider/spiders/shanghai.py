# -*- coding: utf-8 -*-
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


class ShanghaiSpider(CrawlSpider):
    name = 'shanghai'
    allowed_domains = ['shanghai.gov.cn']
    start_urls = ['http://www.shanghai.gov.cn/nw2/nw2314/nw2319/nw12344/index.html']

    rules = (
        Rule(LinkExtractor(allow=r'.*http://www.shanghai.gov.cn/nw2/nw2314/nw2319/nw12344.*'), callback='parse_item', follow=False),
    )

    cont_dict = {}

    def parse_item(self, response):
        title = response.xpath("//div[@id='ivs_title']/text()").get()
        cont = response.xpath("//div[@id='ivs_content']/text()").get()
        index_id = str('_NULL')
        pub_org = str('_NULL')
        pub_time = response.xpath("//div[@id='ivs_date']/text()").get()
        doc_id = str('_NULL')

        print(title)

        if not title:
            return

        for key in keys:
            if key in title:
                self.dict_add_one(title, response.url, re.sub('[\s+]', ' ', cont), pub_time, pub_org, index_id, doc_id)

        item = YqcShanghaiSpiderItem(cont_dict=self.cont_dict)
        print('>>>>')
        print(self.cont_dict)

        return item

    def dict_add_one(self, title, url, cont, pub_time, pub_org, index_id, doc_id):
        if title in self.cont_dict:
            self.cont_dict[title]['key_cnt'] += 1
        else:
            cnt_dict = {'key_cnt': 1, 'title': title, 'url': url, 'cont': cont, 'pub_time': pub_time,
                        'pub_org': pub_org, 'index_id': index_id, 'doc_id': doc_id}

            self.cont_dict[title] = cnt_dict