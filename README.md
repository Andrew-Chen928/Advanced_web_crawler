# Python_web_scrapier
Powerful Web Scraping &amp; Crawling program with Python <br>

In this project, I have used and compared Scrapy framework and Selenium to complete the data scraping from different websites. The final demo is an Ebay spider with graph generator "Matplotlib" which I will sedcribe below.<br>

Scrapy is an asynchronous framework which make a huge improve on efficiency when crawling large amount of data from multiple web pages.I have tried the function of scrapy to work with other tools including "Selenium", Matplotlib. The result showed that scrapy works much faster than combine with Selenium. But you can still try Selenium for specific purpose (EX. Login, click...) <br>

Scrapy use "xpath" to define and locate the data as you desire. Xpath is really simple if you know HTML tags or CSS basic concept. The easiest way to test the result is using scrapy shell(very similar to use shell in django)<br>
Example of what you can do by the shell:<br><br>
In [58]: response.xpath('//span[@class="w2b-sgl"]/text()').extract_first()
Out[58]: '709 sold'
<br>

If you are scraping a website with link of "next page", you can import http.request for looping the Request(take a look of the example spider files).For demo, I made an Ebay spider to grab all the information about "wiper" post on Ebay. The spider finally collected more the 5,000 rows of data and export to .csv file.<br>

<img src="/eBayCar/csv_demo.png" alt="demo">


For a quick demo that how to generate a easy to read graph of your data, I create a smaller csv file with only 50 rows of data. Then I just wrote a little script to achieve the goal. You can find too many different kinds of tools to complete the task. In this demo, I use Matplotlib which I highly recommend for creating a graph. It support lots of different graph. As you can see, you can auto generator the png file like this:<br>

<img src="/eBayCar/wiper_demo.png" alt="demo">

PS: To successfully scraping websites which good at detect and ban auto-scraping ip like Amazon.com, there are some extra setting and selections you can choose:

1. set up download_delay (about 3 seconds) 
2. randomly change your user agent: (you can use some tools for example: https://github.com/alecxe/scrapy-fake-useragent) 
3. Random proxy: check this https://github.com/aivarsk/scrapy-proxies
