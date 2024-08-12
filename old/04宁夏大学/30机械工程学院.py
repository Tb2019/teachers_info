import re
from urllib import parse

from lxml import etree

from crawler import ReCrawler

school_name = '宁夏大学'
college_name = '机械工程学院'
school_id = 4
college_id = 30
start_urls = ['https://jxgc.nxu.edu.cn/szdw1/ljrc1.htm',
              'https://jxgc.nxu.edu.cn/szdw1/gccrc.htm',
              'https://jxgc.nxu.edu.cn/szdw1/zrjs.htm',
              'https://jxgc.nxu.edu.cn/szdw1/yjsds2.htm',
              'https://jxgc.nxu.edu.cn/szdw1/wpds.htm',
              'https://jxgc.nxu.edu.cn/szdw1/xzjfjs.htm'
              ]

a_s_xpath_str = '//div[@id="vsb_content_501_2151_u121" or @id="vsb_content_501_2155_u121" or @id="vsb_content_501_1097_u121" or @id="vsb_content_501_5545_u121"]//a[@href!="#"]'
target_div_xpath_str = '//form[@name="_newscontent_fromname"]'
# # 研究方向
# directions_pattern_list = [
#                             re.compile(r'', re.S),
#                             re.compile(r'', re.S)
#                           ]
# # 简介
# abstracts_pattern_list = [
#                             re.compile(r'', re.S),
#                             re.compile(r'', re.S)
#                           ]
# # 办公地点
# office_address_pattern_list = [
#                                 re.compile(r'', re.S)
#                               ]
# # 在职信息
# job_information_pattern_list = [
#                                 re.compile(r'', re.S)
#                               ]
# # 主要任职
# responsibilities_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]
# # 教育经历
# education_experience_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]
#
# # 工作经历
# work_experience_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]
# # 专利
# patent_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]
# # 科研项目
# project_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]
# # 奖励/荣誉
# award_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]
# # 社会兼职
# social_job_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]

class SpecialSpider(ReCrawler):
    def parse_index(self, index_page, url):
        page = etree.HTML(index_page)
        if url in ['https://jxgc.nxu.edu.cn/szdw1/zrjs.htm', 'https://jxgc.nxu.edu.cn/szdw1/yjsds2.htm']:
            a_s = page.xpath('//div[@class="szb"]//div[@class="name"]//ul//li//a[@href!="#"]')
        else:
            a_s = page.xpath(self.a_s_xpath_str)
        for a in a_s:
            name = a.xpath('.//text()')
            if name:
                name = ''.join(name)
                name = re.sub(r'\s*', '', name)
                name = re.sub(self.name_filter_re, '', name)
                link = a.xpath('./@href')[0]
                link = parse.urljoin(url, link)
            else:
                continue
            yield name, link

spider = SpecialSpider(
                   school_name=school_name,
                   college_name=college_name,
                   school_id=school_id,
                   college_id=college_id,
                   name_filter_re=r'导师简介',
                   start_urls=start_urls,
                   a_s_xpath_str=a_s_xpath_str,
                   target_div_xpath_str=target_div_xpath_str,
                   # directions_pattern_list=directions_pattern_list,
                   # abstracts_pattern_list=abstracts_pattern_list,
                   # office_address_pattern_list=office_address_pattern_list,
                   # job_information_pattern_list=job_information_pattern_list,
                   # responsibilities_pattern_list=responsibilities_pattern_list,
                   # education_experience_pattern_list=education_experience_pattern_list,
                   # work_experience_pattern_list=work_experience_pattern_list,
                   # patent_pattern_list=patent_pattern_list,
                   # project_pattern_list=project_pattern_list,
                   # award_pattern_list=award_pattern_list,
                   # social_job_pattern_list=social_job_pattern_list,
                   save2target='simple'
                   )

spider.run()


