import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes_spider"

    def start_requests(self):
        urls = [
            "http://quotes.toscrape.com/page/1/",
            # "http://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page_id = response.url.split('/')[-2]
        filename = f"quotes-{page_id}.html"
        for q in response.css('div.quote'):
            # quote = q.css('span.text::text').get()
            # author = q.css('small.author::text').get()
            # tags = q.css('a.tag::text').getall()
            # scrapy crawl quotes_spider -o quotes.json -> using this terminal to make
            yield{
                'quote': q.css('span.text::text').get(),
                'author': q.css('small.author::text').get(),
                'tags': q.css('a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

            # yield response.follow(next_page, callback=self.parse)
            # with open(filename, 'wb') as f:
            #     f.write(response.body)
            # self.log(f'Saved file{filename}')
