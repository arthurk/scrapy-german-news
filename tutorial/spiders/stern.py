from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from tutorial.items import GenericItem

import simhash

class SternSpider(CrawlSpider):
    name = 'stern'
    allowed_domains = ['www.stern.de']
    start_urls = ['http://www.stern.de']
    cat_re = 'politik|panorama|sport|kultur|wirtschaft|auto|gesundheit|lifestyle|digital|wissen|reise'
    rules = (
        # Sites which should be saved
        Rule(SgmlLinkExtractor(allow='/(%s)[\/\w-]+\d+.html$' % cat_re), callback='parse_page', follow=True),

        # Sites which should be followed, but not saved
        Rule(SgmlLinkExtractor(allow='/(%s)/' % cat_re, deny='-print.html$')),
    )

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        body = ''.join(hxs.select('//span[@itemprop="articleBody"]//text()').extract()).strip()

        item = GenericItem()
        item['body'] = body
        item['url'] = response.url
        item['simhash'] = str(simhash.hash(body))
        return item
