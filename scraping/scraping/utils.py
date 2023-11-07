import re


def processGithubBlogTitle(rawTitle):
    date_pattern = re.compile(r'\b\d{4} \d{2} \d{2}\b')
    title = re.sub(date_pattern, '', rawTitle).strip()
    return title


blogs = {
    'https://discord.com/category/engineering': {
        'domain': ["discord.com"],
        'allow': ["/blog/"],
        'date': "//div[@class='blog-post-author-name']/text()"
    },
    'https://blog.cloudflare.com/tag/developers/': {
        'domain': ['blog.cloudflare.com'],
        'deny': ['/tag/', '/search/', '/author/', '^https://blog.cloudflare.com/$', 'https://blog.cloudflare.com/([a-z]{2}-[a-z]{2})']
    },
    'https://shopify.engineering/': {
        'domain': ["shopify.engineering"],
        'deny': ["^https://shopify.engineering/$", "^https://shopify.engineering/work-with-us$", "^https://shopify.engineering/sponsorship$", "/topics/", "/search?", "/?page", "/#"],
        'restrict_css': ['.grid__item--desktop-up-two-thirds']
    },
    'https://stripe.com/blog/engineering': {
        'domain': ["stripe.com"],
        'allow': ['/blog/'],
        'deny': ['/blog/engineering', '/blog/feed.rss']
    },
    'https://github.blog/category/engineering/': {
        'domain': ['github.blog'],
        'allow': ['https://github.blog/\d{4}-\d{2}-\d{2}'],
        'title': processGithubBlogTitle
    },
    'https://www.uber.com/en-ES/blog/engineering/': {
        'domain': ['www.uber.com'],
        'allow': ['/en-ES/blog/'],
        'deny': ['/blog/engineering/', '/blog/ride/', '/blog/business/', '/blog/careers/', '^https://www.uber.com/en-ES/blog/$'],
        'date': "//span[@class='b5 gt b7 ff hc']/text()"
    },
    'https://engineering.linkedin.com/blog': {
        'domain': ['engineering.linkedin.com'],
        'allow': ['/blog/\d{4}/'],
        'date': "//div[@class='date']/text()"
    },
    'https://engineering.fb.com/': {
        'domain': ['engineering.fb.com'],
        'allow': ['/\d{4}/\d{2}/\d{2}'],
    },
    'https://engineering.atspotify.com/': {
        'domain': ['engineering.atspotify.com'],
        'allow': ['/\d{4}/\d{2}'],
        'date': "//span[@class='date']/text()"
    }
}
