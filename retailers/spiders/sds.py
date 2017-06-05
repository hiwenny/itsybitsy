# for extracting info in individual pages recursively.
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import json

from retailers.items import RetailersItem


class SDSSpider(CrawlSpider):
    name = 'sds'
    allowed_domains = ('www.sds.com.au',)
    rules = [Rule(LinkExtractor(), follow=True, callback='parse_item')]
    start_urls = ('https://www.sds.com.au/stores',)

    def parse_item(self, response):
        if 'dealer_detail' not in response.url:
            return

        item = RetailersItem()
        item['store_hours'] = ', '.join([s.strip() for s in response.xpath('//section[@class="store-detail"]//p[@class="hours"]/span/text()').extract()])
        item['phone_number'] = response.xpath('//section[@class="store-detail"]//div[@class="vcard"]/p[@class="tel"]/text()').extract_first()
        item['store_name'] = response.xpath('//section[@class="store-detail"]//div[@class="vcard"]/p[@class="store-name"]/text()').extract_first()
        item['address'] = response.xpath('//section[@class="store-detail"]//div[@class="vcard"]/p[@class="store-address"]/span[@class="street"]/text()').extract_first()
        item['city'] = response.xpath('//section[@class="store-detail"]//div[@class="vcard"]/p[@class="store-address"]/span[@class="city"]/text()').extract_first()
        item['state'] = response.xpath('//section[@class="store-detail"]//div[@class="vcard"]/p[@class="store-address"]/span[@class="state"]/text()').extract_first()
        item['zip_code'] = response.xpath('//section[@class="store-detail"]//div[@class="vcard"]/p[@class="store-address"]/span[@class="postal-code"]/text()').extract_first()
        yield item
