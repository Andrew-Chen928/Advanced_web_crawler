# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class BookSpiderSpider(CrawlSpider):
    name = "book_spider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ['http://books.toscrape.com/']

    rules = (Rule(LinkExtractor(), callback='parse_page', follow=False),)
    # other useful argument for Rule:  deny_domains=('facebook.com')
    #                                  allow=('item\/php')
    def parse_page(self, response):
        yield {'URL': response.url}
