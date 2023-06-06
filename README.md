# web_scraper

Python web scraper used for extracting data for a machine learning model.

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

## Setting Up Scrapy Directory

This command creates a new directory that stores the config file, spider directory, and python code.

Scrapy create command:  
```
scrapy startproject filename
```

## Spiders

Spiders are classes which define how a certain site (or a group of sites) will be scraped, including how to perform the crawl (i.e. follow links) and how to extract structured data from their pages (i.e. scraping items). In other words, Spiders are the place where you define the custom behaviour for crawling and parsing pages for a particular site (or, in some cases, a group of sites).

For spiders, the scraping cycle goes through something like this:

1. You start by generating the initial Requests to crawl the first URLs, and specify a callback function to be called with the response downloaded from those requests.

The first requests to perform are obtained by calling the start_requests() method which (by default) generates Request for the URLs specified in the start_urls and the parse method as callback function for the Requests.

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

## Sources
 
[Scrapy Documentation](https://docs.scrapy.org/en/latest/index.html)
