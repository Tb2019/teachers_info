import re
from crawler import ReCrawler


school_id = 2
college_id = 9
school_name = '石河子大学'
college_name = '经济与管理学院'
start_urls = ['https://sem.shzu.edu.cn/szdw/list.htm']

a_s_xpath_str = '//div[@frag="面板8"]//table//li//span//a'
target_div_xpath_str = '//div[@class="wp_articlecontent"]'
# 研究方向
directions_pattern_list = [
                            re.compile(r'研究方向(?::|：)?(.*?)(?:（|\()\w(?:）|\))', re.S),
                            re.compile(r'研究内容(?::|：)?(.*?)\w.主持科研项目', re.S),
                            re.compile(r'研究内容(?::|：)?(.*?)\w.承担(?:的主要)??科研项目', re.S),
                            re.compile(r'研究内容(?::|：)?(.*?)\w.目前承担', re.S),
                            re.compile(r'研究内容(?::|：)?(.*?)\w.\w*?代表性科研成果', re.S),
                            re.compile(r'研究内容(?::|：)?(.*?)\w*?代表性科研成果', re.S),
                            re.compile(r'主要研究领域与业绩(?::|：)?(.*?)\d.目前承担科研项目'),
                            re.compile(r'研究内容(?::|：)?(.*?)\d.讲授课程'),
                            re.compile(r'研究内容(?::|：)?(.*?)\d.联系方式'),
                            re.compile(r'研究内容(?::|：)?(.*?)近年代表性科研成果'),
                            re.compile(r'研究方向(?::|：)?(.*?)科研项目'),
                            re.compile(r'主要研究领域及方向(?::|：)?(.*?)\d、'),
                          ]
# 简介
abstracts_pattern_list = [
                            re.compile(r'基本情况(?::|：)?(.*?)(?:（|\()\w(?:）|\))主要研究', re.S),
                            re.compile(r'基本情况(?::|：)?(.*?)(\w.)?主要研究', re.S),
                            re.compile(r'基本情况(?::|：)?(.*?)\w.联系方式', re.S),
                            re.compile(r'基本情况(?::|：)?(.*?)\w.工作简历', re.S),
                            re.compile(r'^(.*?)(?:学术简历|教育经历|教育背景|工作经历)', re.S),
                          ]
# 办公地点
office_address_pattern_list = [
                                re.compile(r'通讯地址(?::|：)?(.*?)邮政编码', re.S)
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
                                    re.compile(r'教育背景(?::|：)?(.*?)研究方向', re.S),
                                    re.compile(r'教育背景(?::|：)?(.*?)曾获奖励', re.S),
                                    re.compile(r'学术简历(?::|：)?(.*?)\d、', re.S),
                                    re.compile(r'教育背景(?::|：)?(.*?)\d、', re.S),
                                    re.compile(r'教育背景(?::|：)?(.*?)职称及教学研究工作简历', re.S),
                                    re.compile(r'教育及工作经历(?::|：)?(.*?)课程及导师情况', re.S),
                                    re.compile(r'教育背景(?::|：)?(.*?)奖励及荣誉', re.S),
                                    re.compile(r'教育背景(?::|：)?(.*?)科研项目及研究报告', re.S),
                                    re.compile(r'教育背景(?::|：)?(.*?)\d\.主要研究内容', re.S),
                                ]

# 工作经历
work_experience_pattern_list = [
                                    re.compile(r'职称与研究工作经历(.*?)\d、', re.S),
                                    re.compile(r'职称与研究工作经历(.*?)获教学及科研奖励', re.S),
                                    re.compile(r'学术简历(.*?)(?:\d\.)?教育背景', re.S),
                                    re.compile(r'学术简历(.*?)学术兼职', re.S),
                                ]
# 专利
# patent_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]
# 科研项目
project_pattern_list = [
                                    re.compile(r'目前承担科研项目(?::|：)?(.*?)\d、', re.S),
                                    re.compile(r'目前承担科研项目(?::|：)?(.*?)\d\.', re.S),
                                    re.compile(r'课题项目(?::|：)?(.*?)代表作：', re.S),
                                    re.compile(r'科研项目(?::|：)?(.*?)行政管理经验：', re.S),
                                    re.compile(r'主持和参与的课题项目(?::|：)?(.*?)\d、：', re.S),
                                    re.compile(r'主持科研项目(?::|：)?(.*?)讲授课程', re.S),
                                    re.compile(r'科研项目（主持）(?::|：)?(.*?)科研获奖', re.S),
                                ]
# 奖励/荣誉
award_pattern_list = [
                                    re.compile(r'曾获奖励(.*?)主持科研项目', re.S),
                                    re.compile(r'获得荣誉(.*?)\d、', re.S),
                                    re.compile(r'科研获奖(.*?)科研成果', re.S),
                                ]
# 社会兼职
social_job_pattern_list = [
                            re.compile(r'学术兼职(?::|：)?(.*?)教育背景', re.S),
                            re.compile(r'学术和社会兼职(.*?)\w.获得的荣誉'),
                            re.compile(r'社会兼职或荣誉(.*?)\d、')
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


