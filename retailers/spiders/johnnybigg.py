# for extracting info in magento site pages recursively.
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import json

from retailers.items import RetailersItem


class JohnnyBiggSpider(CrawlSpider):
    name = 'johnnybigg'
    allowed_domains = ('www.johnnybigg.com.au',)
    rules = [Rule(LinkExtractor(), follow=True, callback='parse_item')]
    start_urls = ('https://www.johnnybigg.com.au/au/',)

    def parse_item(self, response):
        if '/store/' not in response.url:
            return

        item = RetailersItem()
        data = json.loads(response.xpath('//div[@class="store-locator-content"]/@data-mage-init').extract_first())
        hours = re.findall('([\d:]+[ap]m\W*[\d:]+[ap]m)', data['store']['dates']['oh'])
        days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        if hours:
            for index, dayhour in enumerate(hours):
                hours[index] = days[index] + ' ' + dayhour
            item['store_hours'] = ', '.join(hours)
        item['phone_number'] = response.xpath('//main[@id="maincontent"]//div[@class="store-locator-content-info"]//div[@class="contact"]//text()').extract_first()
        item['store_name'] = response.xpath('//main[@id="maincontent"]//span[@data-ui-id="page-title-wrapper"]/text()').extract_first()
        item['address'] = response.xpath('//main[@id="maincontent"]//span[@data-ui-id="page-title-wrapper"]/text()').extract_first()
        for state in ['QLD', 'VIC', 'NSW', 'SA', 'WA', 'NT']:
            if state in item['address']:
                item['state'] = state
        yield item
