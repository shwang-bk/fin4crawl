# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy import Selector
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst
from exchanges.utils import ItemParser


class StockListsItem(scrapy.Item):
    SymbolPrefix = scrapy.Field()  # 股票期貨、選擇權商品代碼
    StockZH = scrapy.Field()  # 標的證券
    StockSymbol = scrapy.Field()  # 證券代號
    StockAbbreviationZH = scrapy.Field()  # 標的證券簡稱
    HasStockFuture = scrapy.Field(input_processor=MapCompose(ItemParser.p_circle_sign))  # 是否為股票期貨標的
    HasStockOption = scrapy.Field(input_processor=MapCompose(ItemParser.p_circle_sign))  # 是否為股票選擇權標的
    IsETStock = scrapy.Field(input_processor=MapCompose(ItemParser.p_circle_sign))  # 上市普通股標的證券
    IsOTCStock = scrapy.Field(input_processor=MapCompose(ItemParser.p_circle_sign))  # 上櫃普通股標的證券
    IsETETF = scrapy.Field(input_processor=MapCompose(ItemParser.p_circle_sign))  # 上市ETF標的證券
    NotionalFactor = scrapy.Field()  # 標準型證券股數
    
    class Meta:
        fields_to_export = [
            'SymbolPrefix', 'StockZH', 'StockSymbol', 'StockAbbreviationZH',
            'HasStockFuture', 'HasStockOption', 'IsETStock', 'IsOTCStock', 'IsETETF',
            'NotionalFactor'
        ]
    

class StockListsSpider(scrapy.Spider):
    name = 'taifex_stock_lists'
    allowed_domains = ['www.taifex.com.tw']
    date = datetime.date.today().strftime("%Y%m%d")

    def start_requests(self):
        self.logger.info(f'Parsing date: {self.date}')
        yield scrapy.Request(
            'https://www.taifex.com.tw/cht/2/stockLists',
            self.parse)

    def parse(self, response):
        x_paths = [
            ('SymbolPrefix', '//td[1]/text()'),
            ('StockZH', '//td[2]/text()'),
            ('StockSymbol', '//td[3]/text()'),
            ('StockAbbreviationZH', '//td[4]/text()'),
            ('HasStockFuture', '//td[5]/font/text()'),
            ('HasStockOption', '//td[6]/font/text()'),
            ('IsETStock', '//td[7]/font/text()'),
            ('IsOTCStock', '//td[8]/font/text()'),
            ('IsETETF', '//td[9]/font/text()'),
            ('NotionalFactor', '//td[10]/text()'),
        ]
        rows = response.xpath('//tr[count(td)=10]').extract()
        for row in rows:
            loader = ItemLoader(item=StockListsItem(), selector=Selector(text=row))
            loader.default_input_processor = MapCompose(str, str.strip)
            loader.default_output_processor = TakeFirst()
            for field, path in x_paths:
                loader.add_xpath(field, path)
            yield loader.load_item()
