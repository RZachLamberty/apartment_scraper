# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime
import logging
import psycopg2


logger = logging.getLogger('pg_pipeline')


class PostgresPipeline(object):
    def __init__(self, user='apartments', password='apartments',
                 dbname='apartments', host='localhost'):
        self.user = user
        self.password = password
        self.dbname = dbname
        self.host = host

    def open_spider(self, spider):
        self.conn = psycopg2.connect(
            user=self.user,
            dbname=self.dbname,
            host=self.host,
            password=self.password
        )

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        sql = """
            insert into raw_data ( title, city, url, price, bedrooms, maplink,
              longitude, latitude, updated_on, content, image_links,
               attributes, size, parsed_on )
            values ( %(title)s, %(city)s, %(url)s, %(price)s, %(bedrooms)s,
              %(maplink)s, %(longitude)s, %(latitude)s, %(updated_on)s,
              %(content)s, %(image_links)s, %(attributes)s, %(size)s,
              %(parsed_on)s );
        """
        item['parsed_on'] = datetime.datetime.now()

        with self.conn.cursor() as cur:
            logger.debug("attempting insert")
            cur.execute(sql, item)
            self.conn.commit()
            logger.debug("status: {}".format(self.conn.status))

        return item
