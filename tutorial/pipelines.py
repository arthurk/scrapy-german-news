import os
import sqlite3

from scrapy import log
from scrapy.utils.job import job_dir

class SqlitePipeline(object):

    def __init__(self, path):
        filename = os.path.join(path, 'data.sqlite')
        self.conn = sqlite3.connect(filename, check_same_thread=False)
        q = "CREATE TABLE IF NOT EXISTS data (url text primary key, body text, crawl_time text, simhash text)"
        self.conn.execute(q)
        self.conn.commit()

    @classmethod
    def from_settings(cls, settings):
        return cls(path=job_dir(settings))

    def process_item(self, item, spider):
        q = "INSERT INTO data VALUES (?, ?, DATETIME('NOW'), ?)"
        args = (item['url'], item['body'], item['simhash'])
        try:
            self.conn.execute(q, args)
            self.conn.commit()
        except sqlite3.IntegrityError:
            log.msg('IntegrityError: %s' % item['url'])
        return item