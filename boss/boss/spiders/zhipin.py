# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from boss.items import BossItem


class ZhipinSpider(CrawlSpider):
    name = 'zhipin'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/c101020100/?query=python&page=1&ka=page-1']

    rules = (
        Rule(LinkExtractor(allow=r'.+\?query=python&page=\d'), follow=True),
        Rule(LinkExtractor(allow=r'.+job_detail/\d+.html'), callback="parse_job", follow=False)
    )

    def parse_job(self, response):
        title = response.xpath("//h1[@class='name']/text()").strip()
        salary = response.xpath("//h1[@class='name]/span/text()").get().strip()
        job_info = response.xpath("//div[class='job-primary']/div[@class='info-primary']/p//text()").getall()
        city = job_info[0]
        work_years = job_info[1]
        education = job_info[2]
        company = response.xpath("//div[@class='info-company']//a/text()").get()
        item = BossItem(title=title, salary=salary, city=city, work_years=work_years, education=education,
                        company=company)

        yield item
