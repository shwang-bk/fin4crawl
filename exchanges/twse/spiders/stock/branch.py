import datetime

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst

from exchanges.twse.items import StockBranchItem
from exchanges.twse.handlers import StockBranchHandler as Handler


class StockBranchSpider(scrapy.Spider):
    name = 'twse_stock_branch'
    allowed_domains = ['bsr.twse.com.tw']
    date = datetime.date.today().strftime("%Y%m%d")

    def __init__(self, *args, **kwargs):
        super(StockBranchSpider, self).__init__(*args, **kwargs)
        self.processed = self.total = []

    def start_requests(self):
        self.logger.info(f'Parsing date: {self.date}')
        self.total = Handler.load_symbols()
        if self.total:
            for symbol in self.total:
                req = Handler.new_request(symbol, self.parse, self.on_error)
                yield scrapy.Request(**req)
        else:
            req = Handler.stocks_request(self.date, self.parse_stocks, None)
            yield scrapy.Request(**req)

    def parse_stocks(self, response):
        self.total = Handler.get_symbols(response)
        for symbol in self.total:
            req = Handler.new_request(symbol, self.parse, self.on_error)
            yield scrapy.Request(**req)

    def parse(self, response):
        if Handler.check_download_link(response):
            yield scrapy.Request(url=Handler.content_url, meta=response.meta, encoding='cp950',
                                 callback=self.parse_csv, errback=self.on_error, dont_filter=True)
        else:
            response.meta['form'] = Handler.new_form(response)
            yield scrapy.Request(url=Handler.get_img_url(response), meta=response.meta,
                                 callback=self.parse_img, errback=self.on_error, dont_filter=True)

    def parse_img(self, response):
        form = response.meta['form']
        form = Handler.update_form(response, form)
        yield scrapy.FormRequest(url=Handler.menu_url, meta=response.meta, formdata=form,
                                 callback=self.parse, errback=self.on_error, dont_filter=True)

    def parse_csv(self, response):
        rows = response.body_as_unicode().split('\n')
        rows = [row for row in rows if row.count(',') == 10 and ('券商' not in row)]
        for row in rows:
            row = row.split(',')
            yield self.parse_raw(response.meta['symbol'], row[1:5])
            yield self.parse_raw(response.meta['symbol'], row[7:])
        self.processed.append(response.meta['symbol'])
        self.logger.info(f"({len(self.processed)}/{len(self.total)}) {response.meta['symbol']} [{len(rows)} rows]")

    def parse_raw(self, symbol, raw):
        terms = StockBranchItem.terms()
        loader = ItemLoader(item=StockBranchItem())
        loader.default_input_processor = MapCompose(str, str.strip)
        loader.default_output_processor = TakeFirst()
        loader.add_value('date', self.date)
        loader.add_value('code', symbol)
        for idx, field in enumerate(terms):
            loader.add_value(field, raw[idx])
        return loader.load_item()

    def on_error(self, failure):
        symbol = failure.request.meta['symbol']
        req = Handler.new_request(symbol, self.parse, self.on_error)
        yield scrapy.Request(**req)
    
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=scrapy.signals.spider_closed)
        return spider
    
    def spider_closed(self, spider):
        least = set(self.total) - set(self.processed)
        self.logger.info(f"Write {len(least)} symbol cache")
        Handler.write_symbols(least)
