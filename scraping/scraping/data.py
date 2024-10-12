BLOGS = {
    "discord": {
        "domain": "discord.com",
        "start_url": "https://discord.com/category/engineering",
        "blog_url_xpath": "//div[@class='blog-featured-section']//div[@role='listitem']/a/@href",
        "date": "//div[@class='blog-post-author-name']/text()",
    },
    "cloudflare": {
        "domain": "blog.cloudflare.com",
        "start_url": "https://blog.cloudflare.com/tag/developers/",
        "blog_url_xpath": "//main//article/div/a[1]/@href | //main//article/a/@href",
        "date": "//article/p/text()",
    },
    "shopify": {
        "domain": "shopify.engineering",
        "start_url": "https://shopify.engineering/latest",
        "blog_url_xpath": "//article/div/div[2]/a/@href",
        "date": "//time/text()",
    },
    "stripe": {
        "domain": "stripe.com",
        "start_url": "https://stripe.com/blog/engineering",
        "blog_url_xpath": "//article/h1/a/@href",
        "date": "//@datetime",
    },
    "github": {
        "domain": "github.blog",
        "start_url": "https://github.blog/category/engineering/",
        "blog_url_xpath": "//article//h3/a/@href",
        "date": "//@datetime",
    },
    "uber": {
        "domain": "www.uber.com",
        "start_url": "https://www.uber.com/en-ES/blog/engineering/",
        "blog_url_xpath": "//a[@data-baseweb='card']/@href",
        "date": "//span[@class='b5 gt b7 ff hc']/text()",
    },
    "linkedin": {
        "domain": "www.linkedin.com",
        "start_url": "https://www.linkedin.com/blog/engineering/",
        "blog_url_xpath": "//div[@id='all-posts']//li/div[@class='grid-post__title']/a/@href",
        "date": "//@data-published-date",
    },
    "facebook": {
        "domain": "engineering.fb.com",
        "start_url": "https://engineering.fb.com/",
        "blog_url_xpath": "//article/a/@href",
        "date": "//@datetime",
    },
    "spotify": {
        "domain": "engineering.atspotify.com",
        "start_url": "https://engineering.atspotify.com/",
        "blog_url_xpath": "//article//h2/a/@href",
        "date": "//span[@class='date']/text()",
    },
}
