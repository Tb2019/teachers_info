# todo:客座教授未抓取
# todo:李玉泽  email匹配有问题
from crawler import ReCrawler
from utils import get_response, result_dict_2_df, drop_duplicate_collage, df2mysql, sf_engine, save_as_json, \
    local_engine
import pandas as pd
import requests
from fake_headers import Headers
import re


school_name = '宁夏大学'
college_name = '化学化工学院'
school_id = 4
college_id = 31
start_urls = ['https://chem.nxu.edu.cn/szdw/yjsds1/bssds1.htm',
              'https://chem.nxu.edu.cn/szdw/yjsds1/sssds1.htm']

a_s_xpath_str = '//div[@class="jgsz"]/ul/li/a[contains(@href, "info")]'
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

result_part1 = pd.DataFrame()

# 常规部分
class SpecialSpider(ReCrawler):
    def run(self):
        global result_part1
        for url in self.start_urls:
            index_page = get_response(url)
            index_result = self.parse_index(index_page, url)

            detail_pages = self.get_detail_page(index_result)
            for detail_page in detail_pages:
                # print('detail', detail_page)
                result = self.parse_detail(detail_page, url)
                print(result)
                # 防止网页本身为空
                if result:
                    result_part1 = result_dict_2_df(result_part1, result)
                else:
                    continue


spider = SpecialSpider(
                   school_name=school_name,
                   college_name=college_name,
                   school_id=school_id,
                   college_id=college_id,
                   name_filter_re=r'(?:\(|（)(?:男|女)(?:\)|）)',
                   start_urls=start_urls,
                   a_s_xpath_str=a_s_xpath_str,
                   target_div_xpath_str=target_div_xpath_str,
                   email_pattern=re.compile(r'(?<=邮箱(?::|：))[a-zA-Z0-9._-]+(?:@|\(at\)|\(AT\)|\[at]|\[AT])[a-zA-Z0-9_-]+\.[a-zA-Z._-]+', re.S),
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
                   save2target='no'
                   )

spider.run()

# ajax部分
print('------------------ajax------------------')

base_url = 'https://chem.nxu.edu.cn/system/resource/tsites/portal/queryteacher.jsp?collegeid=1167&isshowpage=false&postdutyid=0&postdutyname=&facultyid=&disciplineid=0&rankcode=0&jobtypecode=&enrollid=0&pageindex=1&pagesize=10&login=true&profilelen=10&honorid=0&pinyin=&teacherName=&searchDirection=&viewmode=10&viewOwner=1888820013&viewid=1076580&siteOwner=1888820013&viewUniqueId=u15&showlang=zh_CN&actiontype='
headers = Headers(headers=True).generate()
result_part2 = pd.DataFrame()


resp = requests.get(base_url, headers=headers).json()
teachers_info = resp['teacherData']
result = {}
for teacher_info in teachers_info:
    result['name'] = teacher_info['name']
    result['school_id'] = school_id
    result['college_id'] = college_id
    result['phone'] = None
    result['email'] = teacher_info['email'] if teacher_info['email'] != '' else None
    result['job_title'] = teacher_info['prorank'] if teacher_info['prorank'] != '' else None
    result['abstracts'] = None
    result['directions'] = teacher_info['yjfx'] if teacher_info['yjfx'] != '' else None
    result['education_experience'] = None
    result['work_experience'] = teacher_info['workexperience'] if teacher_info['workexperience'] != '' else None
    result['patent'] = None
    result['project'] = None
    result['award'] = teacher_info['honor'] if teacher_info['honor'] != '' else None
    result['social_job'] = None
    result['picture'] = teacher_info['picUrl'] if teacher_info['picUrl'] != '' else None
    result['education'] = None
    result['qualification'] = None
    result['job_information'] = 1
    result['responsibilities'] = teacher_info['job'] if teacher_info['job'] != '' else None
    result['office_address'] = teacher_info['officeLocation'] if teacher_info['officeLocation'] != '' else None
    print(result)
    result_part2 = result_dict_2_df(result_part2, result)

# print(result_part2)
# print(len(result_part2))


result_df = pd.concat((result_part1, result_part2), axis=0)
print(result_df.shape)

result_df = drop_duplicate_collage(result_df)
print(result_df.shape)


# df2mysql(engine=local_engine, df=result_df, table_name='search_teacher_test')
df2mysql(engine=sf_engine, df=result_df, table_name='search_teacher_simple')
# 保存成json至本地
save_as_json(result_df, school_name, college_name)






