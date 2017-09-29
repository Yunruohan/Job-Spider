# -*- coding: utf-8 -*-
__author__ = "sundongmei"
import scrapy
from src.main.python.util.common.strUtil import StrUtil
import logging.config
from src.main.python.util.io.FileUtil import FileUtil
from ..allitems.leaderitems import UNFCCCLeadersItem
logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu')

class UNECCCleaderSpider(scrapy.Spider):
    name = "UNFCCCLeaders"

    start_urls = ["http://unfccc.int/secretariat/executive_secretary/items/1200.php"]


    def parse(self, response):
        item = self._inititem()
        item["url"] = response.url
        selector = scrapy.Selector(response)

        work = selector.xpath('//td[@class="mT"]/div[2]/text()').extract()
        if work:
            item["work"]= StrUtil.delWhiteSpace(work[0])
            logger.debug('>>>UNFCCCleader>>>work>>>%s' % item["work"])
            yield item

        else:
            logger.error('爬取UNFCCC领导人信息失败')

        experience = selector.xpath('//td[@class="mT"]/div[4]').extract()
        if experience:
            item["experience"] = StrUtil.delWhiteSpace(experience[0])
            logger.debug('>>>UNFCCCleader>>>experience>>>%s' % item["experience"])
            yield item

        else:
            logger.error('爬取UNFCCC领导人信息失败')

        section = selector.xpath('//td[@class="mT"]/div[6]/text()').extract()
        if section:
            item["section"] = StrUtil.delWhiteSpace(section[0])
            logger.debug('>>>UNFCCCleader>>>section>>>%s' % item["section"])
            yield item

        else:
            logger.error('爬取UNFCCC领导人信息失败')

        introduction = selector.xpath('//td[@class="mT"]/div[8]/text()').extract()
        if introduction:
            item["introduction"] = StrUtil.delWhiteSpace(introduction[0])
            logger.debug('>>>UNFCCCleader>>>introduction>>>%s' % item["introduction"])
            yield item

        else:
            logger.error('爬取UNFCCC领导人信息失败')


    def _inititem(self):
        '''
        初始化全部字段
        :return: 初始字段
        '''
        item = UNFCCCLeadersItem()
        item["work"] = ""
        item["experience"] = ""
        item["section"] = ""
        item["introduction"] = ""
        item["englishname"] = "UNFCCC"
        item["url"] = ""
        logger.info('初始化UNFCCC领导人item成功')
        return item
