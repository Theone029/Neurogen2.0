import scrapy

class LeadsSpider(scrapy.Spider):
    name = 'leads'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/leads']

    def parse(self, response):
        for lead in response.css('div.lead'):
            yield {
                'name': lead.css('h2::text').get(),
                'email': lead.css('span.email::text').get(),
                'phone': lead.css('span.phone::text').get(),
            }
