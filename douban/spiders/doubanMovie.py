# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from douban.items import DoubanItem


class DoubanmovieSpider(scrapy.Spider):
    name = "doubanMovie"
    allowed_domains = ["douban.com"]
    start_urls = (
        'http://movie.douban.com/top250',
    )
    pre_url = 'http://movie.douban.com/top250'

    def parse(self, response):
        movies_info = response.xpath('//div[@class="info"]')
        url_suffix = response.xpath('//span[@class="next"]/a/@href').extract()
        name = []
        if url_suffix:
            next_url = self.pre_url + url_suffix[0]
            yield Request(url=next_url, callback=self.parse)
        for m in movies_info:
            item = DoubanItem()
            item['title'] = m.xpath('.//span/text()').extract()[0].encode('utf8')
            item['score'] = m.xpath('.//span[@class="rating_num"]/text()').extract()[0].encode('utf8')
            info = m.xpath('.//div[@class="bd"]/p/text()').extract()
            for k, v in enumerate(info):
                info[k] = v.strip()
            item['movieInfo'] = '; '.join(info[:2]).encode('utf8')
            item['quote'] = m.xpath('.//p[@class="quote"]/span/text()').extract()[0].encode('utf8')
            yield item

