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
        # Extract all the text withing the page section
        #data = res.xpath('//div[@class="section"]//text()').extract()

        url = res.url                                                           # Get URL from response
        statute = self.get_statute(res)                                         # Get statute title
        section_number = self.get_section_number(res, statute)                  # Get section number
        subdiv_number = res.xpath('//div[@class="subd"]/@id').getall()          # Get subdivision number        
        info = res.xpath('//div[@class="section"]/p/text()').getall()           # Main text description

        # Statute has been repealed, renumbered, or expired
        if statute is None:
            section_number = res.xpath('//div[@class="sr"]/@id').get()

            text = res.xpath('//div[@class="sr"]/text()').get()
            print(f'Text: {text}')
            if 'Expired' in text: info.append("Expired")
            elif 'Repealed' in text: info.append("Repealed")
            elif 'Renumbered' in text: info.append("Renumbered")
            else: info.append("Unknown")

        # There are multiple subdivisions that have different html tags
        elif subdiv_number:
            info = res.xpath('//div[@class="subd"]/p/text()').getall()           # Main text description
        '''
        logging.info(
            f'===============================================================================\n'
            f'URL: {url}\n'
            f'Statute: {statute}\n'
            f'Section Number: {section_number}\n'
            f'Sub-div Number: {subdiv_number}'
        )
        '''
        tax_item = TaxItem()
        tax_item['url'] = url
        tax_item['statute'] = statute
        tax_item['section_number'] = section_number
        tax_item['subdiv_number'] = subdiv_number
        tax_item['info'] = info
        
        yield tax_item

    # ===============================================================================
    # Gets statute title from response page
    # Returns a string
    def get_statute(self, res):
        return res.xpath('//div[@class="section"]/h1/text()').get()
    
    # ===============================================================================
    # Gets section number from response page
    # Returns a section_number (String)
    def get_section_number(self, res, statute):
        subdiv_number = res.xpath('//div[@class="subd"]/@id').getall()             # Get subdivision number
        section_number = res.xpath('//div[@class="section"]/@id').get()     # Normal statute

        # Statute has been repealed, renumbered, or expired and there are NO sub-divisions
        if statute is None and not subdiv_number:
            section_number = res.xpath('//div[@class="sr"]/@id').get()
        # Statute has been repealed, renumbered, or expired and there are sub-divisions
        elif statute is None and subdiv_number:
            section_number = res.xpath('//div[@class="sr_by_subd"]/@id').get()

        return section_number
    
    # ===============================================================================
    # Parses statute information from response page
    # Returns Data as a dictionary {sub-division number: info}
    def get_subdiv_info(self, res, statute):
        subdiv_number = res.xpath('//div[@class="subd"]')         
        info = res.xpath('//div[@class="section"]/p/text()').getall()       # Main text description
        data = {}

        # There are multiple subdivisions that have different html tags
        if subdiv_number:
            for div in subdiv_number:
                id = div.xpath('./@id').get()                               # Get the id attribute of the div
                text = div.xpath('.//text()').getall()                      # Get all the text within the div

                # Remove leading/trailing whitespace and join the text together
                text = ' '.join(text).strip()

                if 'Expired' in text: text = "Expired"
                elif 'Repealed' in text: text = "Repealed"
                elif 'Renumbered' in text: text = "Renumbered"
                else: text = "Unknown"

                data[id] = text
        # There are no subdivisions
        elif not subdiv_number:

            # Statute has been repealed, renumbered, or expired
            if statute is None:

                text = res.xpath('//div[@class="sr"]/text()').get()
                print(f'Text: {text}')
                if 'Expired' in text: text = "Expired"
                elif 'Repealed' in text: text = "Repealed"
                elif 'Renumbered' in text: text = "Renumbered"
                else: text = "Unknown"
        
        
        return data

# Adjust the logging settings
logging.getLogger('scrapy').propagate = False
logging.getLogger().setLevel(logging.WARNING)