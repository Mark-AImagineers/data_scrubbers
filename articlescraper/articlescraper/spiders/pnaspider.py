import scrapy
import json
import logging

logger = logging.getLogger(__name__)

class PnaspiderSpider(scrapy.Spider):
    name = "pnaspider"
    allowed_domains = ["pna.gov.ph"]
    start_urls = ["https://pna.gov.ph"]

    def parse(self, response):
        pass
