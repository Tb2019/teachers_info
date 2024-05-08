import re
from crawler import ReCrawler

school_name = '石河子大学'
college_name = '化学化工学院'
school_id = 2
college_id = 1
start_urls = ['https://hgxy.shzu.edu.cn/jsml/list.htm']

a_s_xpath_str = '//div[@id="wp_content_w107_0"]//td//a'
target_div_xpath_str = '//div[@class="article_content"]'

# 研究方向
directions_pattern_list = [
                            re.compile(r'(?:研究|科研)方向(?:：|:)?(.*?)(?=(?:.{1,6}(?:：|:))|个人简介|教育工作经历)', re.S),
                            # re.compile(r'', re.S)
                          ]
# 个人简介
abstracts_pattern_list = [
                            re.compile(r'个人简(?:介|历)(?:：|:)?(.*?)(?=科研项目(?:：|:)?|代表性论文(?:：|:)?|研究方向(?:：|:)?)', re.S),
                            re.compile(r'基本情况(?:：|:)?(.*?)(?<!:|：)招生方向', re.S)
                          ]
# 办公地址
office_address_pattern_list = [
                                re.compile(r'实验室地址(?:：|:)?(.*?)通讯地址(?:(?:：|:)?(.*?)邮编)?', re.S),
                                re.compile(r'(?<!实验室)地址(?:：|:)?(.*?)邮编', re.S)
                              ]
# 在职信息
# job_information_pattern_list = [
#                                 re.compile(r'', re.S)
#                               ]
# 主要任职
responsibilities_pattern_list = [
                                    # re.compile(r'', re.S),
                                    # re.compile(r'', re.S)
                                ]
# 教育经历
education_experience_pattern_list = [
                                    re.compile(r'教育经历(?:：|:)?(.*?)工作经历', re.S),
                                    # re.compile(r'', re.S)
                                ]

# 工作经历
work_experience_pattern_list = [
                                    re.compile(r'工作经历(?:：|:)?(.*?)科研项目', re.S),
                                    # re.compile(r'', re.S)
                                ]
# 专利
patent_pattern_list = [
                                    re.compile(r'发明专利(?:：|:)(.*?)联系方式', re.S),
                                    re.compile(r'发明专利(?!.*?(?:科研项目|工作经历|研究方向|代表性论文).*?)(?:：|:)?(.*?)$', re.S)
                                ]
# 科研项目
project_pattern_list = [
                                    re.compile(r'科研项目(?!.*?工作经历.*?)(?:：|:)?(.*?)代表性论文', re.S),
                                    # re.compile(r'', re.S)
                                ]
# 获奖/荣誉信息
award_pattern_list = [
                                    # re.compile(r'', re.S),
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
                   responsibilities_pattern_list=responsibilities_pattern_list,
                   education_experience_pattern_list=education_experience_pattern_list,
                   work_experience_pattern_list=work_experience_pattern_list,
                   patent_pattern_list=patent_pattern_list,
                   project_pattern_list=project_pattern_list,
                   award_pattern_list=award_pattern_list,
                   # social_job_pattern_list=social_job_pattern_list,
                   save2target='simple'
                   )

spider.run()


