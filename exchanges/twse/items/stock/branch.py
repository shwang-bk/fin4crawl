import scrapy
from scrapy.loader.processors import MapCompose
from exchanges.utils import ItemParser


class StockBranchItem(scrapy.Item):
    date = scrapy.Field(input_processor=MapCompose(str.strip, ItemParser.p_date))  # 資料日期
    code = scrapy.Field()  # 證券代號
    branch = scrapy.Field()  # 券商
    price = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, float))  # 價格
    shares_buy_branch = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 買進股數
    shares_sell_branch = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 賣出股數

    @staticmethod
    def terms():
        return ['branch', 'price', 'shares_buy_branch', 'shares_sell_branch']
