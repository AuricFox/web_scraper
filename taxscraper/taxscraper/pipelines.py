# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class TaxscraperPipeline:
    def __init__(self):
        self.processed_items = set()  # Set to store unique identifiers of processed items

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Assuming the 'statute' field is the unique identifier
        statute = adapter.get('statute')
        if statute is None:                                                 # Statute is Null
            raise DropItem("Item dropped: Null statute")

        if statute in self.processed_items:                                 # Statute is a duplicate
            raise DropItem(f"Item dropped: Duplicate statute - {statute}")
        else:                                                               # Statute is not null nor a duplicate
            self.processed_items.add(statute)
            return item
