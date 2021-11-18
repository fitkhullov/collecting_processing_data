import scrapy
from scrapy.http import HtmlResponse
from leruaparser.items import LeruaparserItem
from scrapy.loader import ItemLoader


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
        loader = ItemLoader(item=LeruaparserItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', '//*[@slot="primary-price"]//span[@slot="price"]/text()')
        loader.add_xpath('photos', '//uc-pdp-media-carousel//picture//source[1][@srcset]/@srcset')
        loader.add_value('link', response.url)
        yield loader.load_item()
