# -*- coding: utf-8 -*-
__author__ = "sundongmei"
import scrapy
from src.main.python.util.common.strUtil import StrUtil
import logging.config
from src.main.python.util.io.FileUtil import FileUtil
from ..allitems.leaderitems import UNESCAPLeadersItem
logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu')

class UNESCAPleadersSpider(scrapy.Spider):
    name = "UNESCAPleaders"

    start_urls = ["http://www.unescap.org/about/secretariat"]

    def parse(self, response):
        item = self._inititem()
        item["url"] = response.url
        selector = scrapy.Selector(response)

        datas = selector.xpath('//div[@class="profile-block"]')
        if datas:
            for data in datas[:-1]:

                ns = data.xpath('div[@class="profile-name"]').xpath('string(.)').extract()
                if ns:
                    if '-' in ns[0]:
                        item["name"] = StrUtil.delWhiteSpace(ns[0].split('-')[0])

                    else:
                        item["name"] = StrUtil.delWhiteSpace(ns[0].split('–')[0])


                work = data.xpath('div[@class="profile-title"]').xpath('string(.)').extract()
                if work:
                    item["work"] = StrUtil.delWhiteSpace(work[0])

                section = data.xpath('div[@class="profile-title-second"]').xpath('string(.)').extract()

                if section:
                    item["section"] = StrUtil.delWhiteSpace(section[0])

                logger.debug('>>>UNESCAPleader>>>name>>>%s' % item["name"])
                logger.debug('>>>UNESCAPleader>>>work>>>%s' % item["work"])
                logger.debug('>>>UNESCAPleader>>>section>>>%s' % item["section"])
                yield item
        else:
            logger.error('爬取UNESCAP领导人姓名和部门失败')


    def _inititem(self):
        '''
        初始化全部字段
        :return: 初始字段
        '''
        item = UNESCAPLeadersItem()
        item["work"] = ""
        item["name"] = ""
        item["section"] = ""
        item["englishname"] = "ESCAP"
        item["url"] = ""
        logger.info('初始化UNESCAP领导人item成功')
        return item
