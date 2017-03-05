# -*- coding: utf-8 -*-
import scrapy
from time import sleep
from scrapy.http import Request
import csv
from scrapy_splash import SplashRequest
from scrapy.selector import Selector
from selenium import webdriver

class CarPartsSpider(scrapy.Spider):
    name = "car_parts"
    allowed_domains = ["www.ebay.com"]
    start_urls = ['http://www.ebay.com/']


    def parse(self, response):
        left_url = "http://www.ebay.com/sch/i.html?_from=R40&_sacat=0&_nkw=condenser%20"
        # left_url = "http://www.ebay.com/sch/i.html?_from=R40&_sacat=0&LH_ItemCondition=3&_nkw="
        right_url = "&_pppn=r1&scp=ce0"
        counter = 1
        # url = "http://www.ebay.com/sch/i.html?_from=R40&_sacat=0&LH_ItemCondition=3&_nkw=30773744%20307737440%2030773744%2086342470&_pppn=r1&scp=ce0"
        # print(url)
        # print("abc!!!")
        # yield Request(url, callback=self.check_result)
        with open('ac.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:

                DPI = row['DPI'].strip()
                absolute_url = left_url + DPI + right_url
                # print(counter)
                print(str(counter) + " -> " + absolute_url)
                # yield {'URL': absolute_url}
                counter += 1
                yield Request(absolute_url, meta={'DPI': DPI}, callback=self.check_result)
                                            
            # DPI = '89545-42040'
            # absolute_url = left_url + DPI + right_url
            # yield Request(absolute_url, meta={'DPI': DPI}, callback=self.check_result)
                                            
    def check_result(self, response):
        DPI = response.meta['DPI']
        print("DPI = " + DPI)
        result = response.xpath('//*[@class="rcnt"]/text()').extract_first()
        print(result)
        # print(int(result))
        
        if int(result) == 0:
            yield {'price': 'N/A', 'note': '', 'DPI': DPI}
        elif int(result) > 50:
            yield {'price': 'unknown', 'note': 'unknown', 'DPI': DPI}
        else:
            price_list = response.xpath('//ul[@id="ListViewInner"]//li[@class="lvprice prc"]/span/text()').extract()
            # urls = response.xpath('//ul[@id="ListViewInner"]/li[contains(@class, "lvresult clearfix li")]/h3/a/@href').extract()
            
            bids = response.xpath('//*[@class="lvformat"]/span/text()').extract()
            if len(price_list) < int(result):
                result = str(len(price_list))
                print("change result to " + str(result))	
            target_price = 99999999.99
            target_index = 0
            for i in range(0, int(result)):
                if price_list[i].strip() == '':
                    del price_list[i]
                if bids[i].strip()[-4:] == 'bids':
                    price_list[i] = '99999999.99'
                print("index = " + str(i) + " list = " + str(float(price_list[i].strip()[1:])))
                if float(price_list[i].strip()[1:]) < target_price:
                    target_price = float(price_list[i].strip()[1:])
                    target_index = i
            print(target_price)
            print(target_index)
            check_url = response.xpath('//ul[@id="ListViewInner"]/li[contains(@class, "lvresult clearfix li")]/h3/a/@href').extract()[target_index]
            print("check for:")
            print(check_url)
            yield Request(check_url, meta={'DPI': DPI}, callback=self.get_info)

            response.xpath('//h3[@class="lvtitle"]/a/@href').extract()

            # check_url = response.xpath('//ul[@id="ListViewInner"]/li[contains(@class, "lvresult clearfix li")][1]/h3/a/@href').extract_first()	
            # print("check for:")
            # print(check_url)
            # yield Request(check_url, callback=self.get_info)



    def get_info(self, response):
        DPI = response.meta['DPI']
        if not DPI in str(response.body):
            yield {'price': 'unknown', 'note': 'unknown', 'DPI': DPI}
        else:
            if response.xpath('//*[@class="notranslate"]/text()').extract_first()[0:2] == 'US':	
                price = response.xpath('//*[@class="notranslate"]/text()').extract_first()[4:]
            else:
                price = response.xpath('//span[@id="convbinPrice"]/text()').extract_first()[4:]
            print("price = " + price)
            # shipping = "FREE"
            shipping = response.xpath('//*[@id="fshippingCost"]/span/text()').extract_first()
            if "United States" in response.xpath('//span[@itemprop="availableAtOrFrom"]/text()').extract_first():
                note = ''
            else:
                note = 'non-US'  
            condition = response.xpath('//div[contains(@itemprop, "itemCondition")]/text()').extract_first()
            # print("DPI = " + DPI + " shipping = " + shipping)
            # print("shipping = " + shipping)
            if price == None or shipping == None or shipping != "FREE" or condition != "New":
                yield {'price': 'unknown', 'note': 'unknown', 'DPI': DPI}
            else:
                yield {'price': price, 'note': note, 'DPI': DPI}

       