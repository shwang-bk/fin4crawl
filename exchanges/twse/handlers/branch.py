import json
import datetime
import re

import cv2
import numpy as np
import pytesseract
from PIL import Image


class StockBranchHandler:
    req_id = 0
    url_prefix = 'https://bsr.twse.com.tw/bshtm'
    menu_url = f'{url_prefix}/bsMenu.aspx'
    content_url = f'{url_prefix}/bsContent.aspx'

    @classmethod
    def stocks_request(cls, date, callback, err_callback):
        return {
            'url': f'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date={date}&type=ALLBUT0999',
            'callback': callback,
            'errback': err_callback,
            'encoding': 'cp950'
        }

    @classmethod
    def get_symbols(cls, response):
        jresp = json.loads(response.body_as_unicode())
        symbols = [row[0] for row in jresp['data9']]
        return [symbol.strip() for symbol in symbols]
    
    @classmethod
    def load_symbols(cls, filename='symbols.tmp'):
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
                return [line.strip() for line in lines]
        except FileNotFoundError:
            return []

    @classmethod
    def write_symbols(cls, symbols, filename='symbols.tmp'):
        with open(filename, 'w') as f:
            f.write('\n'.join(symbols))

    @classmethod
    def new_request(cls, symbol, callback, err_callback):
        cls.req_id += 1
        meta = {'cookiejar': cls.req_id, 'symbol': symbol}
        return {
            'url': cls.menu_url,
            'callback': callback,
            'errback': err_callback,
            'meta': meta,
            'dont_filter': True
        }

    @classmethod
    def new_form(cls, response):
        symbol = response.meta['symbol']
        form = {
            'RadioButton_Normal': 'RadioButton_Normal',
            'TextBox_Stkno': symbol,
            'CaptchaControl1': '',
            'btnOK': '查詢'
        }
        keys = response.xpath('.//input[@type="hidden"]/@id').extract()
        values = response.xpath('.//input[@type="hidden"]/@value').extract()
        form.update({key: val for key, val in zip(keys, values)})
        return form

    @classmethod
    def get_img_url(cls, response):
        img_uuid = response.xpath('.//td/div/div/img/@src').extract()[0]
        return f"{cls.url_prefix}/{img_uuid}"

    @classmethod
    def update_form(cls, response, form):
        img = response.body
        captcha = CaptchaBreaker.guess(img)
        if len(captcha) == 5:
            form.update({'CaptchaControl1': captcha})
        return form

    @classmethod
    def check_download_link(cls, response):
        return response.xpath('.//a[@id="HyperLink_DownloadCSV"]/@href')


class CaptchaBreaker:
    @classmethod
    def guess(cls, captcha):
        if captcha:
            captcha = cls._clean_captcha(captcha)
            return cls._guess(captcha)
        return ''

    # From https://github.com/hhschu/Captcha_OCR
    @classmethod
    def _clean_captcha(cls, captcha):
        captcha = np.asarray(bytearray(captcha), dtype=np.uint8)
        captcha = cv2.imdecode(captcha, cv2.IMREAD_GRAYSCALE)
        (thresh, captcha) = cv2.threshold(captcha, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        captcha = cv2.erode(captcha, np.ones((3, 3), dtype=np.uint8))
        (thresh, captcha) = cv2.threshold(captcha, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        captcha = cv2.fastNlMeansDenoising(captcha, h=50)
        captcha = Image.fromarray(captcha)
        return captcha

    @classmethod
    def _guess(cls, captcha):
        text = re.sub('[^0-9A-Z]+', '', pytesseract.image_to_string(captcha, lang='eng').upper())
        return text or ''
