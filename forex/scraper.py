import scrapy
from scrapy.crawler import CrawlerProcess
from forex.config import SITE
from forex.db import Forex
from forex.db import load_data
import time


class ForexScraper(scrapy.Spider):

    name = 'forex'
    data = None
    time = None

    def start_requests(self):
        self.time = int(time.time() * 1000)
        yield scrapy.Request(url=SITE, callback=self.parse)

    def parse(self, response):
        currency_list = response.selector.xpath("//table[@id='xRatesBxTable']").xpath('tr/th/a/text()').extract()[1:]
        rate_list = list()
        rate_cell = response.selector.xpath("//table[@id='xRatesBxTable']").css('.liveRatesRw')[0].css('.rateCell')
        for cell in rate_cell[1:]:
            entry = cell.xpath('a/text()')
            if len(entry) == 0:
                entry = cell.xpath('div/text()')
            rate = float(entry.extract()[0])
            rate_list.append(rate)
        data = dict(zip(currency_list, rate_list))
        print(data)
        self.data = data
        self.load_in_db()

    def load_in_db(self):
        data_to_load = list()
        for key, value in self.data.items():
            forex = Forex(
                currency=key,
                rate=value,
                time=self.time
            )
            data_to_load.append(forex)
        load_data(data_to_load)


def run_spider():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(ForexScraper)
    process.start()


if __name__ == '__main__':
    run_spider()
