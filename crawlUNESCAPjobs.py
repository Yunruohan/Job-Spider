# -*- coding: utf-8 -*-
__author__ = "sundongmei"
from src.main.python.util.io.FileUtil import FileUtil
from src.main.python.dao.jobDao.CsvCao import SaveToCsv
from src.main.python.util.common.strUtil import StrUtil
from selenium import webdriver
from scrapy.http import HtmlResponse
import time
import re
import logging.config
logging.config.fileConfig(FileUtil().getLogConfigPath())
logger = logging.getLogger('ahu')
UNESCAPJobsPath = u"UNESCAP.csv"

class UNESCAPJOBSpider(object):
    def __init__(self):
        self.driver = webdriver.Chrome()

    def start(self):

        self.driver.get('http://www.unescap.org/jobs')
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        time.sleep(3)

        if 'Job' in self.driver.page_source:
            response = HtmlResponse(url="my HTML string", body=self.driver.page_source, encoding="utf-8")
            links = response.xpath('//div[@class="view-content"]/table/tbody/tr/td[2]/a/@href').extract()
            logger.info("UNESCAP共" + str(len(links)) + "条网页待爬")
            items = []
            for link in links:
                logger.debug("UNESCAP待爬岗位:  " + link)
                url = link
                self.driver.get(url)
                time.sleep(3)
                item = self._parse(self.driver.page_source,url)
                if item not in items:
                    logger.debug("页面%s爬取成功"%url)
                    items.append(item)


            logger.debug("共爬取UNESCAP岗位数据%d条"%len(items))
            saveToCsv = SaveToCsv()
            saveToCsv.saveUNESCAPjobs(UNESCAPJobsPath, items)
        else:
            self.start()

    def _parse(self, page_sourse, url):
        item={}
        item["url"] = "http://www.unescap.org/jobs"

        response = HtmlResponse(url="my HTML string", body=page_sourse, encoding="utf-8")
        workinfo = response.xpath('//div[@id="win0divHRS_JO_WRK_POSTING_TITLE$0"]')
        work = workinfo.xpath('string(.)').extract()[0]
        item["work"] = re.sub('\W', '', work.split('-')[0])  # 岗位
        logger.debug('>>UNESCAP>>JOB>>work>>%s' % item["work"])



        jobcodeinfo = response.xpath('//div[@id="win0divHRS_JO_WRK_UN_LGDESCR"]')
        jobcode = jobcodeinfo.xpath('string(.)').extract()[0]
        item["jobcode"] = re.sub('\W','',jobcode.split('-')[0])  # 工作性质
        logger.debug('>>UNESCAP>>JOB>>jobcode>>%s' % item["jobcode"])

        sectorinfo = response.xpath('//div[@id="win0divUN_SHRCO_WRK_UN_LGDESCR$0"]')
        sector = sectorinfo.xpath('string(.)').extract()[0]
        item["sector"] = sector  # 部门
        logger.debug('>>UNESCAP>>JOB>>sector>>%s' % item["sector"])

        stationinfo = response.xpath('//div[@id="win0divHRS_CE_WRK2_HRS_CE_JO_LCTNS$0"]')
        station = stationinfo.xpath('string(.)').extract()[0]
        item["station"] = station #工作地点
        logger.debug('>>UNESCAP>>JOB>>station>>%s' % item["station"])

        posttimeinfo = response.xpath('//div[@id="win0divUN_SHRCO_WRK_DESCR50$0"]')
        posttime = posttimeinfo.xpath('string(.)').extract()[0]
        item["posttime"] = posttime #发布时间
        logger.debug('>>UNESCAP>>JOB>>posttime>>%s' % item["posttime"])

        numberinfo = response.xpath('//div[@id="win0divUN_SHRCO_WRK_UN_VA_NBR$0"]')
        number = numberinfo.xpath('string(.)').extract()[0]
        item["number"] = number #招聘人数
        logger.debug('>>UNESCAP>>JOB>>number>>%s' % item["number"])

        jobidinfo = response.xpath('//div[@id="win0divUN_SHRCO_WRK_UN_SE_ID_DESCR$0"]')
        jobid = jobidinfo.xpath('string(.)').extract()[0]
        item["jobid"] = jobid #工作编号
        logger.debug('>>UNESCAP>>JOB>>jobid>>%s' % item["jobid"])
        return item

    def depose(self):
        self.driver.close()
if __name__=="__main__":
    uNESCAPJobSpider = UNESCAPJOBSpider()
    uNESCAPJobSpider.start()
    uNESCAPJobSpider.depose()