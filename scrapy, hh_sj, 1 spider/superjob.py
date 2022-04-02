import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_url = 'https://russia.superjob.ru'
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        next_page = self.start_url + response.xpath("//a[contains(@class, 'f-test-link-Dalshe')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = [self.start_url+x for x in response.xpath('//div[@class="f-test-search-result-item"]//div[@class="jNMYr GPKTZ _1tH7S"]//a/@href').getall()]

        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath('//h1/text()').get()
        salary = response.xpath('//span[@class="_2Wp8I _1e6dO _1XzYb _3Jn4o"]/text()').getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)
