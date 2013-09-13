from __future__ import division

import sys
import sqlite3
import simhash

# settings for simhash
num_tables = 6
diff_bits = 3

corpus = simhash.Corpus(num_tables, diff_bits)

# first arg is path to db
db = sys.argv[1]
con = sqlite3.connect(db)
c = con.cursor()

c.execute("SELECT count(simhash), simhash, url FROM data WHERE simhash IS NOT NULL GROUP BY simhash")
results = c.fetchall()

# insert hashes into corpus
total_count = 0
for row in results:
	corpus.insert(int(row[1]))
	total_count += row[0]

# query corpus
unique_count = 0
for row in results:
	r = corpus.find_all(int(row[1]))
	num_similar = len(set(r))+(row[0]-1)
	if num_similar <= 1:
		unique_count += 1

print (1-(unique_count/total_count))

