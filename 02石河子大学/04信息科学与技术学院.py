import re
from crawler import ReCrawler

school_name = '石河子大学',
college_name = '信息科学与技术学院',
school_id = 2
college_id = 4
start_urls = ['https://cs.shzu.edu.cn/js/list.htm',
              'https://cs.shzu.edu.cn/fjs/list.htm',
              'https://cs.shzu.edu.cn/fjs/list2.htm',
              'https://cs.shzu.edu.cn/dzxxzsds/list.htm',
              'https://cs.shzu.edu.cn/dzxxzsds/list2.htm',
              'https://cs.shzu.edu.cn/dzxxzsds/list3.htm',
              'https://cs.shzu.edu.cn/wlkjaqxsds/list.htm',
              'https://cs.shzu.edu.cn/tsqbxzsds/list.htm'
              ]

a_s_xpath_str = '//div[@portletmode="simpleList"]/ul//a'
target_div_xpath_str = '//div[@portletmode="simpleArticleAttri"]'
# 研究方向
directions_pattern_list = [
                            re.compile(r'研究领域(?:：|:)?(.*?)(?=.?系别|\W?荣誉)', re.S),
                            re.compile(r'主要研究内容(?:：|:)?(.*?)(?=4)', re.S),
                            re.compile(r'研究兴趣(?:：|:)?(.*?)\W?科研项目')
                          ]
# 简介
# abstracts_pattern_list = [
#                             re.compile(r'工作经历(?:：|:)?(.*?).研究领域.*?.荣誉及奖励(.*?).开授', re.S),
#                             re.compile(r'基本情况(?:：|:)?(.*?)3')
#                           ]
# 办公地点
office_address_pattern_list = [
                                re.compile(r'办公室(?:：|:)?(\w*?)\W?系别', re.S)
                              ]
# 在职信息
# job_information_pattern_list = [
#                                 re.compile(r'', re.S)
#                               ]
# 主要任职
responsibilities_pattern_list = [
                                    re.compile(r'职务(?:：|:)?(\w*)电子信箱', re.S),
                                    # re.compile(r'', re.S)
                                ]
# 教育经历
education_experience_pattern_list = [
                                    re.compile(r'学习经历(?:：|:)?(.*?)\W?工作经历', re.S),
                                    # re.compile(r'', re.S)
                                ]

# 工作经历
work_experience_pattern_list = [
                                    re.compile(r'工作经历(?:：|:)?(.*?)\W?研究领域', re.S),
                                    # re.compile(r'', re.S)
                                ]
# 专利
patent_pattern_list = [
                                    re.compile(r'发明专利(?:：|:)?(.*?)\W?学术与社会服务', re.S),
                                    # re.compile(r'', re.S)
                                ]
# 科研项目
project_pattern_list = [
                                    re.compile(r'科研项目(?!.*?(?:工作经历|研究领域|学术与社会服务).*?)(?:：|:)?(.*?)$', re.S),
                                    # re.compile(r'', re.S)
                                ]
# 奖励/荣誉
award_pattern_list = [
                                    re.compile(r'荣誉及奖励(?:：|:)?(.*?)\W?开授课程', re.S),
                                    # re.compile(r'', re.S)
                                ]
# 社会兼职
social_job_pattern_list = [
                                    re.compile(r'学术与社会服务(?:：|:)?(.*?)\W?科研项目', re.S),
                                    # re.compile(r'', re.S)
                                ]

spider = ReCrawler(
                   school_name='02石河子大学',
                   college_name='信息科学与技术学院',
                   school_id=school_id,
                   college_id=college_id,
                   name_filter_re=r'\w+(?:—|-)+',
                   start_urls=start_urls,
                   a_s_xpath_str=a_s_xpath_str,
                   target_div_xpath_str=target_div_xpath_str,
                   directions_pattern_list=directions_pattern_list,
                   # abstracts_pattern_list=abstracts_pattern_list,
                   office_address_pattern_list=office_address_pattern_list,
                   # job_information_pattern_list=job_information_pattern_list,
                   responsibilities_pattern_list=responsibilities_pattern_list,
                   education_experience_pattern_list=education_experience_pattern_list,
                   work_experience_pattern_list=work_experience_pattern_list,
                   patent_pattern_list=patent_pattern_list,
                   project_pattern_list=project_pattern_list,
                   award_pattern_list=award_pattern_list,
                   social_job_pattern_list=social_job_pattern_list,
                   save2target='simple'
                   )

spider.run()


