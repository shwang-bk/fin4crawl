# fin4crawl
[![MIT](https://img.shields.io/github/license/shwang-bk/finance4py)](https://opensource.org/licenses/MIT)

一些關於交易所資料的爬蟲

# 套件需求

- pipenv
- tesseract
- sqlite3

# 安裝

```sh
$ git clone https://github.com/shwang-bk/fin4crawl
$ cd fin4crawl
$ pipenv install
```

# 使用
## 列表

```sh
$ pipenv run scrapy list
taifex_future_code  # 期貨對應碼
twse_stock_basic    # 上市公司基本資訊
twse_stock_branch   # 券商分點
twse_stock_chip     # 三大法人
twse_stock_margin   # 資券餘額
twse_stock_quote    # 交易概況
twse_warrant_info   # 權證資訊
```

## 爬取資料

爬取後資料會存至 fin4crawl.db ，請再自行使用相關 SQLite Browser 開啟使用
```sh
$ pipenv run scrapy crawl twse_stock_quote -a date=20200325 -o fin4crawl.db -t sqlite
```
