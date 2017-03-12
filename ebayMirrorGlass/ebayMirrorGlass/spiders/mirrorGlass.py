# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

class MirrorglassSpider(scrapy.Spider):
	name = "mirrorGlass"
	allowed_domains = []
	start_urls = ['http://stores.ebay.com/']


	def parse(self, response):
		main_url = "http://stores.ebay.com/Hub-Caps-and-Mirror-Glass-Plus/_i.html?rt=nc&_nkw=Mirror%20Glass&_sid=8608538&_trksid=p4634.c0.m14.l1581&_pgn="
		next_url = ""
		for i in range(1, 106):
			next_url = main_url + str(i)
			yield Request(next_url, callback=self.search_page)	

	def search_page(self, response):
		mirror_urls = response.xpath('//*[@class="details"]//a/@href').extract()
		for url in mirror_urls:
			yield Request(url, callback=self.mirror_info)


	def mirror_info(self, response):

		product_name = response.xpath('//h1[@id="itemTitle"]/text()').extract_first()
		product_url = response.url
		brand = response.xpath('//h2[contains(@itemprop, "brand")]/span/text()').extract_first()
		part_number = response.xpath('//h2[@itemprop="mpn"]/text()').extract_first()
		
		sold_raw = response.xpath('//span[@class="w2b-sgl"]/text()').extract_first()
		if sold_raw[-4:] == "sold":
			sold_amount = sold_raw[0:-5]
		else:
			sold_alt_raw = response.xpath('//span[@class="vi-qtyS vi-bboxrev-dsplblk vi-qty-vert-algn vi-qty-pur-lnk"]/a/text()').extract_first()
			if sold_alt_raw != None:
				sold_amount = sold_alt_raw[0:-5]
			else:
				sold_amount = "no info"

		price = response.xpath('//span[@itemprop="price"]/text()').extract_first()[4:]

		sIndex = False
		dIndex = False
		sizeIndex = False
		target_count = 0

		raw_dimension_titles = response.xpath('//td[@class="attrLabels"]/text()').extract()
		for index in range(0, len(raw_dimension_titles)):
			if "Standard Dimensions" in raw_dimension_titles[index].strip():
				sIndex = True
				target_count += 1
			if "Diagonal Dimension" in raw_dimension_titles[index].strip():
				dIndex = True
				target_count += 1
			if "Size" in raw_dimension_titles[index].strip():
				sizeIndex = True
				target_count += 1
		

		dimensions = []
		raw_dimensions = response.xpath('//td[@width="50.0%"]/span/text()').extract()
		for index in range(0, len(raw_dimensions)):
		
			if raw_dimensions[index][0].isdigit() == True and not raw_dimensions[index] in dimensions:
				dimensions.append(raw_dimensions[index])
			
		if target_count == 0:
			sDimension = "No info"
			dDimension = "No info"

		elif target_count == 1:
			if sIndex == True or sizeIndex == True:
				sDimension = dimensions[0]
				dDimension = "No info"
			else:
				dDimension = dimensions[0]
				sDimension = "No info"
		else:
			if dIndex == False:
				sDimension = dimensions[0]
				dDimension = "No info"
			else:
				sDimension = dimensions[0]
				dDimension = dimensions[1]

		yield {
			'Name': product_name,
			'URL': product_url,
			'Brand': brand,
			'Part#': part_number,
			'Sold_amount': sold_amount,
			'Price': price,
			'Standard_Dimension': sDimension,
			'Diagonal_Dimension': dDimension
		}
