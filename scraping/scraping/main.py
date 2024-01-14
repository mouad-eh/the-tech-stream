from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from utils import blogs
import argparse


parser = argparse.ArgumentParser()

parser.add_argument("--all", action="store_true")
parser.add_argument("--blog", type=str)

args = parser.parse_args()

process = CrawlerProcess(get_project_settings())

if args.all:
    for blog in blogs:
        process.crawl("engblog", blog_name=blog, **blogs[blog])
if args.blog:
    process.crawl("engblog", blog_name=args.blog, **blogs[args.blog])

process.start()
