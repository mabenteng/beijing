# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ThtItem(scrapy.Item):
    # define the fields for your item here like:
    securities = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    job_addr = scrapy.Field()
    job_category = scrapy.Field()
    publish_time = scrapy.Field()
    department = scrapy.Field()
    job_number = scrapy.Field()
    job_education = scrapy.Field()
    end_time = scrapy.Field()
    others = scrapy.Field()
    source_url = scrapy.Field()
    # pass
