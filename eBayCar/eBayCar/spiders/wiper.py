# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


class WiperSpider(scrapy.Spider):
    name = "wiper"
    allowed_domains = ["www.ebay.com"]
    start_urls = ['http://www.ebay.com/sch/i.html?_from=R40&_trksid=\
                   p2050601.m570.l1311.R1.TR11.TRC1.A0.H0.XWiper.TRS0&_nkw=wiper+blades&_sacat=0/']

    def parse(self, response):
        urls = response.xpath('//h3[contains(@class, "lvtitle")]/a/@href').extract()
        for url in urls:
    	    yield Request(url, callback=self.wiper_info)

        # next_page_url = response.xpath('//a[@aria-label="Next page of results"]/@href').extract_first()
        # yield Request(next_page_url)


    def wiper_info(self, response):
        title = response.xpath('//h1[@id="itemTitle"]/text()').extract_first()
        price = response.xpath('//span[@class="notranslate"]/text()').extract_first()[4:]
        # price = response.xpath('//span[@id="mm-saleDscPrc"]/text()').extract_first()
        condition = response.xpath('//div[@id="vi-itm-cond"]/text()').extract_first()
        # if type(response.xpath('//div[@class="hotness-signal red"]/text()').extract_first()) != "NoneType":
        #     # sold = response.xpath('//div[@class="hotness-signal red"]/text()').extract_first().replace('\n\t\t\t\t\t', '').replace(' sold', '')              
        #     print("sold !!!!!~~~~~~~~~~~")
        #     sold = 100
        # else:
        #     sold = 0
        #     print("None !!!!!!!~~~~~~~")
        sold = response.xpath('//span[@class="w2b-sgl"]/text()').extract_first()[-4:]
        if sold == "sold":
            sold = response.xpath('//span[@class="w2b-sgl"]/text()').extract_first()[0:-5]
        else:
            sold = 0
            print("NONE !!!!!~~~~")
        #                .replace('\n\t\t\t\t\t', '').replace(' sold', '')

        yield {
               # 'title': title,
               'price': price,
               # 'condition': condition
               'sold': sold
               }
       
        
