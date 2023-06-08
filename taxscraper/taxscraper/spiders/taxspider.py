import scrapy


class TaxSpider(scrapy.Spider):
    name = "taxspider"
    allowed_domains = ["www.revisor.mn.gov/statutes/", "www.irs.com"]
    start_urls = ["https://www.revisor.mn.gov/statutes/", "https://www.irs.com"]

    # ===============================================================================
    # Used for iterating thru pages and passing the data to the parse_page function
    def parse(self, response):

        target = response.css('''TARGET TAG''')                     # Enter target css tag here

        for data in target:                                         # Enter individual links in page
            page_url = data.css('''TARGET TAG''')
            '''
            if('TAG/' in next_page):
                item_url = f'https://www.irs.com/{next_page}'
            else:
                item_url = f'https://www.irs.com/TAG/{next_page}'
            yield response.follow(item_url, callback=self.parse_page)   # Parse data from page
            '''
    
        next_page = response.css('''TARGET TAG''').get()                # Get href for the next page

        if next_page is not None:                                       # Run until there are no more pages
            '''
            if('TAG/' in next_page):
                next_page_url = f'https://www.irs.com/{next_page}'
            else:
                next_page_url = f'https://www.irs.com/TAG/{next_page}'
            '''
            next_page_url = f'https://www.irs.com/{next_page}'
            yield response.follow(next_page_url, callback=self.parse)
    
    # ===============================================================================
    # Used as a helper function for parsing the html from target pages
    def parse_page(self, res):
        
        data = res.css('''TARGET TAG''')

        # Collect target data here
        yield {
            'url': res.url,
            'title': res.css('.title').get()
        }