# web_scraper

Python web scraper used for extracting data for a machine learning model. The target data is tax regulations 
within the United States.

## Setting Up Environment

STEP 1: cd into working directory that contains your project  

STEP 2: Create environment:  
```
C: virtualenv env               # env is the environment file name
```  

STEP 3: Activate env:  
```
C: env\Scripts\activate         # Windows
C: source env/bin/activate      # Mac
```  

## Setting Up Scrapy Files

CD into your working directory and execute the following command to setup the config file, 
spider directory, and other python files (items.py, middlewares.py, etc.).

Scrapy create command:  
```
scrapy startproject filename
scrapy startproject taxscraper  
```

Once the files have been created, cd into the spider directory and execute the following command to create 
a spider py file:  
```
scrapy genspider [spider filename] [url of site being scraped]  
scrapy genspider taxspider www.irs.com
```

## Running Spider

The scraper can be executed once all the files have been created. First, cd into the directory containing the initial py 
files (items.py, middlewares.py, etc.). Enter the following command to run the scraper:  
```
scrapy crawl [spider filename]
scrapy crawl taxspider
```

To send results to json file, first cd into the directory containing your spider then enter the following command:  
```
scrapy runspider [spider py file] -o [output json file]  
scrapy runspider taxspider.py -o output.json
```

## Spiders

Spiders are classes which define how a certain site (or a group of sites) will be scraped, including how to perform the crawl (i.e. follow links) and how to extract structured data from their pages (i.e. scraping items). In other words, Spiders are the place where you define the custom behaviour for crawling and parsing pages for a particular site (or, in some cases, a group of sites).

For spiders, the scraping cycle goes through something like this:

1. You start by generating the initial Requests to crawl the first URLs, and specify a callback function to be called with the response downloaded from those requests. The first requests to perform are obtained by calling the start_requests() method which (by default) generates Request for the URLs specified in the start_urls and the parse method as callback function for the Requests.

2. In the callback function, you parse the response (web page) and return item objects, Request objects, or an iterable of these objects. Those Requests will also contain a callback (maybe the same) and will then be downloaded by Scrapy and then their response handled by the specified callback.

3. In callback functions, you parse the page contents, typically using Selectors (but you can also use BeautifulSoup, lxml or whatever mechanism you prefer) and generate items with the parsed data.

4. Finally, the items returned from the spider will be typically persisted to a database (in some Item Pipeline) or written to a file using Feed exports.

## Items

Items are what's returned from spiders after extracting unstructured data from sources such as web pages.

## Middleware

The spider middleware is a framework of hooks into Scrapy’s spider processing mechanism where you can plug custom functionality to process the responses that are sent to Spiders for processing and to process the requests and items that are generated from spiders.


## Pipelines

This is where items that have been scraped go to be processed. Items are aproved for actions or dropped and no longer processed.

Typical uses of item pipelines are:  
* cleansing HTML data
* validating scraped data (checking that the items contain certain fields)
* checking for duplicates (and dropping them)
* storing the scraped item in a database

## Settings

The Scrapy settings allows you to customize the behaviour of all Scrapy components, including the core, extensions, pipelines and spiders themselves.

## Checking Website's Crawling Protocols

To check a website's crawling protocols or guidelines, look for a file called "robots.txt" on the website's domain. The "robots.txt" file is a standardized way for websites to communicate their crawling guidelines to web crawlers, including search engine bots.

Here's how you can check a website's "robots.txt" file:

1. Open a web browser and go to the website's domain.  

2. Append "/robots.txt" to the end of the domain URL and press Enter. For example, if the website is "example.com", the URL to check the "robots.txt" file would be "example.com/robots.txt".

3. The web browser will display the contents of the "robots.txt" file if it exists and is accessible.

4. The "robots.txt" file may contain specific directives that instruct web crawlers on which parts of the website they are allowed to access and crawl. It may include rules such as disallowing access to certain directories or specifying user-agent specific instructions.

By examining the "robots.txt" file, you can gain insights into the website's crawling policies and guidelines.

## Helpful Links
 
[Scrapy Documentation](https://docs.scrapy.org/en/latest/index.html)  
[2022 Minnesota Statutes](https://www.revisor.mn.gov/statutes/)
