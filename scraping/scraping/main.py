from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from data import BLOGS
import argparse

# get arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument("--all", action="store_true")
parser.add_argument("--blog", type=str)
args = parser.parse_args()

# crawl a specific blog or all blogs based on argument
process = CrawlerProcess(get_project_settings())
if args.all:
    for blog in BLOGS:
        # we can consider parallelisme here
        process.crawl("blogSpider", blog_name=blog, **BLOGS[blog])
if args.blog:
    process.crawl("blogSpider", blog_name=args.blog, **BLOGS[args.blog])
process.start()
