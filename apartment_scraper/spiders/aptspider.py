#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: aptspider.py
Author: zlamberty
Created: 2015-07-01

Description:
    web spider for apartment listings

    stolen shamelessly from:
    http://gabrielelanaro.github.io/blog/2015/04/24/scraping-data.html

Usage:
    <usage>

"""

import logging

from re import sub
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from apartment_scraper.items import AptListingsItem


logger = logging.getLogger(__name__)

# ----------------------------- #
#   Main class                  #
# ----------------------------- #

class RoomSpider(CrawlSpider):
    name = 'aptspider'

    def __init__(self, city='washingtondc'):
        super(RoomSpider, self).__init__()
        self.city = city
        self.allowed_domains = ['{}.craigslist.org'.format(self.city)]
        self.start_urls = [
            'https://{}.craigslist.org/search/apa{}'.format(self.city, tail)
            for tail in [''] + ['?s={}'.format(el * 100) for el in range(1, 25)]
        ]

    rules = (
        Rule(
            LinkExtractor(allow=[r'.*?/.+?/apa/\d+\.html']),
            callback="parse_apa",
            follow=False
        ),
    )

    download_delay = 1

    def parse_apa(self, response):
        """ how should we parse apartment listings? """
        url = response.url
        titlebar =  ' '.join(
            el for el in response.xpath(
                '//*[@id="pagecontainer"]/section/h2/'
                '*[@class="postingtitletext"]/text()'
                '[normalize-space()]'
            ).extract()
            if el.strip()
        )
        price = float(
            sub(
                r'[^\d.]',
                '',
                response.xpath('//*[@class="price"]/text()').extract()[0]
            )
        )
        content = response.xpath('//*[@id="postingbody"]').extract()[0]
        maplink = response.xpath(
            '//*[@id="pagecontainer"]/section/section[@class="userbody"]/'
            'div[@class="mapAndAttrs"]/div/p/small/a[1]'
        ).extract()
        try:
            maplink = maplink[0]
        except:
            logger.warning("Unable to subset maplink for url {}".format(url))

        longitude = None
        latitude = None
        mapdata = response.xpath('//*[@id="map"]')
        if len(mapdata) != 0:
            longitude = float(mapdata.xpath("@data-longitude").extract()[0])
            latitude = float(mapdata.xpath("@data-latitude").extract()[0])

        attributes = [
            ''.join(a.xpath('.//text()').extract())
            for a in response.xpath(
                '//*[@id="pagecontainer"]/section/section[@class="userbody"]'
                '/div[@class="mapAndAttrs"]/p[@class="attrgroup"]/span'
            )
        ]

        imageLinks = response.xpath('//*[@id="thumbs"]/a/@href').extract()
        time = response.xpath(
            '//*[@id="display-date"]/time/@datetime'
        ).extract()[0]

        item = AptListingsItem()
        item['title'] = titlebar,
        item['city'] = self.city
        item['url'] = url
        item['price'] = price
        item['bedrooms'] = None
        item['maplink'] = maplink
        item['longitude'] = longitude
        item['latitude'] = latitude
        item['updated_on'] = time
        item['content'] = content
        item['image_links'] = imageLinks
        item['attributes'] = attributes
        item['size'] = None

        return item
