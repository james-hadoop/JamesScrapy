# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import time
import logging


class WeatherPipeline(object):
    def process_item(self, item, spider):
        today = time.strftime('%Y%m%d', time.localtime())
        logging.warning('today=%s' % today)

        fileName = today + '.txt'
        with open(fileName, 'a') as fp:
            fp.write(item["f_date"] + ',')
            print('****f_date=%s' % item["f_date"] + ',')
            fp.write(item['f_city'] + ',')
            print('****f_city=%s' % item["f_city"] + ',')
            fp.write(item['f_temperature'] + '\n')
            print('****f_temperature=%s' % item["f_temperature"] + '\n\n')

        return item
