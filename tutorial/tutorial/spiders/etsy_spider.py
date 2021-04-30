import scrapy
import pandas as pd

class EtsySpider(scrapy.Spider):
    name = "etsy"
    N = 20 # Max Links We'll Visit
    count = 0 # count of link visits

    def start_requests(self):
        urls = [
            'https://www.etsy.com/listing/665594678',
            'https://www.etsy.com/listing/515464712',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Increment to count by one:
        self.count += 1

        content = response.css('div#content.clear')
        listing_page_content = content.css('div.listing-page-content')
        listing_grid = listing_page_content.css('ul.responsive-listing-grid')

        next_page = None

        for link in listing_grid.css('div.js-merch-stash-check-listing'):
            # TODO: find where this html is in the browser using the developer tools or by inspecting the element
            next_page = link.css('a.listing-link::attr(href)').get()
            yield {
                'link': next_page,
                # TODO: find something else to output here
            }
            break #why???? What does this do?

        if next_page is not None and self.count <= self.N:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
