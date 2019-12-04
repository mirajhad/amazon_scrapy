# -*- coding: utf-8 -*-
import scrapy
from ..items import AmazonItem

class AmazonSpider(scrapy.Spider):
    name = 'Amazon'
    page_number = 2
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/b?ie=UTF8&node=17143709011']

    def parse(self, response):
        items = AmazonItem()

        product_name = response.css('.s-access-title::text').extract()
        product_author = response.css('.a-color-secondary .a-text-normal').css('::text').extract()
        product_price = response.css('.a-price-whole::text').extract()
        product_imagelink = response.css('.cfMarker::attr(src)').extract()

        items['product_name'] = product_name
        items['product_author'] = product_author
        items['product_price'] = product_price
        items['product_imagelink'] = product_imagelink

        yield items

        next_page = 'https://www.amazon.com/s?i=specialty-aps&srs=17143709011&page= ' + str(AmazonSpider.page_number) + ' &qid=1575368837&ref=sr_pg_2'
        if AmazonSpider.page_number <= 10:
            AmazonSpider.page_number +=1
            yield response.follow(next_page, callback = self.parse)