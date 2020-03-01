import scrapy
from scrapy.loader.processors import MapCompose
from exchanges.utils import ItemParser


class StockQuoteItem(scrapy.Item):
    date = scrapy.Field(input_processor=MapCompose(str.strip, ItemParser.p_date))  # 資料日期
    code = scrapy.Field()  # 證券代號
    name = scrapy.Field()  # 證券名稱
    shares_trade = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 成交股數
    trade_count = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 成交筆數
    amount_trade = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 成交金額
    price_open = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, float))  # 開盤價
    price_high = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, float))  # 最高價
    price_low = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, float))  # 最低價
    price_close = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, float))  # 收盤價
    price_change_sign = scrapy.Field(input_processor=MapCompose(ItemParser.p_sign))  # 漲跌記號
    price_change = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, float))  # 漲跌值
    last_bid = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, float))  # 最後揭示買價
    last_bid_qty = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 最後揭示買量
    last_ask = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, float))  # 最後揭示賣價
    last_ask_qty = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 最後揭示賣量
    pe_ratio = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, float))  # 本益比

    @staticmethod
    def terms():
        return ['code', 'name', 'shares_trade', 'trade_count', 'amount_trade',
                'price_open', 'price_high', 'price_low', 'price_close',
                'price_change_sign', 'price_change',
                'last_bid', 'last_bid_qty', 'last_ask', 'last_ask_qty', 'pe_ratio']