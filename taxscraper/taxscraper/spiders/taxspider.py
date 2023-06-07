import scrapy


class TaxSpider(scrapy.Spider):
    name = "taxspider"
    allowed_domains = ["www.irs.com"]
    start_urls = ["https://www.irs.com"]

    # ===============================================================================
    # Used for parsing the html from the generated response from the target url
    def parse(self, response):

        res = response.css()            # Enter target css tag here

        for r in res:
            yield{
                'name': r.css()         # Enter target data here
            }
    
        next_page = response.css('''ENTER HREF TAG''').get()            # Get href for next
        
        if next_page is not None:                                       # Run until there are no more pages
            next_page_url = f'https://www.irs.com/{next_page}'
            yield response.follow(next_page_url, callback=self.parse)
