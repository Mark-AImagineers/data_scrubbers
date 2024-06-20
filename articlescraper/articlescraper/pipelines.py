# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
import os
import dj_database_url
import logging

logger = logging.getLogger(__name__)

class PostgresPipeline(object):
    def open_spider(self, spider):
        on_heroku = 'DATABASE_URL' in os.environ
        if on_heroku:
            # Use the database URL from the environment variable (Heroku)
            database_url = dj_database_url.parse(os.environ['DATABASE_URL'])
            self.connection = psycopg2.connect(
                dbname=database_url['NAME'],
                user=database_url['USER'],
                password=database_url['PASSWORD'],
                host=database_url['HOST'],
                port=database_url['PORT'],
                sslmode='require'
            )
        else:
            # Use local database settings
            self.connection = psycopg2.connect(
                dbname='datascrub',
                user='postgres',
                password='0902',
                host='db',  # Docker compose service name
                port='5432',
                sslmode='disable'
            )
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        if spider.name == "inquirerspider":
            table_name = "scrubbers_politicalnews"
        elif spider.name == "businessinq":
            table_name = "scrubbers_businessnews"
        elif spider.name == "technologyinq":
            table_name = "scrubbers_technologynews"
        
        self.cur.execute(
            f"SELECT url FROM {table_name} WHERE url = %s",
            (item['url'],)
        )
        result = self.cur.fetchone()
        if result:
            logger.info(f"Duplicate item found: {item['url']} skipping...")
            return item  # Skip the item if it already exists

        # If not found, insert the new item
        self.cur.execute(
            f"INSERT INTO {table_name} (title, url, publication_date, author, full_text, country, source) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (item['title'], item['url'], item['date'], item['author'], item['full_text'], item['country'], item['source'])
        )
        logger.info(f"Item added to database {table_name}: {item['url']}")
        self.connection.commit()
        return item

class ArticlescraperPipeline:
    def process_item(self, item, spider):
        return item
