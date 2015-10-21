# -*- coding: utf-8 -*-
__author__ = 'lkl'
from scrapy.contrib.spiders import BaseSpider
from emailspider.items import EmailspiderItem
from scrapy.http import Request

class EmailSpider(BaseSpider):

    name = "emails"
    allowed_domains = ["cantonfair110.mingluji.com"]
    start_urls = [
        'http://cantonfair110.mingluji.com/taxonomy/term/2'
    ]

    def parse(self,response):

        for info in response.xpath('//div[@typeof="sioc:Item foaf:Document"]'):
            item = EmailspiderItem()
            item['company'] = info.xpath('.//h2/a/text()').extract_first()
            item['email'] = info.xpath(".//span[@itemprop='email']/text()").extract_first()
            item['telephone'] = info.xpath(".//span[@itemprop='telephone']/text()").extract_first()
            item['country'] = info.xpath(".//a/span/a/text()").extract_first()
            yield item

        for url in response.xpath('//a[@title="Go to next page"]/@href').extract():
            yield Request(response.urljoin(url),callback=self.parse)
