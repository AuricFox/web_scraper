# Define here the models for your scraped items
import scrapy


class TaxItem(scrapy.Item):

    url = scrapy.Field()
    statute = scrapy.Field()
    section_number = scrapy.Field()
    info = scrapy.Field()
