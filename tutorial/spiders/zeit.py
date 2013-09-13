from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from tutorial.items import GenericItem

import simhash

class ZeitSpider(CrawlSpider):
    name = 'zeit'
    allowed_domains = ['www.zeit.de']
    start_urls = ['http://www.zeit.de']
    rules = (
        # Sites which should be saved
        Rule(
            SgmlLinkExtractor(
                allow=('/(online|news|politik|wirtschaft|meinung|gesellschaft|kultur|wissen|digital|' \
                       'studium|campus|karriere|lebensart|reisen|mobilitaet|sport|auto)[\/\w-]+$',

                       '/\d{4}/\d{2}/[\w-]+(/seite-\d)?$'),
                deny=('(komplettansicht|weitere|index)$', '/schlagworte/')),
            callback='parse_page',
            follow=True
        ),

        # Sites which should be followed, but not saved
        Rule(SgmlLinkExtractor(allow='(schlagworte|index)', deny='suche/')),
    )

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        body = ''.join(hxs.select('//div[@class="article-body"]/p//text()').extract()).strip()

        item = GenericItem()
        item['body'] = body
        item['url'] = response.url
        item['simhash'] = str(simhash.hash(body))
        return item
