# -*- coding: utf-8 -*-
import scrapy


class UpworkSpider(scrapy.Spider):
    name = "upwork"
    allowed_domains = ["https://www.upwork.com/o/jobs/browse/"]
    start_urls = ['https://www.upwork.com/o/jobs/browse/?q=scrapy/']

    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers)

    def parse(self, response):
        # h2_tag = response.xpath('//h2/a/text()')
        tags = response.xpath('//h2/a/text()').extract()
        for tag in tags:
        	print (tag.strip())
        # s.strip() for s in tags
        print ("size = %s" % len(tags))  

		# desc = site.select('a/text()').extract()
        tags = [s.strip() for s in tags]
     

        yield {'Tags': tags}
