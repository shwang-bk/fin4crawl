import json
import datetime

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, SelectJmes

from exchanges.twse.items import QuoteItem


class QuoteSpider(scrapy.Spider):
    name = 'twse_quote'
    allowed_domains = ['www.twse.com.tw']
    date = datetime.date.today().strftime("%Y%m%d")

    def start_requests(self):
        self.logger.info(f'Parsing date: {self.date}')
        yield scrapy.Request(
            url=f'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date={self.date}&type=ALLBUT0999',
            callback=self.parse,
            encoding='cp950')

    def parse(self, response):
        self.logger.info('%s', response.url)
        terms = QuoteItem.Meta.fields
        jresp = json.loads(response.body_as_unicode())
        data = SelectJmes('data9')(jresp)
        if not data:
            return
        date = SelectJmes('date')(jresp)
        for row in data:
            loader = ItemLoader(item=QuoteItem())
            loader.default_input_processor = MapCompose(str, str.strip)
            loader.default_output_processor = TakeFirst()
            loader.add_value('date', date)
            for idx, field in enumerate(terms):
                loader.add_value(field, SelectJmes(f'[{idx}]')(row))
            yield loader.load_item()
