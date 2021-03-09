import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import KombankrsItem
from itemloaders.processors import TakeFirst


class KombankrsSpider(scrapy.Spider):
	name = 'kombankrs'
	start_urls = ['https://www.kombank.com/sr/vesti']

	def parse(self, response):
		post_links = response.xpath('//div[@class="card-body"]/ul/li/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath(
			'//*[contains(concat( " ", @class, " " ), concat( " ", "vest", " " ))]//p//text()[normalize-space()]').getall()
		description = [remove_tags(p).strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="col-md-8 vest"]/div[@class="datum"]/text()').get()

		item = ItemLoader(item=KombankrsItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
