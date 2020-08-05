import scrapy
from scrapy.http import HtmlResponse
from lesson_6.bookparser.items import BookparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5/?stype=0']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(".//a[@class='pagination-next__text']/@href").extract_first()
        books_links = response.xpath(".//a[@class='product-title-link']/@href").extract()
        for link in books_links:
            yield response.follow(link, callback=self.book_parse)

        yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        # *Ссылку на книгу
        # *Наименование книги
        # *Автор(ы)
        # *Основную цену
        # *Цену со скидкой
        # *Рейтинг книги
        link_book = response.url
        name_book = response.xpath(".//div[@class='prodtitle']/h1/text()").extract()
        author_book = response.xpath(".//div[@class='authors']/a/text()").extract()
        price_old_book = response.xpath(".//span[@class='buying-priceold-val-number']/text()").extract()
        price_new_book = response.xpath(".//span[@class='buying-pricenew-val-number']/text()").extract()
        price_book = response.xpath(".//span[@class='buying-price-val-number']/text()").extract()
        rate_book = response.xpath(".//div[@id='rate']/text()").extract()
        yield BookparserItem(name=name_book, author=author_book, price=price_book, price_new=price_new_book, price_old=price_old_book, rate=rate_book, link=link_book)
