import scrapy
from scrapy.linkextractors import LinkExtractor
from scraping.items import BlogArticle


class BlogRules:
    def __init__(self, domain, allow, deny, restrict_css=None):
        self.domain = domain
        self.allow = allow
        self.deny = deny
        self.restrict_css = restrict_css


class BlogSpider(scrapy.Spider):
    name = 'engblog'
    start_urls = [  # 'https://discord.com/category/engineering',
        #   'https://blog.cloudflare.com/tag/developers/',
        #   'https://shopify.engineering/',
        'https://stripe.com/blog/engineering',
        #   'https://github.blog/category/engineering/',
        #   'https://www.uber.com/en-ES/blog/engineering/',
        #   'https://engineering.linkedin.com/blog',
        #   'https://engineering.fb.com/',
        #   'https://engineering.atspotify.com/'
    ]
    blogs = {
        'https://discord.com/category/engineering': BlogRules(
            domain="discord.com",
            allow=["/blog/"],
            deny=[]
        ),
        'https://blog.cloudflare.com/tag/developers/': BlogRules(
            domain="blog.cloudflare.com",
            allow=[],
            deny=['/tag/', '/search/', '/author/',
                  '^https://blog.cloudflare.com/$', 'https://blog.cloudflare.com/([a-z]{2}-[a-z]{2})']),
        'https://shopify.engineering/': BlogRules(
            domain="shopify.engineering", allow=[],
            deny=["^https://shopify.engineering/$", "^https://shopify.engineering/work-with-us$",
                  "^https://shopify.engineering/sponsorship$",
                  "/topics/", "/search?", "/?page", "/#"],
            restrict_css=['.grid__item--desktop-up-two-thirds']),
        'https://stripe.com/blog/engineering': BlogRules(
            domain="stripe.com",
            allow=['/blog/'],
            deny=['/blog/engineering', '/blog/feed.rss']
        ),
        'https://github.blog/category/engineering/': BlogRules(
            domain='github.blog',
            allow=['https://github.blog/\d{4}-\d{2}-\d{2}'],
            deny=[]
        ),
        'https://www.uber.com/en-ES/blog/engineering/': BlogRules(
            domain='www.uber.com',
            allow=['/en-ES/blog/'],
            deny=['/blog/engineering/', '/blog/ride/', '/blog/business/',
                  '/blog/careers/', '^https://www.uber.com/en-ES/blog/$']
        ),
        'https://engineering.linkedin.com/blog': BlogRules(
            domain='engineering.linkedin.com',
            allow=['/blog/\d{4}/'],
            deny=[]
        ),
        'https://engineering.fb.com/': BlogRules(
            domain='engineering.fb.com',
            allow=['/\d{4}/\d{2}/\d{2}'],
            deny=[]
        ),
        'https://engineering.atspotify.com/': BlogRules(
            domain='engineering.atspotify.com',
            allow=['/\d{4}/\d{2}'],
            deny=[]
        )
    }

    def parse(self, response):
        rules = self.blogs[response.url]
        link_extractor = LinkExtractor(
            allow=rules.allow, deny=rules.deny, allow_domains=rules.domain, restrict_css=rules.restrict_css)
        links = link_extractor.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url, self.getDetails)

    def getDetails(self, response):
        yield BlogArticle(url=response.url, date=self.getDate(
            response), title=self.getTitle(response.url))

    def getDate(self, response):
        return response.xpath('//@datetime').get()

    def getTitle(self, url):
        url_parts = url.split('/')
        title_with_hyphens = url_parts[-1]
        title_words = title_with_hyphens.split('-')
        title = ' '.join(title_words)
        return title
