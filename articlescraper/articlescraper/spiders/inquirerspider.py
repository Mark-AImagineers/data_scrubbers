import scrapy
import json


class InquirerspiderSpider(scrapy.Spider):
    name = "inquirerspider"
    allowed_domains = ["newsinfo.inquirer.net"]
    start_urls = ["https://newsinfo.inquirer.net/category/inquirer-headlines/nation"]

    def parse(self, response):
        articles = response.css('div#ch-ls-head')
        for article in articles:

            author_raw = article.css('div#ch-postdate span:last-child::text').get()
            if author_raw and 'BY:' in author_raw:
                author = author_raw.strip('BY: ').strip()
            else:
                author =  'Inquirer Philippines'

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
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON decode error at {response.url}: {str(e)}")
                item['full_text'] = 'Error decoding JSON'
            yield item


# response.css('div#ch-ls-head div#ch-cat:contains("Headlines") + h2 a::attr(href)').getall() -- this will get all the url links (headlines only not including trending)
# response.css('div#ch-ls-head div#ch-cat:contains("Headlines") + h2 a::text').get() -- this will get all the titles
# response.css('div#ch-ls-head div#ch-postdate span:first-child::text').get() -- this will get all article dates
# [author.strip('BY: ').strip() for author in response.css('div#ch-postdate span:last-child::text').getall()] -- this will get all article authors