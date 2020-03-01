import scrapy
from scrapy.loader.processors import MapCompose
from exchanges.utils import ItemParser


class StockChipItem(scrapy.Item):
    date = scrapy.Field(input_processor=MapCompose(str.strip, ItemParser.p_date))  # 資料日期
    code = scrapy.Field()  # 證券代號
    name = scrapy.Field()  # 證券名稱
    shares_buy_foreign = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 外陸資買進股數(不含外資自營商)
    shares_sell_foreign = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 外陸資賣出股數(不含外資自營商)
    shares_net_foreign = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 外陸資買賣超股數(不含外資自營商)
    shares_buy_foreign_dealer = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 外資自營商買進股數
    shares_sell_foreign_dealer = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 外資自營商賣出股數
    shares_net_foreign_dealer = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 外資自營商買賣超股數
    shares_buy_trust = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 投信買進股數
    shares_sell_trust = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 投信賣出股數
    shares_net_trust = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 投信買賣超股數
    shares_net_dealer = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 自營商買賣超股數
    shares_buy_dealer_self = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 自營商買進股數(自行買賣)
    shares_sell_dealer_self = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 自營商賣出股數(自行買賣)
    shares_net_dealer_self = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 自營商買賣超股數(自行買賣)
    shares_buy_dealer_hedge = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 自營商買進股數(避險)
    shares_sell_dealer_hedge = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 自營商賣出股數(避險)
    shares_net_dealer_hedge = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 自營商買賣超股數(避險)
    shares_net_legal_person = scrapy.Field(input_processor=MapCompose(ItemParser.p_num, int))  # 三大法人買賣超股數

    @staticmethod
    def terms():
        return ['code', 'name', 'shares_buy_foreign', 'shares_sell_foreign', 'shares_net_foreign',
                'shares_buy_foreign_dealer', 'shares_sell_foreign_dealer', 'shares_net_foreign_dealer',
                'shares_buy_trust', 'shares_sell_trust', 'shares_net_trust',
                'shares_net_dealer',
                'shares_buy_dealer_self', 'shares_sell_dealer_self', 'shares_net_dealer_self',
                'shares_buy_dealer_hedge', 'shares_sell_dealer_hedge', 'shares_net_dealer_hedge',
                'shares_net_legal_person']
