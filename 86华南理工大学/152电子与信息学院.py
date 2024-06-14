# -*- coding: utf-8 -*-
import re
from crawler import ReCrawler

school_name = '华南理工大学'
college_name = '电子与信息学院'
school_id = 86
college_id = 152
img_url_head = 'https://yanzhao.scut.edu.cn/'
partition_num = '020'
start_urls = [
                # 'https://www2.scut.edu.cn/ee/dzkxyjs/list.htm',  # 博导  电子科学与技术
                # 'https://www2.scut.edu.cn/ee/xxytxgc/list.htm',
                # 'https://www2.scut.edu.cn/ee/xxytxgc/list2.htm',
                # 'https://www2.scut.edu.cn/ee/xxytxgc/list3.htm',  # 信息与通信工程
                # 'https://www2.scut.edu.cn/ee/dzxx/list.htm',
                # 'https://www2.scut.edu.cn/ee/dzxx/list2.htm',  # 电子信息
                # 'https://www2.scut.edu.cn/ee/dzkxyjs_36363/list.htm',
                # 'https://www2.scut.edu.cn/ee/dzkxyjs_36363/list2.htm',  # 硕导  电子科学与技术
                # 'https://www2.scut.edu.cn/ee/xxytxgc_36364/list.htm',
                # 'https://www2.scut.edu.cn/ee/xxytxgc_36364/list2.htm',
                # 'https://www2.scut.edu.cn/ee/xxytxgc_36364/list3.htm',
                # 'https://www2.scut.edu.cn/ee/xxytxgc_36364/list4.htm',  # 信息与通信工程
                'https://www2.scut.edu.cn/ee/dzxx_36365/list.htm',
                'https://www2.scut.edu.cn/ee/dzxx_36365/list2.htm',
                'https://www2.scut.edu.cn/ee/dzxx_36365/list3.htm',
                'https://www2.scut.edu.cn/ee/dzxx_36365/list4.htm',
                'https://www2.scut.edu.cn/ee/dzxx_36365/list5.htm',  # 电子信息
                # '',
              ]

a_s_xpath_str = '//ul[@class="te-item"]/li/div[@class="li-con"]/div[@class="te-title"]/a'
target_div_xpath_str = '//div[@id="parId"]/div[3]'

# # 电话
# phone_xpath = None

# # 邮箱
# email_xpath = None

# # 职称
# job_title_xpath = None

# # 学位
# qualification_xpath = None

# # 图片
# img_xpath = None

# 研究方向
# directions_pattern_list = [
#                             re.compile(r'', re.S),
#                             re.compile(r'', re.S)
#                           ]
# directions_xpath = None

# 专利
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

# # 社会兼职
# social_job_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]
# social_job_xpath = None

spider = ReCrawler(
                   school_name=school_name,
                   college_name=college_name,
                   partition_num=partition_num,
                   school_id=school_id,
                   college_id=college_id,
                   name_filter_re=r'简介',
                   start_urls=start_urls,
                   img_url_head=img_url_head,
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
                   # paper_pattern_list=paper_pattern_list,
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
                   # paper_xpath=paper_xpath,
                   # social_job_xpath=social_job_xpath,
                   # img_xpath=img_xpath,

                   save2target='no',
                   selenium_gpt=True,
                   cn_com='com',
                   api=False,
                   )

spider.run()


