import re
from crawler import ReCrawler


school_id = 2
college_id = 8
school_name = '石河子大学'
college_name = '生命科学学院'
start_urls = ['https://skxy.shzu.edu.cn/xyyjsdsjj/list{i}.htm'.format(i=i+1) for i in range(4)]

a_s_xpath_str = '//div[@portletmode="simpleList"]//table[@class="wp_article_list_table"]//a'
target_div_xpath_str = '//div[@class="wp_articlecontent"]'
# 研究方向
directions_pattern_list = [
                            re.compile(r'研究内容(?::|：)?(.*?)\d.目前承担科研项目', re.S),
                            re.compile(r'研究内容(?::|：)?(.*?)\d.承担的科研项目', re.S),
                            re.compile(r'研究内容(?::|：)?(.*?)\d.主持承担科研项目', re.S),
                            re.compile(r'研究内容(?::|：)?(.*?)\d.近年承担科学教研项目', re.S),
                            re.compile(r'研究方向(?::|：)?(.*?)\d.主要研究内容', re.S),
                            re.compile(r'研究方向(?::|：)?(.*?)\w.主持项目', re.S),
                            re.compile(r'研究方向(?::|：)?(.*?)\w.个人介绍', re.S),
                            re.compile(r'研究方向(?::|：)?(.*?)\w.主持的科研项目', re.S),
                            re.compile(r'研究方向(?::|：)?(.*?)\w.主持或参与科研基金项目', re.S),
                            re.compile(r'研究方向(?::|：)?(.*?)\w.招生专业', re.S),
                            re.compile(r'研究方向(?::|：)?(.*?)\w.目前承担科研项目', re.S),
                            re.compile(r'研究内容(?::|：)?(.*?)\w.目前主持科研项目', re.S)
                          ]
# 简介
abstracts_pattern_list = [
                            re.compile(r'^(.*?)学术简历', re.S),
                            re.compile(r'^(.*?)教育背景', re.S),

                            re.compile(r'基本情况(?::|：)?(.*?)\d.主要研究内容', re.S),
                            re.compile(r'照片(.*?)\d.主要研究方向', re.S),
                            re.compile(r'^(.*?)\d.学习和工作经历', re.S),
                            re.compile(r'^(.*?)\d.科研与学术', re.S),
                            re.compile(r'^(.*?)\w.工作经历', re.S),
                            re.compile(r'^(.*?)\w.主要成果', re.S),
                            re.compile(r'^(.*?)目前承担科研项目', re.S),
                            re.compile(r'基本情况(?::|：)?(.*?)\d.研究项目', re.S),
                            re.compile(r'基本情况(?::|：)?(.*?)目前承担科研项目', re.S),
                            re.compile(r'^(.*?)电子邮箱', re.S)
                          ]
# 办公地点
office_address_pattern_list = [
                                re.compile(r'通讯地址(?::|：)?(.*?)\d.邮编'),
                                re.compile(r'联系地址(?::|：)?(.*?)邮编'),
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
                                    re.compile(r'教育经历(?::|：)?(.*?)\d、', re.S),
                                    re.compile(r'学习经历(?::|：)?(.*?)\d、', re.S),
                                    re.compile(r'学习和工作经历(?::|：)?(.*?)\d\.', re.S),
                                    re.compile(r'受教育经历(?::|：)?(.*?)研究工作经历', re.S),
                                    re.compile(r'学习工作经历(?::|：)?(.*?)工作经历', re.S),
                                ]

# 工作经历
work_experience_pattern_list = [
                                    re.compile(r'科研与学术工作经历(?::|：)?(.*?)\d\.', re.S),
                                    re.compile(r'工作经历(?::|：)?(.*?)\d、', re.S),
                                    re.compile(r'研究工作经历(?::|：)?(.*?)主要研究方向', re.S),
                                ]
# 专利
patent_pattern_list = [
                                    re.compile(r'专利(?::|：)?(.*?)电子信箱', re.S),
                                    # re.compile(r'', re.S)
                                ]
# 科研项目
project_pattern_list = [
                                    re.compile(r'主持承担科研项目(?::|：)?(.*?)\d、', re.S),
                                    re.compile(r'主持或参加的项目/课题：(.*?)\d\.', re.S),
                                    re.compile(r'承担的科研项目(?::|：)?(.*?)\d\.', re.S),
                                    re.compile(r'目前承担科研项目(?::|：)?(.*?)\d、', re.S)
                                ]
# 奖励/荣誉
award_pattern_list = [
                                    re.compile(r'获奖及荣誉(?::|：)?(.*?)\d、', re.S),
                                    re.compile(r'获奖情况(?::|：)?(.*?)\d\.', re.S)
                                ]
# 社会兼职
social_job_pattern_list = [
                            re.compile(r'学术兼职(?::|：)?(?!.*?基本情况.*?)(.*?)教育背景'),
                            re.compile(r'学术兼职(?::|：)?(.*?)主讲课程')
                          ]

spider = ReCrawler(school_id=school_id,
                   college_id=college_id,
                   school_name=school_name,
                   college_name=college_name,
                   name_filter_re=r'导师简介',
                   start_urls=start_urls,
                   a_s_xpath_str=a_s_xpath_str,
                   target_div_xpath_str=target_div_xpath_str,
                   directions_pattern_list=directions_pattern_list,
                   abstracts_pattern_list=abstracts_pattern_list,
                   office_address_pattern_list=office_address_pattern_list,
                   # job_information_pattern_list=job_information_pattern_list,
                   # responsibilities_pattern_list=responsibilities_pattern_list,
                   education_experience_pattern_list=education_experience_pattern_list,
                   work_experience_pattern_list=work_experience_pattern_list,
                   # patent_pattern_list=patent_pattern_list,
                   project_pattern_list=project_pattern_list,
                   award_pattern_list=award_pattern_list,
                   social_job_pattern_list=social_job_pattern_list,
                   save2target='simple'
                   )

spider.run()


