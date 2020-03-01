import datetime
import json

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, SelectJmes

from exchanges.twse.items import StockMarginItem


class StockMarginSpider(scrapy.Spider):
    name = 'twse_stock_margin'
    allowed_domains = ['www.twse.com.tw']
    date = datetime.date.today().strftime("%Y%m%d")

    def start_requests(self):
        self.logger.info(f'Parsing date: {self.date}')
        yield scrapy.Request(
            url=f'https://www.twse.com.tw/exchangeReport/MI_MARGN?response=json&date={self.date}&selectType=ALL',
            callback=self.parse,
            encoding='cp950')

    def parse(self, response):
        self.logger.info('%s', response.url)
        terms = StockMarginItem.terms()
        jresp = json.loads(response.body_as_unicode())
        data = SelectJmes('data')(jresp)
        if not data:
            return
        date = SelectJmes('date')(jresp)
        for row in data:
            loader = ItemLoader(item=StockMarginItem())
            loader.default_input_processor = MapCompose(str, str.strip)
            loader.default_output_processor = TakeFirst()
            loader.add_value('date', date)
            for idx, field in enumerate(terms):
                loader.add_value(field, SelectJmes(f'[{idx}]')(row))
            yield loader.load_item()
