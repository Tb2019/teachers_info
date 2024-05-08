import re
from crawler import ReCrawler

school_name = '石河子大学'
college_name = '农学院'
school_id = 2
college_id = 5
start_urls = ['https://nxy.shzu.edu.cn/jsml/list.htm']

a_s_xpath_str = '//div[@id="wp_content_w6_0"]//p[@class="teacher_new"]//a'
target_div_xpath_str = '//div[@portletmode="simpleArticleAttri"]'
# 研究方向
directions_pattern_list = [
                            re.compile(r'研究方向(?::|：)?(.*?)(?=个人简介)', re.S),
                            re.compile(r'研究方向(?::|：)?(.*?)(?=一、工作简历)', re.S),
                            re.compile(r'研究领域(?::|：)?(.*?)(?=主持)')
                          ]
# 简介
abstracts_pattern_list = [
                            re.compile(r'个人简介(?::|：)?(.*?)(?=一、教学情况)')
                          ]
# 办公地点
office_address_pattern_list = [
                                re.compile(r'办公室(?::|：)?(.*?)(?=(?:E-|e-|E\.|e\.)??mai)', re.S)
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
# patent_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]
# 科研项目
project_pattern_list = [
                                    re.compile(r'科学研究(?::|：)?(?:在研项目及已结题项目)?(.*?)\w、', re.S),
                                    re.compile(r'在研科研项目(?::|：)?(.*?)教学基本情况', re.S)
                                ]
# 奖励/荣誉
award_pattern_list = [
                                    re.compile(r'获奖及荣誉(?::|：)?(.*?)\w、', re.S),
                                    # re.compile(r'', re.S)
                                ]
# 社会兼职
# social_job_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]

spider = ReCrawler(
                   school_name=school_name,
                   college_name=college_name,
                   school_id=school_id,
                   college_id=college_id,
                   name_filter_re=r'\s*',
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
                   # patent_pattern_list=patent_pattern_list,
                   project_pattern_list=project_pattern_list,
                   award_pattern_list=award_pattern_list,
                   # social_job_pattern_list=social_job_pattern_list,
                   save2target='simple'
                   )

spider.run()


