from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraping.data import BLOGS

def lambda_function(event=None, context=None):
    process = CrawlerProcess(get_project_settings())
    for blog in BLOGS:
        process.crawl("blogSpider", blog_name=blog, **BLOGS[blog])
    process.start()
