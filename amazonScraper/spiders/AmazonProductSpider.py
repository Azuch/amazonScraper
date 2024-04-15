import scrapy


class AmazonproductspiderSpider(scrapy.Spider):
    name = "AmazonProductSpider"
    allowed_domains = ["amazon.com"]
    
    def start_requests(self):
        key_list = ['ipad']
        for key in key_list:
            amazon_search_url = f"https://www.amazon.com/s?k={key}"
            yield scrapy.Request(url=amazon_search_url, callback=self.parse_page, meta={"key": key})

    def parse_page(self, response):
        key = response.meta['key']

        #Get all products from this page
        products = response.css('div.s-result-item')
        for product in products:
            relative_url = product.xpath('//a/@href')
            yield scrapy.Request(url=f"https://amazon.com{relative_url}", callback=parse_product, meta={'key': key})
        #Go to next page
        next_page = response.xpath('//a[contains(@class, "s-pagination-next")]/@href')
        if next_page:
            yield scrapy.Request(url=f"https://amazon.com{next_page}", callback=self.parse_page, meta={"key": key})

    def parse_product(self, response):
        pass
