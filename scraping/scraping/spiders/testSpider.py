import scrapy
from scrapy.linkextractors import LinkExtractor
from scraping.items import BlogArticle
from scraping.utils import blogs


class BlogSpider(scrapy.Spider):
    name = 'engblog'
    BLOGS = blogs
    start_urls = list(BLOGS.keys())

    def parse(self, response):
        blog = self.BLOGS[response.url]
        link_extractor = LinkExtractor(
            allow=blog.get('allow', None), deny=blog.get('deny', None),
            allow_domains=blog.get('domain', None), restrict_css=blog.get('restrict_css', None))
        links = link_extractor.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url, callback=self.getDetails, cb_kwargs=dict(main_url=response.url))

    def getDetails(self, response, main_url):
        yield BlogArticle(url=response.url, date=self.getDate(
            response, main_url), title=self.getTitle(response, main_url))

    def getDate(self, response, main_url):
        query = self.BLOGS[main_url].get('date', '//@datetime')
        return response.xpath(query).get()

    def getTitle(self, response, main_url):
        url = response.url
        url_parts = url.split('/')
        title_with_hyphens = url_parts[-2] if url.endswith(
            '/') else url_parts[-1]
        title_words = title_with_hyphens.split('-')
        rawTitle = ' '.join(title_words)
        return self.BLOGS[main_url]['title'](rawTitle) if 'title' in self.BLOGS[main_url].keys() else rawTitle
