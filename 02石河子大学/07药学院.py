import re
from crawler import ReCrawler
from lxml import etree
from urllib import parse


school_id = 2
college_id = 7
school_name = '石河子大学'
college_name = '药学院'
start_urls = ['https://yaoxy.shzu.edu.cn/sssds/list{i}.htm'.format(i=i+1) for i in range(6)]

a_s_xpath_str = '//div[@class="article_content"]//ul[@class="wp_article_list"]//li//a'
target_div_xpath_str = '//div[@class="article_content"]'
# 研究方向
directions_pattern_list = [
                            re.compile(r'研究方向(?::|：)?(.*?)\d.开设课程', re.S),
                            # re.compile(r'', re.S)
                          ]
# 简介
abstracts_pattern_list = [
                            re.compile(r'基本信息(?::|：)?(.*?)二、', re.S),
                            re.compile(r'基本信息(?::|：)?(.*?)2\.研究方向', re.S)
                          ]
# 办公地点
office_address_pattern_list = [
                                re.compile(r'通讯地址(?::|：)?(.*?)\d.邮编', re.S)
                              ]
# 在职信息
# job_information_pattern_list = [
#                                 re.compile(r'', re.S)
#                               ]
# 主要任职
# responsibilities_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]
# 教育经历
# education_experience_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]

# 工作经历
# work_experience_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]
# 专利
patent_pattern_list = [
                                    re.compile(r'发明专利(?::|：)?(.*?)\d.代表著作', re.S),
                                    # re.compile(r'', re.S)
                                ]
# 科研项目
project_pattern_list = [
                                    re.compile(r'主持科学研究项目(?::|：)?(.*?)三、', re.S),
                                    re.compile(r'', re.S)
                                ]
# 奖励/荣誉
# award_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]
# 社会兼职
social_job_pattern_list = [
                                    re.compile(r'社会兼职(?::|：)?(.*?)\d.联系方式', re.S),
                                    re.compile(r'', re.S)
                                ]


class Special_ReCrawler(ReCrawler):
    def parse_index(self, index_page, url):
        page = etree.HTML(index_page)
        a_s = page.xpath(self.a_s_xpath_str)
        for a in a_s:
            name = a.xpath('.//text()')
            if name == ['硕士生导师']:
                continue
            elif name:
                name = name[0]
                name = re.sub(self.name_filter_re, '', name)
                link = a.xpath('./@href')[0]
                link = parse.urljoin(url, link)
            else:
                continue
            yield name, link


spider = Special_ReCrawler(school_id=school_id,
                           college_id=college_id,
                           school_name=school_name,
                           college_name=college_name,
                           name_filter_re=r'\s?导师简介',
                           start_urls=start_urls,
                           a_s_xpath_str=a_s_xpath_str,
                           target_div_xpath_str=target_div_xpath_str,
                           directions_pattern_list=directions_pattern_list,
                           abstracts_pattern_list=abstracts_pattern_list,
                           office_address_pattern_list=office_address_pattern_list,
                           # job_information_pattern_list=job_information_pattern_list,
                           # responsibilities_pattern_list=responsibilities_pattern_list,
                           # education_experience_pattern_list=education_experience_pattern_list,
                           # work_experience_pattern_list=work_experience_pattern_list,
                           patent_pattern_list=patent_pattern_list,
                           project_pattern_list=project_pattern_list,
                           # award_pattern_list=award_pattern_list,
                           # social_job_pattern_list=social_job_pattern_list,
                           save2target='simple'
                           )

spider.run()


