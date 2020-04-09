import scrapy
from scrapy.loader.processors import MapCompose

from exchanges.utils import ItemParser


class StockInfoItem(scrapy.Item):
    date = scrapy.Field(input_processor=MapCompose(str.strip, ItemParser.p_date))  # 資料日期
    code = scrapy.Field()  # 證券代號
    name = scrapy.Field()  # 股票名稱
    publish_shares = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 已發行普通股數
    listing_date = scrapy.Field(input_processor=MapCompose(str.strip, ItemParser.p_date_minguo))  # 掛牌日

    class Meta:
        name = 'twse_stock_info'
