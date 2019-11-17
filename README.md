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


### web driver
https://github.com/mozilla/geckodriver/releases/tag/v0.26.0
https://sites.google.com/a/chromium.org/chromedriver/downloads
https://webkit.org/downloads/

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

CREATE TABLE `yqc_shenzhen` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL comment '标题',
  `url` varchar(255) DEFAULT NULL comment '标题',
  `pub_time` datetime DEFAULT NULL comment '发布时间',
  `pub_org` varchar(50) DEFAULT NULL comment '发布机构',
  `doc_id` varchar(100) DEFAULT NULL comment '文号',
  `index_id` varchar(100) DEFAULT NULL comment '索引号',
  `key_cnt` int(11) default 0 comment '关键字匹配数',
  `cont` longtext DEFAULT NULL comment '内容',
  KEY `index_id` (`id`),
  KEY `index_title` (`title`),
  KEY `index_pub_org` (`pub_org`),
  KEY `index_pub_time` (`pub_time`)
) DEFAULT CHARSET=utf8 COMMENT='james__yqc_shenzhen爬虫数据';


