import scrapy
from itemloaders.processors import MapCompose
from exchanges.utils import ItemParser


class WarrantInfoItem(scrapy.Item):
    date = scrapy.Field(input_processor=MapCompose(str.strip, ItemParser.p_date))  # 資料日期
    code = scrapy.Field()  # 權證代號
    name = scrapy.Field()  # 權證簡稱
    style = scrapy.Field(input_processor=MapCompose(ItemParser.p_style))  # 美式/歐式
    put_call = scrapy.Field(input_processor=MapCompose(ItemParser.p_put_call))  # 認購/認售
    broker = scrapy.Field()  # 發行人
    price = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, float))  # 權證收盤價格
    listing_date = scrapy.Field(input_processor=MapCompose(str.strip, ItemParser.p_date_minguo))  # 上市日期
    close_date = scrapy.Field(input_processor=MapCompose(str.strip, ItemParser.p_date_minguo))  # 最後交易日
    delivery_date = scrapy.Field(input_processor=MapCompose(str.strip, ItemParser.p_date_minguo))  # 到期日
    publish_shares = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 權證發行數量
    underlying = scrapy.Field()  # 標的代號
    underlying_price = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, float))  # 標的收盤價格/收盤指數/期貨結算價
    exercise_ratio = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, float, lambda x: x / float(1000.0)))  # 行使比例
    strike_price = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, float))  # 最新履約價格

    class Meta:
        name = 'twse_warrant_info'
        fields = [
            'code', 'name', 'style', 'put_call', 'broker', None, 'price', 'listing_date',
            'close_date', 'delivery_date', None, 'publish_shares', 'underlying', None,
            'underlying_price', 'exercise_ratio', 'strike_price'
        ]
