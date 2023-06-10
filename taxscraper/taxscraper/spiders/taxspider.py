import scrapy
import logging

class TaxSpider(scrapy.Spider):
    name = "taxspider"
    # Use domain name, not specific paths for allowed domains
    allowed_domains = ["www.revisor.mn.gov"]
    start_urls = ["https://www.revisor.mn.gov/statutes/"]

    # ===============================================================================
    # Used for iterating thru pages and passing the data to the parse_page function
    def parse(self, response):
        table_rows = response.xpath('//tbody/tr')                   # Get data in the table body
        logging.info(f'Size of data: {len(table_rows)}')

        if len(table_rows) == 0:                                    # Last page reached, parse it
            yield self.parse_page(response)

        # Iterate thru all the rows in the table and get the links to the next page
        for data in table_rows:
            next_page = data.xpath('.//a/@href').get()              # Get the next page link
            #logging.info(f'Next Page -> {next_page} | Size of data: {len(table_rows)}')
            '''
            Some pages have absolute urls and others have relative urls.
            The relative urls need to be reformatted: 
            /statues/cite/1.01 => https://www.revisor.mn.gov/statutes/cite/1.01
            or
            /statues/cite/1.01 => /cite/1.01
            '''
            if next_page is None: continue                          # Ignore rows without links

            if(self.start_urls[0] not in next_page):                # Invalid relative url
                subpage = next_page.split('statutes/')[-1]          # Get last part of relative url
                next_page = f'{self.start_urls[0]}{subpage}'        # Append absolute and relative url
            
            logging.info(f'Next Page URL: {next_page}')
            yield response.follow(next_page, callback=self.parse)   # Recursively pass next page 
    
    # ===============================================================================
    # Used as a helper function for parsing the html from target pages
    def parse_page(self, res):
        logging.info(f'Response Status Code: {res.status}')
        #data = res.css('''TARGET TAG''')

        # Collect target data here
        yield {
            'url': res.url,
            'title': res.css('.title').get()
        }

# Adjust the logging settings
logging.getLogger('scrapy').propagate = False
logging.getLogger().setLevel(logging.WARNING)