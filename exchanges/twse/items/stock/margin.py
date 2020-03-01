import scrapy
from scrapy.loader.processors import MapCompose
from exchanges.utils import ItemParser


class StockMarginItem(scrapy.Item):
    date = scrapy.Field(input_processor=MapCompose(str.strip, ItemParser.p_date))  # 資料日期
    code = scrapy.Field()  # 證券代號
    name = scrapy.Field()  # 證券名稱
    volume_margin_trading_buy = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 融資買進
    volume_margin_trading_sell = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 融資賣出
    volume_margin_trading_repayment = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 融資現金償還
    volume_margin_trading_total_lastday = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 融資前日餘額
    volume_margin_trading_total = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 融資今日餘額
    volume_margin_trading_limit = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 融資限額
    volume_short_selling_buy = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 融券買進
    volume_short_selling_sell = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 融券賣出
    volume_short_selling_repayment = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 融券現券償還
    volume_short_selling_total_lastday = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 融券前日餘額
    volume_short_selling_total = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 融券今日餘額
    volume_short_selling_limit = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 融券限額

    @staticmethod
    def terms():
        return ['code', 'name', 'volume_margin_trading_buy', 'volume_margin_trading_sell',
                'volume_margin_trading_repayment', 'volume_margin_trading_total_lastday',
                'volume_margin_trading_total', 'volume_margin_trading_limit',
                'volume_short_selling_buy', 'volume_short_selling_sell',
                'volume_short_selling_repayment', 'volume_short_selling_total_lastday',
                'volume_short_selling_total', 'volume_short_selling_limit']