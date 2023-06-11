# Define here the models for your scraped items
import scrapy


class TaxItem(scrapy.Item):

    statute = scrapy.Field()
    section_number = scrapy.Field()
    subdiv_number = scrapy.Field()
    info = scrapy.Field()
