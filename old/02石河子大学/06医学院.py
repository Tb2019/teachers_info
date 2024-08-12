import re
from crawler import ReCrawler

school_name = '石河子大学'
college_name = '医学院'
school_id = 2
college_id = 6
start_urls = ['https://yixy.shzu.edu.cn/dsjj_yjs/list{i}.htm'.format(i=i+1) for i in range(26)]

a_s_xpath_str = '//div[@id="wp_news_w6"]//a'
target_div_xpath_str = '//div[@portletmode="simpleArticleTitle"]'
# 研究方向
directions_pattern_list = [
                            re.compile(r'研究领域(?::|：)?(.*?)邮箱', re.S),
                            re.compile(r'研究(?:方向|内容)(?::|：)?(.*?)。', re.S),
                            re.compile(r'科研方向(?::|：)(.*?)项目'),
                            re.compile(r'研究(?:方向|内容)(?::|：)?(.*?)\d.目前承担科研项目')
                          ]
# 简介
# abstracts_pattern_list = [
#                             re.compile(r'', re.S),
#                             re.compile(r'', re.S)
#                           ]
# 办公地点
office_address_pattern_list = [
                                re.compile(r'通讯地址(?::|：)?(.*?)学术兼职', re.S)
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
education_experience_pattern_list = [
                                    re.compile(r'科研学术工作经历与教育背景(?::|：)?(.*?)科研项目', re.S),
                                    # re.compile(r'', re.S)
                                ]

# 工作经历
# work_experience_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]
# 专利
patent_pattern_list = [
                                    re.compile(r'专利(?::|：)?(?!.*?论文.*?)(.*?)承担教学', re.S),
                                    # re.compile(r'', re.S)
                                ]
# 科研项目
project_pattern_list = [
                                    re.compile(r'科研项目(?::|：)?(.*?)学术论文(?::|：)', re.S),
                                    re.compile(r'项目(?::|：)(.*?)成果(?::|：)', re.S)
                                ]
# 奖励/荣誉
award_pattern_list = [
                                    re.compile(r'获奖(?::|：)?(.*?)专利', re.S),
                                    re.compile(r'获奖(?::|：)?(.*?)承担教学', re.S)
                                ]
# 社会兼职
social_job_pattern_list = [
                                    re.compile(r'学术兼职情况(?::|：)?(.*?)科研学术工作经历与教育背景', re.S),
                                    re.compile(r'学术兼职情况(?::|：)?(.*?)八、基本情况', re.S)
                                ]

spider = ReCrawler(school_id=school_id,
                   college_id=college_id,
                   school_name=school_name,
                   college_name=college_name,
                   name_filter_re=r'\s?导师简介',
                   start_urls=start_urls,
                   a_s_xpath_str=a_s_xpath_str,
                   target_div_xpath_str=target_div_xpath_str,
                   directions_pattern_list=directions_pattern_list,
                   # abstracts_pattern_list=abstracts_pattern_list,
                   office_address_pattern_list=office_address_pattern_list,
                   # job_information_pattern_list=job_information_pattern_list,
                   # responsibilities_pattern_list=responsibilities_pattern_list,
                   education_experience_pattern_list=education_experience_pattern_list,
                   # work_experience_pattern_list=work_experience_pattern_list,
                   patent_pattern_list=patent_pattern_list,
                   project_pattern_list=project_pattern_list,
                   award_pattern_list=award_pattern_list,
                   social_job_pattern_list=social_job_pattern_list,
                   save2target='simple'
                   )

spider.run()


