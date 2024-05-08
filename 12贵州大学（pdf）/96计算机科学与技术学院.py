import re
from urllib import parse

import pandas as pd
from lxml import etree

from crawler import ReCrawler
from utils import get_response, result_dict_2_df, drop_duplicate_collage, truncate_table, df2mysql, local_engine, \
    sf_engine, save_as_json

school_name = '贵州大学'
college_name = '计算机科学与技术学院'
school_id = 12
college_id = 96

# 第一部分
urls_part1 = [
                'http://cs.gzu.edu.cn/16253/list.htm',
                'http://cs.gzu.edu.cn/16254/list.htm',
              ]
# 第二部分--直接提取(只有电话邮箱等基本信息)
urls_part2 = [
    'http://cs.gzu.edu.cn/16311/list.htm'
]

start_urls = urls_part1 + urls_part2
a_s_xpath_str = '//div[@id="wp_content_w5_0"]/table//a[@href!="#"]'
target_div_xpath_str = '//div[@class="info"]'
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
        if url in urls_part1:
            a_s = page.xpath(self.a_s_xpath_str)
            for a in a_s:
                name = a.xpath('.//text()')
                # print(name)
                if name:
                    name = ''.join(name)
                    if name == 'ZHUYUEMIN':
                        continue
                    name = re.sub(r'\s*', '', name)
                    name = re.sub(self.name_filter_re, '', name)
                    link = a.xpath('./@href')[0]
                    link = parse.urljoin(url, link)
                else:
                    print('未解析到name，请检查：a_s_xpath_str')
                    continue
                yield name, link
        else:
            print('直接解析', url)
            tr_s = page.xpath('//div[@id="wp_content_w5_0"]//tr[position()>1]/td/parent::tr')
            for tr in tr_s:
                try:
                    td_s = tr.xpath('./td[not(@rowspan)]')
                    name = ''.join(td_s[1].xpath('.//text()'))
                    name = re.sub(r'\s*', '', name)
                    name = re.sub(r'ZhuYuemin（(朱跃敏)）', r'\1', name)
                    email = td_s[4].xpath('.//text()')[0]
                    directions = td_s[3].xpath('.//text()')[0]
                except:
                    continue
                result = {
                    'name': name,
                    'school_id': school_id,
                    'college_id': college_id,
                    'phone': None,
                    'email': email,
                    'job_title': None,
                    'abstracts': None,
                    'directions': directions,
                    'education_experience': None,
                    'work_experience': None,
                    'patent': None,
                    'project': None,
                    'award': None,
                    'social_job': None,
                    'picture': None,
                    'education': None,
                    'qualification': None,
                    'job_information': 1,
                    'responsibilities': None,
                    'office_address': None
                }
                print(result)
                self.result_df = result_dict_2_df(self.result_df, result)
            return None


    def run(self):
        self.result_df = pd.DataFrame()
        for url in self.start_urls:
            index_page = get_response(url)
            index_result = self.parse_index(index_page, url)
            if index_result:
                detail_pages = self.get_detail_page(index_result)
                for detail_page in detail_pages:
                    # print('detail', detail_page)
                    result = self.parse_detail(detail_page, url)
                    print(result)
                    # 防止网页本身为空
                    if result:
                        self.result_df = result_dict_2_df(self.result_df, result)
                    else:
                        continue

        # 去重
        # result_df.drop_duplicates(inplace=True, keep='first', subset=['name', 'email'])
        result_df = drop_duplicate_collage(self.result_df)

        # 保存至数据库
        if self.save2target == 'no':
            pass
        elif self.save2target == 'test':
            truncate_table(host='localhost', user='root', password='123456', database='alpha_search', port=3306, table_name='search_teacher_test')
            df2mysql(engine=local_engine, df=result_df, table_name='search_teacher_test')
        # elif self.save2target == 'local':
        #     df2mysql(engine=local_engine, df=result_df, table_name='search_teacher')
        elif self.save2target == 'target':
            df2mysql(engine=sf_engine, df=result_df, table_name='search_teacher')
            save_as_json(result_df, self.school_name, self.college_name)
        # elif self.save2target == 'simple':
        #     df2mysql(engine=sf_engine, df=result_df, table_name='search_teacher_simple')
        #     # 保存成json至本地
        #     save_as_json(result_df, self.school_name, self.college_name)


spider = SpecialSpider(
                   school_name=school_name,
                   college_name=college_name,
                   school_id=school_id,
                   college_id=college_id,
                   name_filter_re=r'简介',
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
                   # email_pattern=re.compile(r'[a-zA-Z0-9._-]+(?:@|\(at\)|\(AT\)|\[at]|\[AT])(?=.{1,10}(?:\.com|\.cn))[a-zA-Z0-9_-]+\.[0-9a-zA-Z._-]+',re.S),
                   save2target='target'
                   )

spider.run()



