import scrapy
from scrapy.linkextractors import LinkExtractor
from scraping.items import BlogArticle
from dateutil import parser
from datetime import datetime


class BlogSpider(scrapy.Spider):
    name = "engblog"

    def __init__(
        self,
        start_url=None,
        domain=None,
        allow=None,
        deny=None,
        restrict_css=None,
        date=None,
        title=None,
        *args,
        **kwargs
    ):
        super(BlogSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_url
        self.domain = domain
        self.allow = allow
        self.deny = deny
        self.restrict_css = restrict_css
        self.date = date
        self.title = title

    def start_requests(self):
        yield scrapy.Request(self.start_urls, self.parse)

    def parse(self, response):
        link_extractor = LinkExtractor(
            allow=self.allow,
            deny=self.deny,
            allow_domains=self.domain,
            restrict_css=self.restrict_css,
        )
        links = link_extractor.extract_links(response)
        for link in links:
            yield scrapy.Request(
                link.url,
                callback=self.getDetails,
            )

    def getDetails(self, response):
        yield BlogArticle(
            url=response.url,
            date=self.getDate(response),
            title=self.getTitle(response),
        )

    def getDate(self, response):
        query = self.date if self.date is not None else "//@datetime"
        rawDate = response.xpath(query).get()
        # default to get the current year when it is not specified in the rawDate
        parsedDateTime = parser.parse(rawDate, default=datetime.now())
        return parsedDateTime.date()

    def getTitle(self, response):
        url = response.url
        url_parts = url.split("/")
        title_with_hyphens = url_parts[-2] if url.endswith("/") else url_parts[-1]
        title_words = title_with_hyphens.split("-")
        rawTitle = " ".join(title_words)
        return self.title(rawTitle) if self.title is not None else rawTitle
