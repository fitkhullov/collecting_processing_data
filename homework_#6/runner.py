from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.superjob import SuperjobSpider
from jobparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)  # импорт настроек из файла settings.py в паука
    process = CrawlerProcess(settings=crawler_settings)  # загрузка настроек в паука
    process.crawl(SuperjobSpider)
    process.crawl(HhruSpider)  # инициализация паука
    process.start()  # начало работы паука
