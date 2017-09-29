# -*- coding: utf-8 -*-
__author__ = 'chenjialin'
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
        items = self._initiem2()
        joburls = selector.xpath('//table[@class="va_list"]/tbody/tr[2]/td')

        url = self.preurl +  ''.join(joburls.xpath('a/@href').extract()[0])
        joburl = selector.xpath('//table[@class="va_list"]/tbody/tr[1]/td')
        urla = self.preurl +  ''.join(joburl.xpath('a/@href').extract()[0])
        print urla
        print url
        items["time"] = StrUtil.delWhiteSpace(url)
        yield Request(url, callback=self.duepdf, dont_filter=True)
        yield Request(urla, callback=self.duepdf, dont_filter=True)

    def duepdf(self, response):
        url = response.url
        items = self._initiem2()
        PDF_name = url.split('/')[-1]
        logger.debug("UNIDO-->job-->%s" % PDF_name)
        yield Request(url, meta={'PDF_name': PDF_name}, callback=self.savepdf, dont_filter=True)
        yield items

    def savepdf(self, response):
        PDF_name = response.meta['PDF_name']
        with open('../' + PDF_name +'.pdf', 'wb') as f:
            f.write(response.body)


    def _initiem2(self):
        items = UNFCCCjobsDataItem()
        items["time"] = ''
        items['englishname'] = 'UNFCCC'  # 组织英文缩写
        items['url'] = 'www.unfccc.org'  # 组织主页
        return items


