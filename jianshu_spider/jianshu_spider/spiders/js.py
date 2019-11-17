# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from jianshu_spider.items import ArticleItem


class JsSpider(CrawlSpider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    start_urls = ['http://jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=False),
    )

    def parse_detail(self, response):
        title = response.xpath("//h1[@class='_1RuRku']/text()").get()
        content = response.xpath("//div[@class='_2rhmJa']").get()
        url = response.url
        url1 = url.split("?")[0]
        article_id = url1.split('/')[-1]
        origin_url = response.url
        author = response.xpath("//div[1]/div/div/section[1]/div[1]/div/div/div[1]/span/a/text()").get()
        avatar = response.xpath("//a[@class='_1OhGeD']/img/@src").get()
        pub_time = response.xpath("//div[@class='s-dsoj']/time/text()").get()

        word_count = response.xpath("//div[@class='s-dsoj']/span[2]/text()").get()
        read_count = response.xpath("//div[@class='s-dsoj']/span[3]/text()").get()
        like_count = response.xpath("//div[@class='_3U4Smb']/div[@class='s-dsoj']/span[1]/span/text()").get()

        # subjects = ",".join(response.xpath("/div[@class='include-collection]/a/div/text()").getall())

        print(title)
        print(pub_time)
        print(word_count)
        print(like_count)

        item = ArticleItem(
            title=title,
            content=content,
            author=author,
            avatar=avatar,
            pub_time=pub_time,
            origin_url=origin_url,
            article_id=article_id,
            read_count=read_count,
            like_count=like_count,
            word_count=word_count
        )

        yield item
