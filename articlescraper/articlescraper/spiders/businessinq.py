import scrapy
import json
import logging

logger = logging.getLogger(__name__)


class BusinessinqSpider(scrapy.Spider):
    name = "businessinq"
    allowed_domains = ["business.inquirer.net"]

    def __init__(self, start_page=1, end_page=1, *args, **kwargs):
        super(BusinessinqSpider, self).__init__(*args, **kwargs)
        self.start_page = int(start_page)
        self.end_page = int(end_page)
        self.start_urls = [
            f"https://business.inquirer.net/category/business-headlines/page/{page}"
            for page in range(self.start_page, self.end_page + 1)
        ]
        logger.info(f"Scraping from {self.start_page} to {self.end_page} of Inquirer.net")

    def parse(self, response):
        articles = response.css('div#ch-ls-head')
        for article in articles:
            author_raw = article.css('div#ch-postdate span:last-child::text').get()
            author = author_raw.strip('BY: ').strip() if author_raw and 'BY:' in author_raw else 'Inquirer Philippines'

            item = {
                'title': article.css('div#ch-cat:contains("Headlines") + h2 a::text').get(),
                'url': article.css('div#ch-cat:contains("Headlines") + h2 a::attr(href)').get(),
                'date': article.css('div#ch-postdate span:first-child::text').get(),
                'author': author,
                'country': 'Philippines',
                'source': 'Inquirer.net'
            }

            if item['url']:
                yield response.follow(item['url'], self.parse_article, meta={'item': item})

    def parse_article(self, response):
        item = response.meta['item']
        script = response.xpath('//script[@type="application/ld+json"]/text()').get()
        if script:
            script_clean = script.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
            try:
                data = json.loads(script_clean)
                item['full_text'] = data.get('articleBody', 'No article body found.')
                print(item)
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON decode error at {response.url}: {str(e)}")
                item['full_text'] = 'Error decoding JSON'
            yield item
