from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from retailers.items import RetailersItem


class MultiSpider(CrawlSpider):
    name = 'multi'
    allowed_domains = ('www.veronikamaine.com.au',)
    rules = [Rule(LinkExtractor(allow=r'/Stores'), follow=True, callback='parse_item')]
    start_urls = ('https://www.veronikamaine.com.au/Stores',)
    custom_settings = {'ROBOTSTXT_OBEY': False}

    def parse_item(self, response):
        item = RetailersItem()
        store_names_array = response.xpath('//div[@id="countryWrapper"]//ul/li//h2/text()').extract()
        addresses_array = response.xpath('//div[@id="countryWrapper"]//ul/li//address')
        phone_numbers_array = [item.strip() for item in response.xpath('//section[@class="storeListing"]//ul/li/div[@class="detailsMain"]/text()[normalize-space(.)]').extract()]
        opening_hours_array = response.xpath('//div[@id="countryWrapper"]//ul/li/div[@class="openingHours"]')

        for i, val in enumerate(phone_numbers_array):
            item['phone_number'] = val
            item['store_name'] = store_names_array[i]

            item['store_hours'] = opening_hours_array[i].xpath('normalize-space(.)').extract_first()
            # item['store_hours'] = store_hours_array[i].xpath('substring-after(normalize-space(.), "Opening Hours: ")').extract()

            item['address'] = ' '.join(addresses_array[i].xpath('.//p/text()').extract())

            suburbpostcode = addresses_array[i].xpath('./text()[normalize-space(.)]').extract_first().strip().split('  ')
            item['suburb'] = suburbpostcode[0]
            item['zip_code'] = suburbpostcode[1]

            # suburbpostcode = addresses_array[10].xpath('re:match(./text()[normalize-space(.)], "Castle (\w*)")/text()').extract()
            # for state in ['QLD', 'VIC', 'NSW', 'SA', 'WA', 'NT']:
            #     if state in item['address']:
            #         item['state'] = state
            yield item

    # latitude = scrapy.Field()
    # longitude = scrapy.Field()
