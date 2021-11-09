# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy import Selector
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst
from exchanges.utils import ItemParser


class ETFMarginingItem(scrapy.Item):
    StockFutureSymbol = scrapy.Field()  # 股票期貨英文代碼
    StockSymbol = scrapy.Field()  # 股票期貨標的證券代號
    StockFutureZH = scrapy.Field()  # 股票期貨中文簡稱
    StockZH = scrapy.Field()  # 股票期貨標的證券
    SettlementMargin = scrapy.Field(input_processor=MapCompose(ItemParser.p_num))  # 結算保證金
    MaintainMargin = scrapy.Field(input_processor=MapCompose(ItemParser.p_num))  # 維持保證金
    InitialMargin = scrapy.Field(input_processor=MapCompose(ItemParser.p_num))  # 原始保證金
    
    class Meta:
        fields_to_export = [
            'StockFutureSymbol', 'StockSymbol', 'StockFutureZH', 'StockZH',
            'SettlementMargin', 'MaintainMargin', 'InitialMargin'
        ]
    

class ETFMarginingSpider(scrapy.Spider):
    name = 'taifex_future_etf_margining'
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
            ('SettlementMargin', '//td[6]/text()'),
            ('MaintainMargin', '//td[7]/text()'),
            ('InitialMargin', '//td[8]/text()'),
        ]
        
        rows = response.xpath('//*[@id="printhere"]/div[1]/table[2]//tr[count(td)=8]').extract()
        for row in rows:
            loader = ItemLoader(item=ETFMarginingItem(), selector=Selector(text=row))
            loader.default_input_processor = MapCompose(str, str.strip)
            loader.default_output_processor = TakeFirst()
            for field, path in x_paths:
                loader.add_xpath(field, path)
            yield loader.load_item()
