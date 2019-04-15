# Hunting Season Scraper

## Usage

In the root folder (where scrapy.cfg is located) run the following command in terminal
```bash
scrapy crawl hunting -o hunting.json --loglevel=INFO
```
hunting is the name of the scraper, -o means output to file, hunting.json is the name of the output file, and loglevel is set to INFO in order to keep only necessary information. 

## Built With

* [Python 3](https://www.python.org/download/releases/3.0/) 
* [Scrapy](https://scrapy.org/) - An open source and collaborative framework for Python data scraping.
