# todo:格式规范
import re
from crawler import ReCrawler

school_name = '延边大学'
college_name = '农学院'
school_id = 10
college_id = 87
start_urls = [
                'https://nxy.ybu.edu.cn/szdw/zzjs/nxx.htm',
                'https://nxy.ybu.edu.cn/szdw/zzjs/ylyyx/ylzy.htm',
                'https://nxy.ybu.edu.cn/szdw/zzjs/ylyyx/yyzy.htm',
                'https://nxy.ybu.edu.cn/szdw/zzjs/dwkxx.htm',
                'https://nxy.ybu.edu.cn/szdw/zzjs/dwyxx.htm',
                'https://nxy.ybu.edu.cn/szdw/zzjs/spyswkxx/swjszy.htm',
                'https://nxy.ybu.edu.cn/szdw/zzjs/spyswkxx/spkxygczy.htm',
                'https://nxy.ybu.edu.cn/szdw/bssyjsds/cmx/dwycyzyfz.htm',
                'https://nxy.ybu.edu.cn/szdw/bssyjsds/cmx/dwyyyslkx.htm',
                'https://nxy.ybu.edu.cn/szdw/bssyjsds/cmx/dwscx.htm',
                'https://nxy.ybu.edu.cn/szdw/bssyjsds/cmx/dwcppzyaqsc.htm',
                'https://nxy.ybu.edu.cn/szdw/sssyjsds/xsxssyjs/zwx.htm',
                'https://nxy.ybu.edu.cn/szdw/sssyjsds/xsxssyjs/yyx.htm',
                'https://nxy.ybu.edu.cn/szdw/sssyjsds/xsxssyjs/nyzyyhj.htm',
                'https://nxy.ybu.edu.cn/szdw/sssyjsds/xsxssyjs/cmx.htm',
                'https://nxy.ybu.edu.cn/szdw/sssyjsds/xsxssyjs/syx.htm',
                'https://nxy.ybu.edu.cn/szdw/sssyjsds/xsxssyjs/spkxygc.htm',
                'https://nxy.ybu.edu.cn/szdw/sssyjsds/zyxssyjs/nyss/nyyzy.htm',
                'https://nxy.ybu.edu.cn/szdw/sssyjsds/zyxssyjs/nyss/zylyyzwbh.htm',
                'https://nxy.ybu.edu.cn/szdw/sssyjsds/zyxssyjs/nyss/cm.htm',
                'https://nxy.ybu.edu.cn/szdw/sssyjsds/zyxssyjs/nyss/spjgyaq.htm',
                'https://nxy.ybu.edu.cn/szdw/sssyjsds/zyxssyjs/syss.htm',
                'https://nxy.ybu.edu.cn/szdw/sssyjsds/zyxssyjs/fjyl.htm'
              ]

a_s_xpath_str = '//div[@class="col-lg-9 order-1 order-lg-2"]/ul//a[@href!="#"]'
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
                   save2target='target'
                   )

spider.run()


