from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from tutorial.items import GenericItem

import simhash

class FtdSpider(CrawlSpider):
    name = 'ftd'
    allowed_domains = ['www.ftd.de']
    start_urls = ['http://www.ftd.de']
    rules = (
        # Sites which should be saved
        Rule(
            SgmlLinkExtractor(allow='/[\d]+.html(\?page\=\d)?$'),
            callback='parse_page',
            follow=True
        ),

        # Sites which should be followed, but not saved
        Rule(SgmlLinkExtractor(
            allow='(thema|unternehmen|finanzen|politik|karriere|it-medien|sport|auto|luxus|panorama)[\/\w-]*$')
        ),
    )

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        body = ''.join(hxs.select('//p[@class="paragraph"]//text()').extract()).strip()

        item = GenericItem()
        item['body'] = body
        item['url'] = response.url
        item['simhash'] = str(simhash.hash(body))
        return item
