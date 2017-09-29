# -*- coding: utf-8 -*-
__author__ = 'sundongmei'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import logging.config
from scrapy.http import Request
from ..allitems.jobitems import UNFCCCjobsDataItem
from src.main.python.util.common.strUtil import StrUtil
from src.main.python.util.io.FileUtil import FileUtil
logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger("ahu")

class UNIDOjobLink(scrapy.Spider):
    name = "UNFCCCjobPDF"
    start_urls = ["https://unfccc.int/secretariat/employment/recruitment"]

    def __init__(self):
        self.preurl = 'http://unfccc.int'

    def parse(self, response):
        selector = scrapy.Selector(response)
        joburls = selector.xpath('//table[@class="va_list"]/tbody/tr[2]/td')
        url = self.preurl +  ''.join(joburls.xpath('a/@href').extract()[0])
        joburl = selector.xpath('//table[@class="va_list"]/tbody/tr[1]/td')
        urla = self.preurl +  ''.join(joburl.xpath('a/@href').extract()[0])
        yield Request(url, callback=self.duepdf, dont_filter=True)
        yield Request(urla, callback=self.duepdf, dont_filter=True)

    def duepdf(self, response):
        url = response.url
        PDF_name = url.split('/')[-1]
        logger.debug("UNIDO-->job-->%s" % PDF_name)
        yield Request(url, meta={'PDF_name': PDF_name}, callback=self.savepdf, dont_filter=True)

    def savepdf(self, response):
        PDF_name = response.meta['PDF_name']
        with open('../' + PDF_name +'.pdf', 'wb') as f:
            f.write(response.body)




