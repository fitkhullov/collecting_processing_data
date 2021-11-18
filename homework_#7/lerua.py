import scrapy
from scrapy.http import HtmlResponse

class LeruaSpider(scrapy.Spider):
    name = 'lerua'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={query}']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[@data-qa="product-name"]')
        for link in links:
            yield response.follow(link, callback=self.good_parse)

    def good_parse(self, response: HtmlResponse):
        name = response.xpath('//h1/text()').get()
        price = response.xpath('//*[@slot="primary-price"]//span[@slot="price"]/text()').get()
        photos = response.xpath('//uc-pdp-media-carousel//picture//source[1][@srcset]/@srcset').getall()

        print()