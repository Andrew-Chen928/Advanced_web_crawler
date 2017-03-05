# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


class BookSpiderSpider(scrapy.Spider):
    name = "book_spider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        book_urls = response.xpath('//*[@class="image_container"]/a/@href').extract()
        for href_url in book_urls:
            url = response.urljoin(href_url)
            yield Request(url, callback=self.book_info)
            
        next_url = response.xpath('//*[@class="next"]/a/@href').extract_first()
        next_url = response.urljoin(next_url)
        yield Request(next_url)
    
    
    def book_info(self, response):
        book_name = response.xpath('//*[contains(@class, "product_main")]/h1/text()').extract()
        category = response.xpath('//*[@class="breadcrumb"]/li/a/text()').extract()[2]
        if response.xpath('//table[@class="table table-striped"]//td/text()').extract()[5][0:2] == "In":
            availability = "Yes"
        else:
        	availability = "No"
        price = response.xpath('//table[@class="table table-striped"]//td/text()').extract()[3][1:]
        rating = response.xpath('//div[contains(@class, "product_main")]/p[contains(@class, "star-rating")]/@class').extract_first()[12:]
        image_url = response.xpath('//div[@class="item active"]/img/@src').extract_first()
        image_url = response.urljoin(image_url)
        description = response.xpath('//div[@id="product_description"]/following::p/text()').extract_first()

        yield {
            'book_name': book_name,
            'category': category,
            'availability': availability,
            'price': price,
            'rating': rating,
            'image_url': image_url,
            'description': description
        }
