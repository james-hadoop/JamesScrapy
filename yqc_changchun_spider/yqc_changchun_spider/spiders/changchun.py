# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import datetime
import time

import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from yqc_changchun_spider.items import YqcChangchunSpiderItem

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


class ChangchunSpider(CrawlSpider):
    name = 'changchun'
    allowed_domains = ['changchun.gov.cn']
    start_urls = ['http://www.changchun.gov.cn/zw_33994/']

    """
    http://www.changchun.gov.cn/zw_33994/zfwj/ytdd/201812/t20181203_1989028.html
    """
    rules = (
        Rule(LinkExtractor(allow=r'.*changchun.gov.cn/zw_33994/zfwj/sfbwj_108294.*'),
             callback='parse_page',
             follow=False),
    )

    cont_dict = {}

    def parse_item(self, response):
        print("5. parse_item(): " + datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S.%f') + " -> " + response.url)
        title = response.xpath("//*[@class='xyh_xxynrq']/h2/text()").get()
        cont = response.xpath("//*[@class='TRS_Editor']").get()
        index_id = str('_NULL')
        pub_org = str('长春市政府')

        pub_time = response.xpath("//*[@class='pages-date']/span/text()[1]").get()
        doc_id = response.xpath("//*[@class='xyh_xxynrq']/h3/text()").get()
        region = str('长春')
        update_time = datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")

        if not title:
            return

        print("\t>>> " + title)
        for key in keys:
            if key in title:
                self.dict_add_one(re.sub('[\s+]', ' ', title), response.url, re.sub('[\s+]', ' ', cont),
                                  re.sub('[\s+]', ' ', pub_time), re.sub('[\s+]', ' ', pub_org), index_id, doc_id,
                                  region, update_time, key)

        item = YqcChangchunSpiderItem(cont_dict=self.cont_dict)

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

    def parse_page(self, response):
        url = response.url

        print("4. parse_page(): " + datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S.%f') + " -> " + url)

        url_prefix = 'http://www.changchun.gov.cn/zw_33994/zfwj/zcjd/'

        if str('zcjd') in url:
            pass
            # tr_list = response.xpath("//*[@class='currency_ul']/li")
            #
            # for tr in tr_list:
            #     print(tr)
            #     url = tr.xpath("./a/@href").get()
            #     if str(url).startswith('.') and str(url).endswith('html'):
            #         full_url = url_prefix + url
            #         print("\t>>> " + url)
            #         yield scrapy.Request(full_url, callback=self.parse_item)
            #     else:
            #         pass

        else:
            title = response.xpath("//*[@class='xyh_xxynrq']/h2/text()").get()
            cont = response.xpath("//*[@class='TRS_Editor']").get()
            index_id = str('_NULL')
            pub_org = str('长春市政府')

            pub_time = response.xpath("//*[@class='pages-date']/span/text()[1]") .get()
            doc_id = response.xpath("//*[@class='xyh_xxynrq']/h3/text()").get()
            region = str('长春')
            update_time = datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")

            if not title:
                return

            print("\t>>> " + title)
            for key in keys:
                if key in title:
                    # print("\t>>> included")
                    self.dict_add_one(re.sub('[\s+]', ' ', title), response.url, re.sub('[\s+]', ' ', cont),
                                      re.sub('[\s+]', ' ', pub_time), pub_org, index_id, doc_id, region, update_time,
                                      key)

            item = YqcChangchunSpiderItem(cont_dict=self.cont_dict)

            print("6. parse_page(): " + datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S.%f') + " -> " + url)
            # print("\n")
            # print(item)

            yield item
