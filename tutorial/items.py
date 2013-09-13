from scrapy.item import Item, Field

class GenericItem(Item):
    url = Field()
    body = Field()
    simhash = Field()