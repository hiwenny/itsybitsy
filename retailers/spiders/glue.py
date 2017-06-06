# for extracting info in individual pages recursively.
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import json

from retailers.items import RetailersItem


class GlueSpider(CrawlSpider):
    name = 'glue'
    allowed_domains = ('www.gluestore.com.au',)
    rules = [Rule(LinkExtractor(), follow=True, callback='parse_item')]
    start_urls = ('https://www.gluestore.com.au/stores',)

    def parse_item(self, response):
        if 'index' not in response.url:
            return

        item = RetailersItem()
        item['store_hours'] = ', '.join([s.xpath('normalize-space(.)').extract_first().replace(u'\xa0', '') for s in response.xpath('////div[@id="content"]//div[@class="location-store-info"]//div[@class="location-oph"]//tbody/tr')])
        item['phone_number'] = response.xpath('//div[@id="content"]//div[@class="location-store-info"]//div[@class="location-cnt"]//label[@class="det-phone"]/text()').extract_first()
        item['store_name'] = response.xpath('re:match(//div[@id="content"]//div[@class="location-store-title page-title"]/h1/text(), "-\s?(.*)")[last()]/text()').extract_first()
        item['address'] = response.xpath('normalize-space(//div[@id="content"]//div[@class="location-store-info"]//div[@class="location-cnt"]//label[@class="det-address"])').extract_first()
        for state in ['QLD', 'VIC', 'NSW', 'SA', 'WA', 'NT']:
            if state in item['address']:
                item['state'] = state
        yield item
