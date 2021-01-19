import scrapy
from itemloaders.processors import MapCompose
from exchanges.utils import ItemParser


class QuoteItem(scrapy.Item):
    date = scrapy.Field(input_processor=MapCompose(str.strip, ItemParser.p_date))  # 資料日期
    code = scrapy.Field()  # 證券代號
    name = scrapy.Field()  # 證券名稱
    shares = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 成交股數
    count = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 成交筆數
    amount = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 成交金額
    open = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, float))  # 開盤價
    high = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, float))  # 最高價
    low = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, float))  # 最低價
    close = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, float))  # 收盤價
    change_sign = scrapy.Field(input_processor=MapCompose(ItemParser.p_sign))  # 漲跌記號
    change = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, float))  # 漲跌值
    last_bid = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, float))  # 最後揭示買價
    last_bid_qty = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 最後揭示買量
    last_ask = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, float))  # 最後揭示賣價
    last_ask_qty = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 最後揭示賣量
    pe_ratio = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, float))  # 本益比

    class Meta:
        name = 'twse_quote'
        fields = [
            'code', 'name', 'shares', 'count', 'amount',
            'open', 'high', 'low', 'close', 'change_sign', 'change',
            'last_bid', 'last_bid_qty', 'last_ask', 'last_ask_qty', 'pe_ratio'
        ]
