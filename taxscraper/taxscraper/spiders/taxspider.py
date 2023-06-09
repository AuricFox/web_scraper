import scrapy
import logging

class TaxSpider(scrapy.Spider):
    name = "taxspider"
    allowed_domains = ["www.revisor.mn.gov/statutes/"]
    start_urls = ["https://www.revisor.mn.gov/statutes/"]

    # ===============================================================================
    # Used for iterating thru pages and passing the data to the parse_page function
    def parse(self, response):
        table_rows = response.xpath('//tbody/tr')                   # Get data in the table body
        print(f'Size of data: {len(table_rows)}')

        # Iterate thru all the rows in the table and get the links to the next page
        for data in table_rows:
            next_page = data.xpath('.//a/@href').get()              # Get the next page link
            print(f'Next Link: {next_page}')
            '''
            Some pages have absolute urls and others have relative urls.
            The relative urls need to be reformatted: 
            /statues/cite/1.01 => https://www.revisor.mn.gov/statutes/cite/1.01
            or
            /statues/cite/1.01 => /cite/1.01
            '''
            if(self.start_urls[0] not in next_page):           # Invalid relative url
                subpage = next_page.split('statues/')[-1]           # Get last part of relative url
                next_page = f'{self.start_urls[0]}{subpage}'        # Append absolute and relative url

            yield response.follow(next_page, callback=self.parse)   # Recursively pass next page 

        if not table_rows:                                          # Last page reached, parse it
            self.parse_page(response)
    
    # ===============================================================================
    # Used as a helper function for parsing the html from target pages
    def parse_page(self, res):
        print("working")
        #data = res.css('''TARGET TAG''')

        # Collect target data here
        yield {
            'url': res.url,
            'title': res.css('.title').get()
        }

# Adjust the logging settings
logging.getLogger('scrapy').propagate = False
logging.getLogger().setLevel(logging.WARNING)