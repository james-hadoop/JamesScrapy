# -*- coding: utf-8 -*-
import re
import datetime
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from yqc_beijing_spider.items import YqcBeijingSpiderItem

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


class BeijingSpider(CrawlSpider):
    name = 'beijing'
    allowed_domains = ['beijing.gov.cn']
    start_urls = ['http://www.beijing.gov.cn/zhengce/']

    rules = (
        Rule(LinkExtractor(allow=r'.*zhengcefagui.*'), callback='parse_item',
             follow=False),
    )

    cont_dict = {}

    def parse_item(self, response):
        print("5. parse_item(): " + datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S.%f') + " -> " + response.url)
        # title = response.xpath("//body/div[1]/div/h1/text()").get()
        title = response.xpath("//div[@class='header']/p/text()").get()
        # cont = response.xpath("//div[@class='TRS_Editor']").get()
        cont = response.xpath("//div[@class='view TRS_UEDITOR trs_paper_default trs_web']/p").get()
        index_id = ''
        # pub_org = response.xpath("//div[@class='xx_con']/p[3]/text()").get()
        pub_org = response.xpath("//div[@class='container']/ol/li[2]/span/text()").get()
        # pub_time = response.xpath("//body/div[1]/div/h4/text()").get()
        pub_time = response.xpath("//div[@class='container']/ol/li[8]/span/text()").get()
        # doc_id = response.xpath("//div[@class='xx_con']/p[6]/text()").get()
        doc_id = response.xpath("//div[@class='container']/ol/li[6]/span").get()
        region = str('北京')
        update_time = datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")

        if not title:
            return

        print("\t>>> " + title)
        for key in keys:
            if key in title:
                self.dict_add_one(re.sub('[\s+]', ' ', title), response.url, re.sub('[\s+]', ' ', cont),
                                  re.sub('[\s+]', ' ', pub_time), pub_org, index_id, doc_id, region, update_time)

        item = YqcBeijingSpiderItem(cont_dict=self.cont_dict)

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