import os
import sqlite3

from scrapy import log
from scrapy.dupefilter import BaseDupeFilter
from scrapy.utils.job import job_dir
from scrapy.utils.request import request_fingerprint

class SqliteDupeFilter(BaseDupeFilter):
    """Sqlite duplicates filter"""

    def __init__(self, path):
        filename = os.path.join(path, 'seen.sqlite')
        self.conn = sqlite3.connect(filename, check_same_thread=False)
        q = "CREATE TABLE IF NOT EXISTS seen (fp text primary key)"
        self.conn.execute(q)
        self.conn.commit()
        
    def request_seen(self, request):
        fp = request_fingerprint(request)
        q = "INSERT INTO seen VALUES (?)"
        args = (fp,)
        try:
            self.conn.execute(q, args)
            self.conn.commit()
        except sqlite3.IntegrityError:
            return True

    @classmethod
    def from_settings(cls, settings):
        return cls(job_dir(settings))