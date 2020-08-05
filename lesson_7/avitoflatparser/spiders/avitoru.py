import scrapy
from scrapy.http import HtmlResponse
from lesson_7.avitoflatparser.items import AvitoflatparserItem
from scrapy.loader import ItemLoader

from scrapy.item import ItemMeta
import os

class AvitoruSpider(scrapy.Spider):
    name = 'avitoru'
    allowed_domains = ['avito.ru']
    # start_urls = ['https://www.avito.ru/chelyabinsk/kvartiry/prodam/2-komnatnye/vtorichka-ASgBAQICAUSSA8YQAkDmBxSMUsoIFIJZ?cd=1&district=10&f=ASgBAQECAUSSA8YQA0DmBxSMUsoIFIJZkL4NFJauNQJF4AcXeyJmcm9tIjo1MTIxLCJ0byI6bnVsbH2ECRV7ImZyb20iOjUwLCJ0byI6bnVsbH0']
    start_urls = ['https://www.avito.ru/chelyabinsk/kvartiry/prodam/3-komnatnye/vtorichka-ASgBAQICAUSSA8YQAkDmBxSMUsoIFIRZ?cd=1&district=10&f=ASgBAQECAUSSA8YQA0DmBxSMUsoIFIRZkL4NFJauNQJF4AcXeyJmcm9tIjo1MTIxLCJ0byI6bnVsbH2ECRV7ImZyb20iOjUwLCJ0byI6bnVsbH0']
    i = 1
    def parse(self, response: HtmlResponse):

        print(response)
        links = response.xpath("//h3/a[@class='snippet-link']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)
        next_page = response.xpath("//span[contains(@data-marker,'pagination-button/next')]/@class").extract_first()
        print(next_page)
        if 'pagination-item_readonly-2V7oG' in next_page:
            return
        self.i += 1

        switch_page = response.url + f'&p={self.i}'
        yield response.follow(switch_page, callback=self.parse)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=AvitoflatparserItem(), response=response)
        loader.add_xpath('name', "//h1/span/text()")
        loader.add_xpath('_id', "//div[@class='item-view-search-info-redesign']/span[@data-marker='item-view/item-id']")
        loader.add_xpath('photos', "//div[contains(@class,'gallery-img-wrapper')]/div/@data-url")
        loader.add_value('url', response.url)
        loader.add_xpath('address', "//span[@class='item-address__string']/text()")
        loader.add_xpath('district', "//span[@class='item-address-georeferences-item__content']/text()")
        loader.add_xpath('price', "//span[@class='js-item-price']/text()")
        loader.add_xpath('body', "//div[@class='item-description-text']/p/text()")
        loader.add_value('parameters', self.create_dict(response))
        yield loader.load_item()

    def create_dict(self, response):
        params1 = []
        params = response.xpath("//ul[@class='item-params-list']//span[@class='item-params-label']/text()").extract()
        values = response.xpath("//ul[@class='item-params-list']/li[@class='item-params-list-item']/text()").extract()
        for value in values:
            if value == ' ':
                values.remove(value)
            else:
                value.replace('\xa0', ' ')
        for param in params:
            param = param.replace(':', '')
            params1.append(param)
        parameters = dict(zip(params1, values))
        return parameters


