import sys
import sqlite3
import simhash

# first arg is path to db
db = sys.argv[1]

conn = sqlite3.connect(db)
c = conn.cursor()

for chunk in xrange(30):
    c.execute("SELECT url, body FROM data WHERE simhash IS NULL LIMIT 7000")
    rows = c.fetchall()
    for row in rows:
        url = row[0]
        body = row[1]
        c.execute('UPDATE data SET simhash=? WHERE url=?', (str(simhash.hash(body)), url))
        conn.commit()

conn.close()
