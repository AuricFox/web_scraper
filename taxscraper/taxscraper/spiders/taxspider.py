import scrapy
import logging
from taxscraper.items import TaxItem

class TaxSpider(scrapy.Spider):
    name = "taxspider"
    # Use domain name, not specific paths for allowed domains
    allowed_domains = ["www.revisor.mn.gov"]
    start_urls = ["https://www.revisor.mn.gov/statutes/"]

    # ===============================================================================
    # Used for iterating thru pages and passing the data to the parse_page function
    def parse(self, response):
        table_rows = response.xpath('//tbody/tr')                   # Get data in the table body
        #logging.info(f'Size of data: {len(table_rows)} | Response: {response}')

        if len(table_rows) == 0:                                    # Last page reached, parse it
            yield from self.parse_page(response)

        # Iterate thru all the rows in the table and get the links to the next page
        for data in table_rows:
            next_page = data.xpath('.//a/@href').get()              # Get the next page link
            
            '''
            Some pages have absolute urls and others have relative urls.
            The relative urls need to be reformatted: 
            /statues/cite/1.01 => https://www.revisor.mn.gov/statutes/cite/1.01
            or
            /statues/cite/1.01 => /cite/1.01
            '''
            if next_page is None: continue                          # Ignore rows without links

            if self.start_urls[0] not in next_page:                 # Invalid relative url
                subpage = next_page.split('statutes/')[-1]          # Get last part of relative url
                next_page = f'{self.start_urls[0]}{subpage}'        # Append absolute and relative url
            
            yield response.follow(next_page, callback=self.parse)   # Recursively pass next page 
    
    # ===============================================================================
    # Used as a helper function for parsing the text from target pages
    def parse_page(self, res):
        print("===============================================================================")
        
        # Extract all the text withing the page section
        #data = res.xpath('//div[@class="section"]//text()').extract()

        statute = res.xpath('//div[@class="section"]/h1/text()').get()          # Get statute title
        section_number = res.xpath('//div[@class="section"]/@id').get()         # Get section number
        subdiv_number = res.xpath('//div[@class="subd"]/@id').getall()          # Get subdivision number        
        info = res.xpath('//div[@class="section"]/p/text()').getall()           # Main text description

        logging.info(f'\nURL: {res}\nStatute: {statute}\nSection No: {section_number}\nSub-div No: {subdiv_number}')
        tax_item = TaxItem()

        tax_item['statute'] = statute
        tax_item['section_number'] = section_number
        tax_item['subdiv_number'] = subdiv_number
        tax_item['info'] = info
        
        yield tax_item

# Adjust the logging settings
logging.getLogger('scrapy').propagate = False
logging.getLogger().setLevel(logging.WARNING)