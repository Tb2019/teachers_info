import json
import re

import pandas as pd
import requests
from fake_headers import Headers
from crawler import ReCrawler
from utils import get_response, result_dict_2_df

school_name = '复旦大学'
college_name = '管理学院'
school_id = 105
college_id = 135
start_urls = [
                'https://www.fdsm.fudan.edu.cn/AboutUs/teachers_dir.html'
              ]
headers = Headers(headers=True).generate()

a_s_xpath_str = '//div[@id="mCSB_13_container"]/div//a[@href!="#"]'
target_div_xpath_str = ''

# # 电话
# phone_xpath = None

# # 邮箱
# email_xpath = None

# # 职称
# job_title_xpath = None

# # 学位
# qualification_xpath = None

# # 研究方向
# directions_pattern_list = [
#                             re.compile(r'', re.S),
#                             re.compile(r'', re.S)
#                           ]
# directions_xpath = None

# # 简介
# abstracts_pattern_list = [
#                             re.compile(r'', re.S),
#                             re.compile(r'', re.S)
#                           ]
# abstracts_xpath = None

# # 办公地点
# office_address_pattern_list = [
#                                 re.compile(r'', re.S)
#                               ]
# office_address_xpath = None

# # 在职信息
# job_information_pattern_list = [
#                                 re.compile(r'', re.S)
#                               ]
# job_information_xpath = None

# # 主要任职
# responsibilities_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]
# responsibilities_xpath = None

# # 教育经历
# education_experience_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]
# education_experience_xpath = None


# # 工作经历
# work_experience_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]
# work_experience_xpath = None

# # 专利
# patent_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]
# patent_xpath = None

# # 科研项目
# project_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]
# project_xpath = None

# # 奖励/荣誉
# award_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]
# award_xpath = None

# # 社会兼职
# social_job_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]
# social_job_xpath = None

# # 图片
# img_xpath = None


class SpecialSpider(ReCrawler):
    def parse_index(self, index_page, url):
        # 方法重写时引入包
        global etree, parse
        if not globals().get('etree'):
            from lxml import etree
        if not globals().get('parse'):
            from urllib import parse

        page = etree.HTML(index_page)
        a_s = page.xpath(self.a_s_xpath_str)
        for a in a_s:
            name = a.xpath('.//text()')
            # print(name)
            if name:
                name = ''.join(name)
                if not re.match(r'[A-Za-z\s]*$', name, re.S):  # 中文名替换空格
                    name = re.sub(r'\s*', '', name)
                name = re.sub(self.name_filter_re, '', name)
                link = a.xpath('./@href')[0]
                uid = re.search(r'uid=(.*)$', link).group(1)
            else:
                print('未解析到name，请检查：a_s_xpath_str')
                continue
            yield name, uid

    def parse(self, name, uid):
        base_info_url = 'https://app.fdsm.fudan.edu.cn/NewTeacherService/api/Professor/GetSingleTeacherOtherInfo?personId={personId}&language=cn&labelName=personMessage&typeStr='
        resp = requests.get(base_info_url.format(personID=uid), headers=headers).json()
        print(resp)

    def run(self):
        result_df = pd.DataFrame()
        for url in self.start_urls:
            index_page = get_response(url)
            index_result = self.parse_index(index_page, url)

            for name, uid in index_result:
                result = self.parse(name, uid)
                # print(result)
                # if result:
                #     result_df = result_dict_2_df(result_df, result)
                # else:
                #     continue

        # # 去重
        # # result_df.drop_duplicates(inplace=True, keep='first', subset=['name', 'email'])
        # result_df = drop_duplicate_collage(result_df)
        #
        # # 保存至数据库
        # if self.save2target == 'no':
        #     pass
        # elif self.save2target == 'test':
        #     truncate_table(host='localhost', user='root', password='123456', database='alpha_search', port=3306, table_name='search_teacher_test')
        #     df2mysql(engine=local_engine, df=result_df, table_name='search_teacher_test')
        # # elif self.save2target == 'local':
        # #     df2mysql(engine=local_engine, df=result_df, table_name='search_teacher')
        # elif self.save2target == 'target':
        #     df2mysql(engine=sf_engine, df=result_df, table_name='search_teacher')
        #     save_as_json(result_df, self.school_name, self.college_name)
        # # elif self.save2target == 'simple':
        # #     df2mysql(engine=sf_engine, df=result_df, table_name='search_teacher_simple')
        # #     # 保存成json至本地
        # #     save_as_json(result_df, self.school_name, self.college_name)


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
                   # email_pattern=re.compile(r'[a-zA-Z0-9._-]+(?:@|\(at\)|\(AT\)|\[at]|\[AT])(?=.{1,10}(?:\.com|\.cn|\.net))[a-zA-Z0-9_-]+\.[0-9a-zA-Z._-]+',re.S),

                   # phone_xpath=phone_xpath,
                   # email_xpath=email_xpath,
                   # job_title_xpath=job_title_xpath,
                   # qualification_xpath=qualification_xpath,
                   # directions_xpath=directions_xpath,
                   # abstracts_xpath=abstracts_xpath,
                   # office_address_xpath=office_address_xpath,
                   # job_information_xpath=job_information_xpath,
                   # responsibilities_xpath=responsibilities_xpath,
                   # education_experience_xpath=education_experience_xpath,
                   # work_experience_xpath=work_experience_xpath,
                   # patent_xpath=patent_xpath,
                   # project_xpath=project_xpath,
                   # award_xpath=award_xpath,
                   # social_job_xpath=social_job_xpath,
                   # img_xpath=img_xpath,

                   save2target='test',
                   api=False,
                   )

spider.run()


