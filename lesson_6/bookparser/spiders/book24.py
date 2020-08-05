import scrapy
from scrapy.http import HtmlResponse
from lesson_6.bookparser.items import BookparserItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(".//a[contains(@class, 'catalog-pagination__item') and normalize-space(text())='Далее']/@href").extract_first()
        books_links = response.xpath(".//a[@class='book__image-link js-item-element ddl_product_link']/@href").extract()
        for link in books_links:
            yield response.follow(link, callback=self.book_parse)

        yield response.follow(next_page, callback=self.parse)



    def book_parse(self, response: HtmlResponse):

        link_book = response.url
        name_book = response.xpath(".//h1[@class='item-detail__title']/text()").extract()
        author_book = response.xpath(".//span[@class='item-tab__chars-value']/a/text()").extract()
        price_old_book = response.xpath(".//div[@class='item-actions__price-old']/text()").extract()
        price_new_book = response.xpath(".//div[@class='item-actions__price']/b/text()").extract()
        price_book = response.xpath(".//div[@class='item-actions__price']/b/text()").extract()
        rate_book = response.xpath(".//span[@class='rating__rate-value']/text()").extract()
        yield BookparserItem(name=name_book, author=author_book, price=price_book, price_new=price_new_book,
                             price_old=price_old_book, rate=rate_book, link=link_book)
# item-detail__title h1
# rating__rate-value span
# item-actions__price b new_price
# item-actions__price-old div old_price
# item-actions__price b
# item-tab__chars-link js-data-link a author
# catalog-pagination__item _text js-pagination-catalog-item
# catalog-pagination__item _text js-pagination-catalog-item