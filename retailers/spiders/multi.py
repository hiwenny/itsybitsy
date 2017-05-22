from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from retailers.items import RetailersItem


class MultiSpider(CrawlSpider):
    name = 'multi'
    allowed_domains = ('www.universalstore.com',)
    rules = [Rule(LinkExtractor(allow=r'/store-locator'), follow=True, callback='parse_item')]
    start_urls = ('https://www.universalstore.com/store-locator/',)
    custom_settings = {'ROBOTSTXT_OBEY': False}

    def parse_item(self, response):
        item = RetailersItem()
        phone_numbers_array = response.xpath('//p[@class="phone-number"]/text()').extract()
        store_names_array = response.xpath('//p[@class="storename"]/text()').extract()
        store_hours_array = response.xpath('//p[@class="opening-hours"]')
        addresses_array = response.xpath('//p[@class="address"]')
        # for hours in store_hours_array:
        #     (hours.xpath('normalize-space(.)').extract())

        # json_node = response.xpath('//script[contains("@type":"Store")]/text()').extract_first()
        # print(json_node)
        # item['store_hours'] = response.xpath('//time[@itemprop="openingHours"]/@datetime').extract()
        # item['location'] = response.xpath('normalize-space(//section[contains(@class, "store-address-phone")])').extract_first()
        for i, val in enumerate(phone_numbers_array):
            item['phone_number'] = val
            item['store_name'] = store_names_array[i]
            item['store_hours'] = store_hours_array[i].xpath('substring-after(normalize-space(.), "Opening Hours: ")').extract()
            item['address'] = addresses_array[i].xpath('normalize-space(.)').extract_first()
            for state in ['QLD', 'VIC', 'NSW', 'SA', 'WA', 'NT']:
                if state in item['address']:
                    item['state'] = state
            yield item
        # pass



    # city = scrapy.Field()
    # suburb = scrapy.Field()
    # zip_code = scrapy.Field()
    # latitude = scrapy.Field()
    # longitude = scrapy.Field()
