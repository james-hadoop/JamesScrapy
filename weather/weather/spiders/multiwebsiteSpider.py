# -*- coding: utf-8 -*-
import scrapy
from weather.items import WeatherItem
from scrapy.crawler import CrawlerProcess
import logging


class ShanghaiSpider(scrapy.Spider):
    name = 'shanghaiSpider'
    allowed_domains = ['www.tianqi.com/shanghai']
    cities = ['shanghai']
    start_urls = []

    for city in cities:
        start_urls.append('https://www.tianqi.com/' + city + '/')

    def parse(self, response):
        logging.warning('response=%s' % response)
        # print('----response=%s' % response)

        items = []
        item = WeatherItem()

        # f_temperature = response.xpath('//p[@class="now"]/text()')
        # item['f_temperature'] = f_temperature
        # print('----f_temperature=%s' % f_temperature)

        f_temperature = response.xpath('//p[@class="now"]/b/text()')
        f_temperature_unit = response.xpath('//p[@class="now"]/i/text()')
        item['f_temperature'] = f_temperature.extract()[0] + f_temperature_unit.extract()[0]
        print('----f_temperature=%s' % f_temperature)

        f_date = response.xpath('//dd[@class="week"]/text()')
        item['f_date'] = f_date.extract()[0]
        print('----f_date=%s' % f_date)

        f_city = response.xpath('//dd[@class="name"]/h2/text()')
        item['f_city'] = f_city.extract()[0]
        print('----f_city=%s' % f_city)

        items.append(item)

        return items


class ShenzhenSpider(scrapy.Spider):
    name = 'shenzhenSpider'
    allowed_domains = ['www.tianqi.com/shenzhen']
    cities = ['shenzhen']
    start_urls = []

    for city in cities:
        start_urls.append('https://www.tianqi.com/' + city + '/')

    def parse(self, response):
        logging.warning('response=%s' % response)
        # print('----response=%s' % response)

        items = []
        item = WeatherItem()

        # f_temperature = response.xpath('//p[@class="now"]/text()')
        # item['f_temperature'] = f_temperature
        # print('----f_temperature=%s' % f_temperature)

        f_temperature = response.xpath('//p[@class="now"]/b/text()')
        f_temperature_unit = response.xpath('//p[@class="now"]/i/text()')
        item['f_temperature'] = f_temperature.extract()[0] + f_temperature_unit.extract()[0]
        print('----f_temperature=%s' % f_temperature)

        f_date = response.xpath('//dd[@class="week"]/text()')
        item['f_date'] = f_date.extract()[0]
        print('----f_date=%s' % f_date)

        f_city = response.xpath('//dd[@class="name"]/h2/text()')
        item['f_city'] = f_city.extract()[0]
        print('----f_city=%s' % f_city)

        items.append(item)

        return items


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess()
    process.crawl(ShanghaiSpider)
    process.crawl(ShenzhenSpider)
    process.start()
