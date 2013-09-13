scrapy-german-news
==================

Scrapy project with spiders to extract article content from the following
german news sites:

    * spiegel.de
    * stern.de
    * faz.net
    * zeit.de
    * ftd.de

To get a list of all provided spiders:

    scrapy list

To start a spider:

    scrapy crawl stern -s JOBDIR=crawls/stern

== Similarity ==

The simhash value is generated for every extracted article text.
By using the similarity.py script, the similarity of all downloaded content
can be computed.

Example:

    python similarity.py crawls/stern/data.sqlite
    0.327760236037

The value is the similarity in percent. In the example above the downloaded 
content has a 32% similarity.

== Database ==

The content is stored in a Sqlite database called 'data.sqlite'. 
The 'data'-table has the following columns:

    * url - the downloaded url
    * body - the extracted article content
    * crawl\_time - time of crawl
    * simhash - the generated simhash of the article content

If during a crawl you want to check how many sites have been crawled do the following:

    sqlite crawls/stern/data.sqlite
    select count(url) from data;

Execute this to get the top 10 sites with the same simhash (e.g. sites which are 100% similar):

    select simhash, count(simhash) from data group by simhash order by count(simhash) DESC limit 10;

