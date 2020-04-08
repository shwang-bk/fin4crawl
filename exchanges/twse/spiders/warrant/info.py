# -*- coding: utf-8 -*-
import datetime
import scrapy
from scrapy import Selector
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
from exchanges.twse.items import WarrantInfoItem


class WarrantInfoSpider(scrapy.Spider):
    name = 'twse_warrant_info'
    allowed_domains = ['isin.twse.com.tw']
    date = datetime.date.today().strftime("%Y%m%d")

    def start_requests(self):
        self.logger.info(f'Parsing date: {self.date}')
        yield scrapy.FormRequest(url='https://mops.twse.com.tw/mops/web/ajax_t90sbfa01', formdata={
            'encodeURIComponent': '1', 'step': '1', 'ver': '1.9', 'TYPEK': '', 'market': '1',
            'wrn_class': 'all', 'stock_no': '', 'wrn_no': '', 'co_id': 'all', 'wrn_type': 'all',
            'left_month': 'all', 'return_rate': 'all', 'price_down': '', 'price_up': '',
            'price_inout': 'all', 'newprice_down': '', 'newprice_up': '', 'fin_down': '', 'fin_up': '', 'sort': '1'
        }, callback=self.parse)

    def parse(self, response):
        self.logger.info('%s', response.url)
        fields = WarrantInfoItem.Meta.fields
        rows = response.xpath('//tr[count(td)=21]').extract()
        for row in rows:
            loader = ItemLoader(item=WarrantInfoItem(), selector=Selector(text=row))
            loader.default_input_processor = MapCompose(str, str.strip)
            loader.default_output_processor = TakeFirst()
            loader.add_value('date', self.date)
            for idx, field in enumerate(fields, start=1):
                if field:
                    loader.add_xpath(field, f'//td[{idx}]/text()')
            yield loader.load_item()
