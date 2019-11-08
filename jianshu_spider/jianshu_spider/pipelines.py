# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class JianshuSpiderPipeline(object):
    def __init__(self):
        print('-' * 60)
        print('JianshuSpiderPipeline')
        print('-' * 60)
        dbparams = {'host': 'localhost',
                    'port': 3306,
                    'user': 'developer',
                    'password': 'developer',
                    'database': 'developer',
                    'charset': 'utf8'
                    }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        print('>>> called process_item()')
        print(self.sql)
        print('*' * 10)
        print(item['title'], item['content'], item['author'], item['pub_time'], item['origin_url'],
              item['article_id'])
        self.cursor.execute(self.sql, (
            item['title'], item['content'], item['author'], item['pub_time'], item['origin_url'],
            item['article_id']))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into jianshu_article(id, title,content,author,pub_time,origin_url,article_id) values (null,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql
