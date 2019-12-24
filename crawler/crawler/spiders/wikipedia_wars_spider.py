# -*- coding: utf-8 -*-
import scrapy
import copy
from scrapy import Request
from crawler.items import WarItem

class WikipediaWarsSpiderSpider(scrapy.Spider):
    name = 'wikipedia_wars_spider'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Timeline_of_wars']

        
    def parse_extra_data(self,response):
        warItem = response.meta['item']
        
        if warItem['war_name'] in response.text and "Wikipedia does not have an article with this exact name" not in response.text:
            warItem['death_number'] = list(map(lambda i: i.replace('\n','') , list(filter(lambda i: i!=' ' and i!='' and i!='\n',response.xpath('//tr[contains(string(.),"Casualties and losses")]/following-sibling::tr/td/text()').extract()))))
            warItem['location_name'] = response.xpath('string(//div[@class="location"])').extract()[0]

        return warItem


    def parse(self, response):
        #crawl war lists by date
        if "timeline of wars" in response.text:

            warLists = response.xpath('//ul[1]/li/a[@class="mw-redirect"]')
            
            for warList in warLists:
                warListUrl = 'https://en.wikipedia.org'+ warList.xpath('./@href').extract()[0]
                yield Request(warListUrl)

        #crawl specified wars
        else:
            warItem = WarItem()
            wars = response.xpath('//table[@class="wikitable"]/tbody/tr')[2:]

            for war in wars:
                w = war.xpath('./td')
                if w==[]:
                    continue
                warItem['start_year_date'] = w[0].xpath('.//text()').extract()[0].replace('\n','')
                warItem['end_year_date'] = w[1].xpath('.//text()').extract()[0].replace('\n','')
                warItem['war_name'] = ''.join(w[2].xpath('.//text()').extract()).replace('\n','')
                warItem['win_country_name'] = list(filter(lambda i:i!=' ' and i!= '' and i!=  '\xa0' and i!= ' (ELN)' and i!=  ' (EPL)' and i not in '1234567890 ():  '  ,list((map( lambda i: i.replace('\n','') ,w[3].xpath('.//text()').extract())))))
                warItem['defeated_country_name'] = list(filter(lambda i:i!=' ' and i!= '' and i!=  '\xa0' and i!= ' (ELN)' and i!=  ' (EPL)' and i not in '1234567890 ():  '  ,list((map( lambda i: i.replace('\n','') ,w[4].xpath('.//text()').extract())))))
                warItem['death_number'] = 'Unkown'
                warItem['location_name'] = 'Unkown'

                warUrl = w.xpath('./a/@href').extract()
                if warUrl!=[]:
                    warUrl = 'https://en.wikipedia.org'+ warUrl[0]
                    yield scrapy.Request(url=warUrl,meta={'item':copy.deepcopy(warItem)},callback=self.parse_extra_data)
                else:
                    yield warItem
                
            
