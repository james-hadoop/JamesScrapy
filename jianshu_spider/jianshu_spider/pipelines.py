# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors


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
        self.cursor.execute(self.sql, (
            item['title'], item['content'], item['author'], item['pub_time'], item['origin_url'],
            item['article_id']))
        self.conn.commit()

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into jianshu_article(id, title,content,author,pub_time,origin_url,article_id) values (null,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql


class JianShuTwistedPipeline(object):
    def __init__(self):
        dbparams = {'host': 'localhost',
                    'port': 3306,
                    'user': 'developer',
                    'password': 'developer',
                    'database': 'developer',
                    'charset': 'utf8',
                    'cursorclass': cursors.DictCursor
                    }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into jianshu_article(id, title,content,author,pub_time,origin_url,article_id,read_count,like_count,word_count) values (null,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item, item)
        defer.addErrback(self.handle_error, item, spider)

    def insert_item(self, cursor, item):
        cursor.execute(self.sql, (
            item['title'], item['content'], item['author'], item['pub_time'], item['origin_url'],
            item['article_id'], item['read_count'], item['like_count'], item['word_count']))

    def handle_error(self, error, item, spider):
        print('=' * 10 + 'error' + '=' * 10)
        print(error)
        print('=' * 10 + 'error' + '=' * 10)
