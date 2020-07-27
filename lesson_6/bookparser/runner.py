from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lesson_6.bookparser import settings
from lesson_6.bookparser.spiders.book24 import Book24Spider
from lesson_6.bookparser.spiders.labirint import LabirintSpider


if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LabirintSpider)
    # process.crawl(Book24Spider)

    process.start()
