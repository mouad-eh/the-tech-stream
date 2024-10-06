from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from scrapy.utils.reactor import install_reactor
install_reactor('twisted.internet.epollreactor.EPollReactor')
from twisted.internet import reactor,defer
import argparse
from scraping.spiders.blogSpider import BlogSpider
from scraping.data import BLOGS

configure_logging(get_project_settings())
runner = CrawlerRunner(get_project_settings())

@defer.inlineCallbacks                       
def crawl(args):
    if args.all:
        for blog in BLOGS:
            yield runner.crawl(BlogSpider, blog_name=blog, **BLOGS[blog])
        reactor.stop()
    if args.blog:
        yield runner.crawl(BlogSpider, blog_name=args.blog, **BLOGS[args.blog])
        reactor.stop()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--blog", type=str)
    args = parser.parse_args()

    crawl(args)
    reactor.run()

if __name__ == "__main__":
    main()
