# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class CrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class Pipeline_ToCSV(object):
 
    def __init__(self):
        store_file ='/home/louie/Workspace/Web-Science/Data/wars.csv'
        self.file = open(store_file,'w')
        self.writer = csv.writer(self.file)
        self.writer.writerow(('win_country_name','defeated_country_name','start_year_date','end_year_date','location_name','death_number','war_name'))
        
    def process_item(self,item,spider):
        self.writer.writerow((item['win_country_name'],item['defeated_country_name'],item['start_year_date'],item['end_year_date'],item['location_name'], item['death_number'], item['war_name']))
        return item
    
    def close_spider(self,spider):
        self.file.close()
