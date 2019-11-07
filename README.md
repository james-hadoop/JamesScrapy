### start.py
# encoding: utf-8

from scrapy import cmdline

cmdline.execute("scrapy crawl bmw5".split())

### User-Agent
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}

### mysql table
drop table jianshu_article;

CREATE TABLE `jianshu_article` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `content` longtext DEFAULT NULL,
  `author` varchar(255) DEFAULT NULL,
  `pub_time` datetime DEFAULT NULL,
  `article_id` varchar(30) DEFAULT NULL,
  `origin_url` varchar(255) DEFAULT NULL,
  KEY `index_id` (`id`),
  KEY `index_title` (`title`),
  KEY `index_author` (`author`),
  KEY `index_pub_time` (`pub_time`)
) DEFAULT CHARSET=utf8 COMMENT='james__简书爬虫数据';