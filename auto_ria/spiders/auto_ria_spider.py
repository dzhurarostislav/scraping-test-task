import scrapy
from scrapy.http import Response
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.chrome.options import Options


class AutoRiaSpider(scrapy.Spider):
    name = "auto_ria"
    allowed_domains = ["auto.ria.com"]
    start_urls = ["https://auto.ria.com/uk/car/used/"]

    def __init__(self):
        super(AutoRiaSpider, self).__init__()
        options = Options()
        options.add_argument('--headless=new')
        self.driver = webdriver.Chrome(options=options)
        self.count = 0

    def parse(self, response: Response, **kwargs):
        product_links = response.css(".ticket-title a::attr(href)").getall()
        for product_link in product_links:
            yield scrapy.Request(
                url=product_link,
                callback=self.parse_product,
                meta={"url": product_link}
            )
        next_page_link = response.css("a.js-next::attr(href)").get()
        if next_page_link:
            self.count += 1
            if self.count < 10:
                yield scrapy.Request(url=next_page_link, callback=self.parse)

    @staticmethod
    def all_non_empty_data_value(driver) -> list | bool:
        phones = driver.find_elements(By.CSS_SELECTOR, ".popup-show-phone .list-phone a")
        for phone in phones:
            data_value = phone.get_attribute("data-value")
            if not data_value:
                return False
        return phones

    @staticmethod
    def string_phones_to_int(phones) -> list[int]:
        int_phones = []
        char_remove = ["(", ")", " "]
        for phone in phones:
            str_phone = phone.get_attribute("data-value")
            for char in char_remove:
                str_phone = str_phone.replace(char, "")
            str_phone = int("38" + str_phone)
            int_phones.append(str_phone)
        return int_phones

    def parse_product(self, response: Response, **kwargs):
        title = response.css(".ticket-status-0 .heading .head::text").get()
        price_usd = response.css(".price.mb-15.mhide strong::text").get()
        odometer = response.css(".price.mb-15.mhide .base-information span::text").get()
        username = response.css(".seller_info_name.bold::text").get()
        image_url = response.css(".gallery-order.carousel source::attr(srcset)").get()
        image_count = response.css(".gallery-order.carousel .mhide::text").get()
        car_number = response.css(".state-num::text").get()
        car_vin = response.css(".t-check .label-vin::text, .vin-code::text").get()

        wait = WebDriverWait(self.driver, 10)
        self.driver.get(response.meta.get("url"))

        phone_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".phones_list.mb-15 .mhide")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", phone_button)
        phone_button.click()
        phones = wait.until(lambda driver: self.all_non_empty_data_value(driver))

        yield {
            "url": response.meta.get("url"),
            "title": title,
            "price_usd": int(price_usd[:len(price_usd) - 1].replace(" ", "")),
            "odometer": int(odometer + "000"),
            "username": username,
            "phone_number": self.string_phones_to_int(phones),
            "image_url": image_url,
            "images_count": image_count[2:],
            "car_number": car_number,
            "car_vin": car_vin,
        }

    def closed(self, reason) -> None:
        self.driver.quit()
