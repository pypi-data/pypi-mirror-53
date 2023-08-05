# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.utils.spider import iterate_spider_output
from scrapy.exceptions import NotConfigured, NotSupported
import xlrd
import logging
logger = logging.getLogger(__name__)

def xlsiter(response, headers = None, sheet_index = 0):
    with xlrd.open_workbook(file_contents=response.body) as wb:
        sh = wb.sheet_by_index(sheet_index)
        if sh.nrows > 0:
            start_line = 0
            if not headers:
                headers = sh.row_values(0)
                start_line = 1
            for i in range(start_line, sh.nrows):
                row = sh.row_values(i)
                if len(headers) != len(row):
                    logger.warning("ignoring row %(csvlnum)d (length: %(csvrow)d, "
                            "should be: %(csvheader)d)",
                            {'csvlnum': i + 1, 'csvrow': len(row),
                             'csvheader': len(headers)})
                    continue
                else:
                    yield dict(zip(headers, row))

class XLSFeedSpider(Spider):
    headers = None
    sheet_index = 0
    def adapt_response(self, response):
        return response

    def process_result(self, response, results):
        return results

    def parse_row(self, response, row):
        raise NotImplementedError

    def parse_rows(self, response):
        for row in xlsiter(response, self.headers, self.sheet_index):
            ret = iterate_spider_output(self.parse_row(response, row))
            for result_item in self.process_result(response, ret):
                yield result_item

    def parse(self, response):
        if not hasattr(self, 'parse_row'):
            raise NotConfigured('You must define parse_row method in order to scrape this XLS feed')
        response = self.adapt_response(response)
        return self.parse_rows(response)
