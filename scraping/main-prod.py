import json
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from scrapy.utils.reactor import install_reactor
install_reactor('twisted.internet.epollreactor.EPollReactor')
from twisted.internet import reactor,defer
from scraping.spiders.blogSpider import BlogSpider


@defer.inlineCallbacks                       
def crawl(runner):
    with open('blogs.json', 'r') as f:
        BLOGS = json.load(f)
    for blog in BLOGS:
        yield runner.crawl(BlogSpider, blog_name=blog, **BLOGS[blog])
    reactor.stop()

def scraper(event, context):
    configure_logging(get_project_settings())
    runner = CrawlerRunner(get_project_settings())
    crawl(runner)
    reactor.run()
    return "Success"