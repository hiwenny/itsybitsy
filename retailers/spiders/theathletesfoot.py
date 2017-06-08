# for extracting info in individual pages recursively.
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import json

from retailers.items import RetailersItem


class TAFSpider(CrawlSpider):
    name = 'theathletesfoot'
    allowed_domains = ('www.theathletesfoot.com.au',)
    rules = [Rule(LinkExtractor(deny='r/shoe-brands'), follow=True, callback='parse_item')]
    start_urls = ('https://www.theathletesfoot.com.au/',)

    def parse_item(self, response):
        if 'store-location' not in response.url:
            return

        item = RetailersItem()
        item['store_hours'] = ', '.join([s.xpath('normalize-space(.)').extract_first() for s in response.xpath('//div[@class="storeDetails"]//div[@class="storeDetailsDiscription"]//div[contains(@class, "time-row")]')])
        item['phone_number'] = response.xpath('normalize-space(//div[@class="storeDetails"]//div[@class="microsite-address-details"]//div[@class="telephone"]//text())').extract_first()
        item['store_name'] = response.xpath('//div[@class="storeDetails"]//div[@class="pagenName"]/h1/text()').extract_first()
        address = response.xpath('normalize-space(//div[@class="storeDetails"]//div[@class="microsite-address-details"]//span[@class="address"])').extract_first()[:-1]
        if not address:
            address = response.xpath('normalize-space(//div[@class="storeDetails"]//div[@class="microsite-address-details"]//div[@class="address"])').extract_first()[:-1]
        item['address'] = address
        item['state'] = response.xpath('re:match(normalize-space(//div[@class="storeDetails"]//div[@class="microsite-address-details"]//span[@class="shop-addr"]), ",\s*(\w+)\s*,")[last()]/text()').extract_first()
        item['zip_code'] = response.xpath('re:match(normalize-space(//div[@class="storeDetails"]//div[@class="microsite-address-details"]//span[@class="shop-addr"]), ",[A-Z\s]*(\d+)")[last()]/text()').extract_first()
        for state in ['QLD', 'VIC', 'NSW', 'SA', 'WA', 'NT']:
            if state in item['address']:
                item['state'] = state
        yield item
