import scrapy
from itemloaders.processors import MapCompose
from exchanges.utils import ItemParser


class BranchSettlementItem(scrapy.Item):
    date = scrapy.Field(input_processor=MapCompose(str.strip, ItemParser.p_date))  # 資料日期
    code = scrapy.Field()  # 證券代號
    branch = scrapy.Field()  # 券商
    price = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, float))  # 價格
    buy = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 買進股數
    sell = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 賣出股數

    class Meta:
        name = 'twse_branch_settlement'
        fields = ['branch', 'price', 'buy', 'sell']
