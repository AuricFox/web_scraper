# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class TaxscraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)
        
        # Drop all occurances of null statutes from the data
        if adapter.get('statute') is None:
            raise DropItem("Item dropped: Null statute")


        return item
    
    