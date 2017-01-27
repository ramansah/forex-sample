import scrapy
from scrapy.crawler import CrawlerProcess


class ForexScraper(scrapy.Spider):

    name = 'forex'

    def start_requests(self):
        yield scrapy.Request(url='http://www.xe.com', callback=self.parse)

    def parse(self, response):
        currency_list = response.selector.xpath("//table[@id='xRatesBxTable']").xpath('tr/th/a/text()').extract()[1:]
        rate_list = list()
        rate_cell = response.selector.xpath("//table[@id='xRatesBxTable']").css('.liveRatesRw')[0].css('.rateCell')
        for cell in rate_cell[1:]:
            entry = cell.xpath('a/text()')
            if len(entry) == 0:
                entry = cell.xpath('div/text()')
            rate = entry.extract()[0]
            rate_list.append(rate)
        data = dict(zip(currency_list, rate_list))
        print(data)


def run_spider():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(ForexScraper)
    process.start()

run_spider()