import scrapy


class DiscordBlogSpider(scrapy.Spider):
    name = 'discord_blog'
    base_url = 'https://discord.com'
    start_urls = ['https://discord.com/category/engineering']

    def parse(self, response):
        # Extract all links from the page
        links = response.css('a::attr(href)').extract()

        # Filter links that start with 'https://discord.com/blog/'
        filtered_links = [link for link in links if link.startswith('/blog/')]

        # Print the filtered links
        for link in filtered_links:
            self.logger.info(self.base_url + link)
