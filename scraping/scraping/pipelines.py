from itemadapter import ItemAdapter
import psycopg2
from urllib.parse import urlparse
import os


class ScrapingPipeline:
    CREATE_TABLE1_QUERY = """
        CREATE TABLE IF NOT EXISTS blog_articles (
            id SERIAL PRIMARY KEY,
            blog_name VARCHAR(255),
            url VARCHAR(255),
            title VARCHAR(255),
            description TEXT,
            image VARCHAR(255),
            date DATE
        );
    """
    CREATE_TABLE2_QUERY = """
        CREATE TABLE IF NOT EXISTS latest_blog_article (
            id SERIAL PRIMARY KEY,
            blog_name VARCHAR(255),
            title VARCHAR(255),
            date DATE
        );
    """

    def __init__(self):
        self.items = []

    def open_spider(self, spider):
        connection_string = os.environ.get("DB_URI")
        url = urlparse(connection_string)
        self.conn = psycopg2.connect(
            dbname=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port,
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute(ScrapingPipeline.CREATE_TABLE1_QUERY)
        self.cursor.execute(ScrapingPipeline.CREATE_TABLE2_QUERY)

    def process_item(self, item, spider):
        self.items.append(item)
        return item

    def close_spider(self, spider):
        # get the latest blog article
        blog_name = self.items[0]["blog_name"]
        latest_blog_article = self.get_latest_blog_article(blog_name)

        # sort scraped blog articles chronologically
        sorted_items = sorted(self.items, key=lambda item: item["date"], reverse=True)

        # insert new blog articles only
        for item in sorted_items:
            if latest_blog_article and (
                (
                    item["title"] == latest_blog_article[0]
                    and item["date"] == latest_blog_article[1]
                )
                or item["date"] < latest_blog_article[1]
            ):
                break
            self.insert_item(item)

        # update/insert the latest blog article
        if not latest_blog_article:
            self.insert_latest_blog_article(blog_name, sorted_items[0])
        else:
            self.update_latest_blog_article(blog_name, sorted_items[0])

        # commit and close cursor & DB connection
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def get_latest_blog_article(self, blog_name):
        query = """
        SELECT title, date FROM latest_blog_article WHERE blog_name = %s;
        """
        self.cursor.execute(query, (blog_name,))
        return self.cursor.fetchone()

    def insert_item(self, item):
        query = """
        INSERT INTO blog_articles (blog_name, url, title, description, image, date)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        values = (
            item["blog_name"],
            item["url"],
            item["title"],
            item["description"],
            item["image"],
            item["date"],
        )
        self.cursor.execute(query, values)

    def insert_latest_blog_article(self, blog_name, latest_item):
        query = """
        INSERT INTO latest_blog_article (blog_name, title, date) VALUES (%s, %s, %s);
        """
        self.cursor.execute(
            query,
            (
                blog_name,
                latest_item["title"],
                latest_item["date"],
            ),
        )

    def update_latest_blog_article(self, blog_name, latest_item):
        query = """
        UPDATE latest_blog_article
        SET title = %s, date = %s
        WHERE blog_name = %s
        """
        self.cursor.execute(
            query,
            (
                latest_item["title"],
                latest_item["date"],
                blog_name,
            ),
        )
