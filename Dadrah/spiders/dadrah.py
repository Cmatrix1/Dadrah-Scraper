import scrapy
from urllib.parse import urljoin
from unidecode import unidecode

class DadrahSpider(scrapy.Spider):
    name = 'dadrah'
    allowed_domains = ['www.dadrah.ir']
    start_urls = ['https://www.dadrah.ir/dadrah-lawyers.php']

    def extrct_text(self, card, xpath):
        return card.xpath(xpath).extract_first().replace(" ", "").replace("\n", "")

    def parse(self, response):
        cards = response.css(".col-12.col-md-4.mb-2")
        
        for card in cards:
            item = {}
            item["name"] = self.extrct_text(card, ".//h6[@class='card-title text-black']/text()")
            item["phone"] = self.extrct_text(card, ".//div[2]/a[1]/@href")
            item["profile"] = self.extrct_text(card, ".//div[2]/a[2]/@href") 
            item["city"] = self.extrct_text(card, ".//small[2]/text()")

            yield scrapy.Request(response.urljoin(item["phone"]), callback=self.parse_phone_info, meta={'dont_redirect': False,"item":item}) 
        
        # next_page_url = response.xpath("//a[contains(text(), 'صفحه بعد')]/@href").extract_first()
        # if next_page_url:
        #     yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)

    def parse_phone_info(self, response):
        item = response.meta["item"]
        item["call_status"] = True if "امکان" in self.extrct_text(response, "//div[1]/div/div[2]/span/text()") else False
        item["hour"] = unidecode(self.extrct_text(response, "//div/div[2]/span[2]/text()"))[:2]
        
        print(item["hour"], item["call_status"])
        # yield {"name":item["name"], "call_status":item["call_status"]}
