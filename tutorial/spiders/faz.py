from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from tutorial.items import GenericItem

import simhash

class FazSpider(CrawlSpider):
    name = 'faz'
    allowed_domains = ['www.faz.net']
    start_urls = ['http://www.faz.net']
    rules = (
        # Sites which should be saved
        Rule(
            SgmlLinkExtractor(allow='(aktuell|themenarchiv)/[\/\w.-]+\-[0-9]+\.html$'),
            callback='parse_page',
            follow=True
        ),

        # Sites which should be followed, but not saved
        Rule(SgmlLinkExtractor(allow='(aktuell|thema|themenarchiv)/[\/\w.-]+(/|s[\d]+.html)$')),
    )

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        body = ''
        body += ''.join(hxs.select('//h1[@itemprop="headline"]//text()').extract()).strip() + '\n'
        body += ''.join(hxs.select('//p[@itemprop="description"]/text()').extract()).strip() + '\n'
        body += ''.join(hxs.select('//div[@itemprop="articleBody"]/p/text()').extract()).strip()

        item = GenericItem()
        item['body'] = body
        item['url'] = response.url
        item['simhash'] = str(simhash.hash(body))
        return item
