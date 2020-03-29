## Reference:
https://docs.scrapy.org/en/latest/topics/architecture.html


## Project Generator
```

scrapy startproject yqc_ningbo_spider && \
cd yqc_ningbo_spider && \
scrapy genspider -t crawl ningbo "ningbo.gov.cn" && \
cd ..


scrapy startproject yqc_qingdao_spider && \
cd yqc_qingdao_spider && \
scrapy genspider -t crawl qingdao "qingdao.gov.cn" && \
cd ..


scrapy startproject yqc_chongqing_spider && \
cd yqc_chongqing_spider && \
scrapy genspider -t crawl chongqing "chongqing.gov.cn" && \
cd ..


scrapy startproject yqc_haikou_spider && \
cd yqc_haikou_spider && \
scrapy genspider -t crawl haikou "haikou.gov.cn" && \
cd ..


scrapy startproject yqc_xiamen_spider && \
cd yqc_xiamen_spider && \
scrapy genspider -t crawl xiamen "xiamen.gov.cn" && \
cd ..

```


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
  (SELECT t_cont.*
   FROM
     (SELECT min(id) id,
             title
      FROM developer.yqc_spider
      GROUP BY title) t_id
   LEFT JOIN
     (SELECT id,
             title,
             url,
             pub_time,
             pub_org,
             doc_id,
             index_id,
             key_cnt,
             region,
             update_time
      FROM developer.yqc_spider
      WHERE update_time>'2020-02-13 00:00:00') t_cont ON t_id.id=t_cont.id) tt
WHERE title IS NOT NULL
ORDER BY region,
         key_cnt DESC;
```

## run in terminal
```
cd workspace4py/JamesScrapy/yqc_beijing_spider

cd ../yqc_beijing_spider/ && scrapy crawl beijing && \
cd ../yqc_chongqing_spider/ && scrapy crawl chongqing && \
cd ../yqc_haikou_spider/ && scrapy crawl haikou && \
cd ../yqc_ningbo_spider/ && scrapy crawl ningbo && \
cd ../yqc_shanghai_spider && scrapy crawl shanghai && \
cd ../yqc_shanghai_spider2 && scrapy crawl shanghai && \
cd ../yqc_shanghai_spider3 && scrapy crawl shanghai3 && \
cd ../yqc_shenzhen_spider && scrapy crawl shenzhen && \
cd ../yqc_xiamen_spider && scrapy crawl xiamen && \
cd ../yqc_suzhou_spider && scrapy crawl suzhou
```