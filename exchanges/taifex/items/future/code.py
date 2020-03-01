import scrapy


class FutureCodeItem(scrapy.Item):
    code = scrapy.Field()
    underlying = scrapy.Field()
