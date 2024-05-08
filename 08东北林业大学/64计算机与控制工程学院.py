import re
from crawler import ReCrawler

school_name = '东北林业大学'
college_name = '计算机与控制工程学院'
school_id = 8
college_id = 64
start_urls = [
                'https://ccec.nefu.edu.cn/szdw/zdh.htm',
                'https://ccec.nefu.edu.cn/szdw/zdh/1.htm',
                'https://ccec.nefu.edu.cn/szdw/jsjkxyjs.htm',
                'https://ccec.nefu.edu.cn/szdw/jsjkxyjs/2.htm',
                'https://ccec.nefu.edu.cn/szdw/jsjkxyjs/1.htm',
                'https://ccec.nefu.edu.cn/szdw/dzxxgc.htm',
                'https://ccec.nefu.edu.cn/szdw/dzxxgc/1.htm',
                'https://ccec.nefu.edu.cn/szdw/dqgcjqzdh.htm',
                'https://ccec.nefu.edu.cn/szdw/dqgcjqzdh/1.htm',
                'https://ccec.nefu.edu.cn/szdw/txgc.htm',
                'https://ccec.nefu.edu.cn/szdw/rjgc.htm',
                'https://ccec.nefu.edu.cn/szdw/sjkxydsjjs.htm',
                'https://ccec.nefu.edu.cn/szdw/sjkxydsjjs/1.htm',
                'https://ccec.nefu.edu.cn/szdw/rgzn.htm',
                'https://ccec.nefu.edu.cn/szdw/syzx.htm',
                'https://ccec.nefu.edu.cn/szdw/dgjys.htm'
              ]

a_s_xpath_str = '//div[@class="sub_cont"]/div/ul/li/a[contains(@href, "info")]'
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

spider = ReCrawler(
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
                   save2target='simple'
                   )

spider.run()


