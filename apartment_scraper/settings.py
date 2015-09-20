# -*- coding: utf-8 -*-

# Scrapy settings for apartment_scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'apartment_scraper'

SPIDER_MODULES = ['apartment_scraper.spiders']
NEWSPIDER_MODULE = 'apartment_scraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'apartment_scraper (+http://www.yourdomain.com)'

LOG_FILE = "apartment_scraper.log"
ITEM_PIPELINES = {
    'apartment_scraper.pipelines.PostgresPipeline': 100,
}
