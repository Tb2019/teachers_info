import re
from crawler import ReCrawler

school_name = '石河子大学'
college_name = '化学化工学院'
school_id = 2
college_id = 2
start_urls = ['https://jdxy.shzu.edu.cn/sssdsjj/list.htm', 'https://jdxy.shzu.edu.cn/bssdsjj/list.htm']

a_s_xpath_str = '//div[@id="wp_content_w22_0"]//a'
target_div_xpath_str = '//div[@class="content_txt"]'

directions_pattern_list = [
                            re.compile(r'研究(?:领域|内容)(?:：|:)?(.*?)(?=(?:\d、\w{2,})??科研项目)', re.S),
                            # re.compile(r'', re.S)
                          ]

abstracts_pattern_list = [
                            re.compile(r'基本情况(1.*?2.*?)3、', re.S),
                            re.compile(r'^(.*?)(?=电子??邮|招生专业)', re.S)
                          ]

# office_address_pattern_list = [
#                                 re.compile(r'', re.S)
#                               ]

# job_information_pattern_list = [
#                                 re.compile(r'', re.S)
#                               ]

# responsibilities_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]

education_experience_pattern_list = [
                                    re.compile(r'教育背景(?:（按时间倒排序）)?(?:：|:)?(.*?)(?:出访及挂职经历|研究领域)', re.S)
                                    # re.compile(r'', re.S)
                                ]


work_experience_pattern_list = [
                                    re.compile(r'出访及挂职经历(?:：|:)?(.*?)研究领域', re.S),
                                    # re.compile(r'', re.S)
                                ]

# patent_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]

project_pattern_list = [
                            re.compile(r'目前承担科研项目(?:：|:)?(.*?)\d.(?:近3年)?代表性科研成果', re.S),
                            re.compile(r'科研项目(?:情况)?(?:：|:)?(.*?)代表性(?:科研)?成果', re.S),
                       ]

award_pattern_list = [
                                    re.compile(r'奖励与荣誉(?:：|:)?(.*?)$', re.S),
                                    # re.compile(r'', re.S)
                                ]

# social_job_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]

spider = ReCrawler(
                   school_name='02石河子大学',
                   college_name='机械电气工程学院',
                   school_id=school_id,
                   college_id=college_id,
                   name_filter_re=r'\s*',
                   start_urls=start_urls,
                   a_s_xpath_str=a_s_xpath_str,
                   target_div_xpath_str=target_div_xpath_str,
                   directions_pattern_list=directions_pattern_list,
                   abstracts_pattern_list=abstracts_pattern_list,
                   # office_address_pattern_list=office_address_pattern_list,
                   # job_information_pattern_list=job_information_pattern_list,
                   # responsibilities_pattern_list=responsibilities_pattern_list,
                   education_experience_pattern_list=education_experience_pattern_list,
                   work_experience_pattern_list=work_experience_pattern_list,
                   # patent_pattern_list=patent_pattern_list,
                   project_pattern_list=project_pattern_list,
                   award_pattern_list=award_pattern_list,
                   # social_job_pattern_list=social_job_pattern_list,
                   save2target='simple'
                   )

spider.run()


