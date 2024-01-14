import scrapy
from scraping.items import BlogArticle
from urllib.parse import urlunparse
from dateutil import parser
from datetime import datetime
import logging


class BlogSpider(scrapy.Spider):
    name = "engblog"

    def __init__(self, date=None, *args, **kwargs):
        super(BlogSpider, self).__init__(*args, **kwargs)
        self.date = date

    def start_requests(self):
        yield scrapy.Request(self.start_url, self.parse)

    def parse(self, response):
        selectors = response.xpath(self.blog_url_xpath)
        for selector in selectors:
            blog_path = selector.get()
            blog_url = (
                blog_path
                if blog_path.startswith("https")
                else urlunparse(("https", self.domain, blog_path, "", "", ""))
            )
            yield scrapy.Request(
                blog_url,
                callback=self.getDetails,
            )

    def getDetails(self, response):
        title = response.xpath("//meta[@property='og:title']/@content").get()
        description = response.xpath(
            "//meta[@property='og:description']/@content"
        ).get()
        image = response.xpath("//meta[@property='og:image']/@content").get()
        date = self.getDate(response)
        yield BlogArticle(
            blog_name=self.blog_name,
            url=response.url,
            title=title,
            description=description,
            image=image,
            date=date,
        )

    def getDate(self, response):
        datetime_str = response.xpath(
            "//meta[@property='article:published_time']/@content"
        ).get()
        if not datetime_str:
            datetime_str = response.xpath(self.date).get()
        datetime_obj = parser.parse(datetime_str, ignoretz=True, default=datetime.now())
        return datetime_obj.date()
