from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import json, re

from retailers.items import RetailersItem


class CueSpider(CrawlSpider):
    name = 'cue'
    allowed_domains = ('www.cue.cc',)
    rules = [Rule(LinkExtractor(allow=r'/Stores'), follow=True, callback='parse_item')]
    start_urls = ('https://www.cue.cc/Stores',)
    # custom_settings = {'ROBOTSTXT_OBEY': False}

    def parse_item(self, response):
        item = RetailersItem()

        data = json.loads(response.xpath('re:match(//script[contains(text(), "storesModel")]/text(), "storesModel\W*({.*})")[last()]/text()').extract_first())['stores']['australia']

        for stateLevelData in data:
            for region in stateLevelData['storeData']:
                for store in stateLevelData['storeData'][region]:
                    item['store_hours'] = ', '.join('{}{}'.format(key, val) for key, val in store['storeHours'].items())
                    item['phone_number'] = store['phone']
                    item['store_name'] = store['name']
                    item['address'] = re.sub('<[^<]+?>', '', store['address']).replace('\n', ' ').replace('\r', '')
                    item['suburb'] = store['city']
                    item['state'] = store['stateName']
                    item['zip_code'] = store['postCode']
                    item['latitude'] = store['latitude']
                    item['longitude'] = store['longitude']
                    yield item
