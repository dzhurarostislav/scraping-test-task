import scrapy
from scrapy.http import Response
from unicodedata import decimal


class AutoRiaSpider(scrapy.Spider):
    name = "auto_ria"
    allowed_domains = ["auto.ria.com"]
    start_urls = ["https://auto.ria.com/uk/car/used/"]

    def parse(self, response: Response, **kwargs):

        product_links = response.css(".ticket-title a::attr(href)").getall()
        for product_link in product_links:
            yield scrapy.Request(
                url=product_link,
                callback=self.parse_product,
                meta={"url": product_link}
            )
        # next_page_link = response.css("a.js-next::attr(href)").get()
        # if next_page_link:
        #    yield scrapy.Request(url=next_page_link, callback=self.parse)

    def parse_product(self, response: Response, **kwargs):
        title = response.css(".ticket-status-0 .heading .head::text").get()
        price_usd = response.css(".price.mb-15.mhide strong::text").get()
        odometer = response.css(".price.mb-15.mhide .base-information span::text").get()
        username = response.css(".seller_info_name.bold::text").get()
        yield {
            "url": response.meta.get("url"),
            "text": title,
            "price_usd": int(price_usd[:len(price_usd)-1].replace(" ", "")),
            "odometer": int(odometer + "000"),
            "username": username
        }
