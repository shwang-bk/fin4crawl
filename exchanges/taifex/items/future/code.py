import scrapy


class FutureCodeItem(scrapy.Item):
    code = scrapy.Field()
    underlying = scrapy.Field()

    class Meta:
        name = 'taifex_future_code'
