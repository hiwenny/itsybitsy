# for extracting info in individual pages recursively.
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
import json

from retailers.items import RetailersItem


class GlueSpider(CrawlSpider):
    name = 'glue'
    allowed_domains = ('www.gluestore.com.au',)
    # rules = [Rule(LinkExtractor(allow='/stores/.*'), follow=True, callback='parse_item')]
    rules = [Rule(LinkExtractor(deny=r'/blog'), follow=True, callback='parse_item')]
    start_urls = ('https://www.gluestore.com.au/',)
    custom_settings = {'DUPEFILTER_DEBUG':True, 'ROBOTSTXT_OBEY': False}

    # def parse_dupe(self, response):
    #     yield Request(url=response.url, dont_filter=True, callback=self.parse_item)

    def parse_item(self, response):
        if 'stores' not in response.url:
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
