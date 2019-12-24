# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class WarItem(scrapy.Item):
    war_name = scrapy.Field()
    start_year_date = scrapy.Field()
    end_year_date = scrapy.Field()
    win_country_name = scrapy.Field()
    defeated_country_name = scrapy.Field()
    death_number = scrapy.Field()
    location_name = scrapy.Field()
    
