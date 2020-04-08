import dataset
from scrapy.exporters import BaseItemExporter

from exchanges import settings


class SQLiteItemExporter(BaseItemExporter):
    def __init__(self, file, **kwargs):
        super().__init__(**kwargs)
        self.db = dataset.connect(f'sqlite:///{file.name}')

    def export_item(self, item):
        table = self.db[item.Meta.name]
        table.insert(item)


class SQLItemExporter(BaseItemExporter):
    def __init__(self, _file, **kwargs):
        super().__init__(**kwargs)
        self.db = dataset.connect(settings.DATABASE_URL)

    def export_item(self, item):
        table = self.db[item.Meta.name]
        table.insert(item)
