import scrapy
from itemloaders.processors import MapCompose
from exchanges.utils import ItemParser


class MarginTradingItem(scrapy.Item):
    date = scrapy.Field(input_processor=MapCompose(str.strip, ItemParser.p_date))  # 資料日期
    code = scrapy.Field()  # 證券代號
    name = scrapy.Field()  # 證券名稱

    long = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 融資買進
    long_flat = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 融資賣出
    long_flat_repayment = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 融資現金償還
    long_deposit_last = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 融資前日餘額
    long_deposit = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 融資今日餘額
    long_deposit_limit = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 融資限額

    short_flat = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 融券買進
    short = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 融券賣出
    short_flat_repayment = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 融券現券償還
    short_deposit_last = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 融券前日餘額
    short_deposit = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 融券今日餘額
    short_deposit_limit = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 融券限額

    class Meta:
        name = 'twse_margin_trading'
        fields = [
            'code', 'name',
            'long', 'long_flat', 'long_flat_repayment',
            'long_deposit_last', 'long_deposit', 'long_deposit_limit',
            'short_flat', 'short', 'short_flat_repayment',
            'short_deposit_last', 'short_deposit', 'short_deposit_limit'
        ]
