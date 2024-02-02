# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
from psycopg2 import sql


class AutoRiaPipeline:

    def __init__(self):
        hostname = "localhost"
        username = "postgres"
        password = ""  # your password
        database = "AutoRiaDB"

        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

        self.cur = self.connection.cursor()

        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS cars(
                    id serial PRIMARY KEY, 
                    url text,
                    title text,
                    price_usd int,
                    odometer int,
                    username text,
                    phone_number bigint[],
                    image_url  text,
                    images_count   int,
                    car_number text,
                    car_vin text,
                    datetime_found timestamp DEFAULT CURRENT_TIMESTAMP
                )
                """)

    def process_item(self, item, spider):
        insert_query = sql.SQL("""
                    INSERT INTO cars (
                        url, title, price_usd, odometer, username,
                        phone_number, image_url, images_count,
                        car_number, car_vin
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """)

        self.cur.execute(insert_query, (
            item['url'], item['title'], item['price_usd'],
            item['odometer'], item['username'], item['phone_number'],
            item['image_url'], item['images_count'],
            item['car_number'], item['car_vin']
        ))

        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()
