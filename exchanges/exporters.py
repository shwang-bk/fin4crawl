import dataset
from scrapy.exporters import BaseItemExporter


class SQLiteItemExporter(BaseItemExporter):
    def __init__(self, file, **kwargs):
        super().__init__(**kwargs)
        self.db = dataset.connect(f'sqlite:///{file.name}')

    def export_item(self, item):
        table = self.db[item.__class__.__name__]
        table.insert(item)
