# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import logging


class DoubanPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            # cursorclass=MySQLdb.cursors.DictCursor,
            charset='utf8',
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert_, item)
        query.addErrback(self.handle_error)
        return item

    def _conditional_insert_(self, tx, item):
        tx.execute('SELECT * FROM movie_top250 WHERE title="%s"' % item["title"])
        result = tx.fetchone()
        logging.warning(result)
        if result:
            logging.debug("Item already stored in db:%s" % item["title"])
        else:
            tx.execute('''INSERT INTO movie_top250 (title, score, movieInfo, quote)
                          VALUES ("%s", %s, "%s", "%s")''' % (item["title"], float(item["score"]), item['movieInfo'], item['quote']))
            logging.debug("Item stored in db: %s" % item["title"])

    def handle_error(self, e):
        logging.error(e)


