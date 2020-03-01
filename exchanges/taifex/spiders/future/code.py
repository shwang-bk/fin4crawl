# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy import Selector
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst

from exchanges.taifex.items import FutureCodeItem


class FutureCodeSpider(scrapy.Spider):
    name = 'taifex_future_code'
    allowed_domains = ['www.taifex.com.tw']
    date = datetime.date.today().strftime("%Y%m%d")

    def start_requests(self):
        self.logger.info(f'Parsing date: {self.date}')
        yield scrapy.Request(
            'https://www.taifex.com.tw/cht/2/stockLists',
            self.parse)

    def parse(self, response):
        x_paths = [
            ('code', '//td[1]/text()'),
            ('underlying', '//td[3]/text()')
        ]
        rows = response.xpath('//tr[count(td)=10]').extract()
        for row in rows:
            loader = ItemLoader(item=FutureCodeItem(), selector=Selector(text=row))
            loader.default_input_processor = MapCompose(str, str.strip)
            loader.default_output_processor = TakeFirst()
            for field, path in x_paths:
                loader.add_xpath(field, path)
            yield loader.load_item()
