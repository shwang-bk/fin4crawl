# -*- coding: utf-8 -*-
import datetime
import json
from collections import OrderedDict

import six
import scrapy
from scrapy import Selector
from scrapy.exporters import CsvItemExporter
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst
from exchanges.utils import ItemParser


class StockMarginingItem(scrapy.Item):
    StockFutureSymbol = scrapy.Field()  # 股票期貨英文代碼
    StockSymbol = scrapy.Field()  # 股票期貨標的證券代號
    StockFutureZH = scrapy.Field()  # 股票期貨中文簡稱
    StockZH = scrapy.Field()  # 股票期貨標的證券
    MarginClassInterval = scrapy.Field()  # 保證金所屬級距
    SettlementMargin = scrapy.Field(input_processor=MapCompose(ItemParser.p_rate))  # 結算保證金適用比例
    MaintainMargin = scrapy.Field(input_processor=MapCompose(ItemParser.p_rate))  # 維持保證金適用比例
    InitialMargin = scrapy.Field(input_processor=MapCompose(ItemParser.p_rate))  # 原始保證金適用比例
    
    class Meta:
        fields_to_export = [
            'StockFutureSymbol', 'StockSymbol', 'StockFutureZH', 'StockZH',
            'MarginClassInterval', 'SettlementMargin', 'MaintainMargin', 'InitialMargin'
        ]
    

class StockMarginingSpider(scrapy.Spider):
    name = 'taifex_future_stock_margining'
    allowed_domains = ['www.taifex.com.tw']
    date = datetime.date.today().strftime("%Y%m%d")

    def start_requests(self):
        self.logger.info(f'Parsing date: {self.date}')
        yield scrapy.Request(
            'https://www.taifex.com.tw/cht/5/stockMargining',
            self.parse)

    def parse(self, response):
        x_paths = [
            ('StockFutureSymbol', '//td[2]/text()'),
            ('StockSymbol', '//td[3]/text()'),
            ('StockFutureZH', '//td[4]/text()'),
            ('StockZH', '//td[5]/text()'),
            ('MarginClassInterval', '//td[6]/text()'),
            ('SettlementMargin', '//td[7]/text()'),
            ('MaintainMargin', '//td[8]/text()'),
            ('InitialMargin', '//td[9]/text()'),
        ]
        rows = response.xpath('//*[@id="printhere"]/div[1]/table[1]//tr[count(td)=9]').extract()
        for row in rows:
            loader = ItemLoader(item=StockMarginingItem(), selector=Selector(text=row))
            loader.default_input_processor = MapCompose(str, str.strip)
            loader.default_output_processor = TakeFirst()
            for field, path in x_paths:
                loader.add_xpath(field, path)
            yield loader.load_item()
