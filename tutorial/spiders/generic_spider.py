from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy import log

import simhash

from tutorial.items import GenericItem

class GenericSpider(CrawlSpider):
    name = "generic"

    rules = (
        # specific for golem.de -- remove for other sites
        #Rule(SgmlLinkExtractor(allow=('news\/',)), callback='parse_page', follow=True),
        Rule(SgmlLinkExtractor(), callback='parse_page', follow=True),
    )

    def __init__(self, url, *a, **kw):
        super(GenericSpider, self).__init__(*a, **kw)
        self.url = url
        self.start_urls = [url,]
        self.allowed_domains = [url.split('http://')[1]]
        
    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)

        item = GenericItem()
        #text = hxs.select('//div[@class="formatted"]/p//text()').extract()
        #item['body'] = "".join(text).strip()
        item['body'] = response.body_as_unicode()
        item['url'] = response.url

        return item

class SpiegelSpider(CrawlSpider):
    name = 'spiegel'
    allowed_domains = ['www.spiegel.de']
    start_urls = ['http://www.spiegel.de']
    allowed_categories_re = 'thema|politik|wirtschaft|panorama|sport|kultur|netzwelt|wissenschaft|gesundheit|' \
                            'karriere|unispiegel|schulspiegel|reise|auto'
    rules = (
        # Sites which should be saved
        Rule(
            SgmlLinkExtractor(allow='(%s)\/([\/\w-])*\-a\-[0-9]*\.html$' % allowed_categories_re),
            callback='parse_page',
            follow=True
        ),

        # Sites which should be followed, but not saved
        Rule(SgmlLinkExtractor(allow='(%s)\/' % allowed_categories_re)),
    )

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        body = ''
        body += ''.join(hxs.select('//h2[@class="article-title"]//text()').extract()).strip() + '\n'
        body += ''.join(hxs.select('//p[@class="article-intro"]//text()').extract()).strip() + '\n'
        text = hxs.select('//div[@class="article-section clearfix"]/p//text()').extract()
        body += '\n'.join([x for x in [l.strip() for l in text] if not x.startswith(('<!--', '//'))])

        item = GenericItem()
        item['body'] = body
        item['url'] = response.url
        item['simhash'] = str(simhash.hash(body))
        return item
