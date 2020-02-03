# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from twisted.enterprise import adbapi
from pymysql import cursors
import time

class YqcHaikouSpiderPipeline(object):
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

        self.titleSet = set()

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
               insert into yqc_spider_haikou(id, title, url, pub_time, pub_org, doc_id, index_id, key_cnt, region, update_time, cont) values (null, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        time.sleep(0.3)
        defer = self.dbpool.runInteraction(self.insert_item, item)

        defer.addErrback(self.handle_error, item, spider)

    def insert_item(self, cursor, item):
        cont_dict = item['cont_dict']

        for v in cont_dict.values():
            if v['title'] not in self.titleSet:
                cursor.execute(self.sql, (
                    v['title'], v['url'], v['pub_time'], v['pub_org'], v['doc_id'], v['index_id'],
                    v['key_cnt'], v['region'], v['update_time'], v['cont']))

                self.titleSet.add(v['title'])

    def handle_error(self, error, item, spider):
        logging.error('-' * 10 + ' error ' + ' ' * 10)
        logging.error(error)
        logging.error('-' * 10 + ' error ' + ' ' * 10)