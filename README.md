## Reference:
https://docs.scrapy.org/en/latest/topics/architecture.html


## start.py
```
# encoding: utf-8

from scrapy import cmdline

cmdline.execute("scrapy crawl shanghai".split())
```

## User-Agent
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}


## web driver
https://github.com/mozilla/geckodriver/releases/tag/v0.26.0
https://sites.google.com/a/chromium.org/chromedriver/downloads
https://webkit.org/downloads/

## mysql table
```
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

CREATE TABLE `yqc_spider` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL comment '标题',
  `url` varchar(255) DEFAULT NULL comment '标题',
  `pub_time` varchar(20) DEFAULT NULL comment '发布时间',
  `pub_org` varchar(50) DEFAULT NULL comment '发布机构',
  `doc_id` varchar(100) DEFAULT NULL comment '文号',
  `index_id` varchar(100) DEFAULT NULL comment '索引号',
  `key_cnt` int(11) default 0 comment '关键字匹配数',
  `region` varchar(30) default null comment '地区',
  `update_time` datetime not null comment '更新时间',
  `cont` longtext DEFAULT NULL comment '内容',
  KEY `index_id` (`id`),
  KEY `index_title` (`title`),
  KEY `index_pub_org` (`pub_org`),
  KEY `index_pub_time` (`pub_time`),
  KEY `index_region` (`region`),
  KEY `index_update_time` (`update_time`)
) DEFAULT CHARSET=utf8 COMMENT='james__yqc_爬虫数据';
```

## Query Result from Mysql Table
```
SELECT *
FROM
  (SELECT *
   FROM
     (SELECT min(title) title,
             min(url) url,
             min(pub_time) pub_time,
             min(pub_org) pub_org,
             min(doc_id) doc_id,
             min(index_id) index_id,
             min(key_cnt) key_cnt,  
             min(region),
             min(update_time) update_time
      FROM developer.yqc_spider_shanghai
      GROUP BY title,
               url,
               pub_time,
               pub_org,
               doc_id,
               index_id,
               key_cnt,
               region,
               update_time) t1
   WHERE update_time>'2019-12-22 00:00:00'
   UNION ALL SELECT *
   FROM
     (SELECT min(title) title,
             min(url) url,
             min(pub_time) pub_time,
             min(pub_org) pub_org,
             min(doc_id) doc_id,
             min(index_id) index_id,
             min(key_cnt) key_cnt,
             min(region),
             min(update_time) update_time
      FROM developer.yqc_spider
      GROUP BY title,
               url,
               pub_time,
               pub_org,
               doc_id,
               index_id,
               key_cnt,
               region,
               update_time) t2
   WHERE update_time>'2019-12-22 00:00:00') tt
ORDER BY key_cnt,
         pub_time DESC;
```