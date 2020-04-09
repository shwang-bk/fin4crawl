import re
import datetime


class ItemParser:
    @staticmethod
    def p_flag(text):
        return True if 'Y' in text else False

    @staticmethod
    def p_sign(text):
        return -1 if '-' in text else 1

    @staticmethod
    def p_num(text):
        text = re.sub(r'[, ]+', '', text)
        text = re.sub(r'[xX\-]+', '0', text)
        return text if text else '0'

    @staticmethod
    def p_xml_tag(text):
        return re.sub(r'<.*?>', '', text)

    @staticmethod
    def p_style(text):
        return 'American' if '美式' in text else 'European'

    @staticmethod
    def p_put_call(text):
        return 'Call' if '認購' in text else 'Put'

    @staticmethod
    def p_date(text):
        return datetime.datetime.strptime(text, "%Y%m%d").date()

    @staticmethod
    def p_date_slash(text):
        return datetime.datetime.strptime(text, "%Y/%m/%d").date()

    @staticmethod
    def p_date_underscore(text):
        return datetime.datetime.strptime(text, "%Y_%m_%d").date()

    @staticmethod
    def p_date_minguo(text):
        text = text.split('/')
        return datetime.datetime(int(text[0]) + 1911, int(text[1]), int(text[2])).date()

    @staticmethod
    def p_time(text):
        return datetime.datetime.strptime(text, '%H%M%S').time()

    @staticmethod
    def p_time_colon(text):
        return datetime.datetime.strptime(text, '%H:%M:%S').time()
