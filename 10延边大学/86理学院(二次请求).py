import re
from urllib import parse
from fake_headers import Headers
import requests
import selenium.webdriver
from selenium import webdriver
from lxml import etree

from crawler import ReCrawler
# todo:ajax：解析详情页面div.biaoqianline  --> 拿到id和类目  发送post请求拿到数据
# 使用selenium方便

school_name = '延边大学'
college_name = '理学院'
school_id = 10
college_id = 86
start_urls = [
                'https://science.ybu.edu.cn/szdw/zrjs.htm'
              ]

a_s_xpath_str = '//div[@id="vsb_content"]//table//a[@href!="#"]'
target_div_xpath_str = '//div[@class="show-bgimg hf-bgimg"]'

options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
headers = Headers(headers=True).generate()
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
class SpecialSpider(ReCrawler):
    def parse_detail(self, detail_page, url):
        if detail_page:
            page, info_s = detail_page
            # page_tree = etree.HTML(page)
            try:
                teacher_id = re.search(r'class="biaoqianline".*? onclick.*?get_front_teacher_menu_child_block.*?"(.*?)"', page, re.S).group(1)
            except:
                return None
            basic_post_data = {
                'teacher_zjh': teacher_id
            }
            personal_post_data = {
                'teacher_zjh': teacher_id,
                'parent_id': 1
            }
            basic_info = requests.post('https://homepage.ybu.edu.cn/manager/ajax_get_basic_profile.php', data=basic_post_data, headers=headers)
            personal_info = requests.post('https://homepage.ybu.edu.cn/front/ajax_get_fields.php', data=personal_post_data, headers=headers)

            basic_info_json = basic_info.json()
            personal_info_json = personal_info.json()
            personal_info = personal_info_json['result']

            name = info_s[0][1]


            # 学校id
            school_id = self.school_id

            # 学院id
            college_id = self.college_id

            phone = basic_info_json['result']['phone'] if basic_info_json['result']['phone'] and re.sub(r'\s*', '', basic_info_json['result']['phone']) else None
            if phone:
                if len(phone) < 7:
                    phone = None
                elif len(phone) < 11:
                    phone = '0433-' + phone
                elif len(phone) == 11:
                    phone = re.sub(r'(0433)(\d{7})', r'\1-\2', phone)
                else:
                    phone = re.sub(r'\+??86-??433', '0433', phone)
                    phone = re.sub(r'\+86', '', phone)
                    phone = re.sub(r'-(\d{4})$', r'\1', phone)
                    phone = re.sub(r'433\)', '0433', phone)

            email = basic_info_json['result']['email'] if basic_info_json['result']['email'] and re.sub(r'\s*', '', basic_info_json['result']['email']) else None
            if email:
                email = email.replace('；', ',')
                email = re.sub(r'\[(?:a|A)(?:t|T)]', '@', email)
                email = re.sub(r'(?:\(|（).*$', '', email)

            job_title = re.sub(r'.*\^', '', basic_info_json['result']['zc']) if basic_info_json['result']['zc'] and re.sub(r'\s*', '', basic_info_json['result']['zc']) else None
            abstracts = None
            directions = basic_info_json['result']['yjfx'] if basic_info_json['result']['yjfx'] and re.sub(r'\s*', '', basic_info_json['result']['yjfx']) else None
            education_experience = None
            work_experience = None
            patent = None
            project = None
            award = None
            social_job = None
            full_src = 'http://homepage.ybu.edu.cn/rsc/avatar/' + basic_info_json['result']['avatar'] if basic_info_json['result']['avatar'] and re.sub(r'\s*', '', basic_info_json['result']['avatar']) else None
            # 学位、学历
            qualification = None
            education = None
            edu_dict = {'学士': 1, '硕士': 2, '博士': 3}
            edu_code = 0
            try:
                qualification_list = self.qualification_pattern.findall(personal_info)
                for qualification in qualification_list:
                    edu_code_temp = edu_dict[qualification]
                    if edu_code_temp > edu_code:
                        edu_code = edu_code_temp
                if edu_code == 1:
                    qualification = '学士'
                    education = '本科'
                elif edu_code == 2:
                    qualification = '硕士'
                    education = '研究生'
                elif edu_code == 3:
                    qualification = '博士'
                    education = '研究生'
            except:
                pass

            job_information = 1
            responsibilities = None
            office_address = basic_info_json['result']['address'] if basic_info_json['result']['address'] and re.sub(r'\s*', '', basic_info_json['result']['address']) else None
            result = {
                'name': name,
                'school_id': school_id,
                'college_id': college_id,
                'phone': phone,
                'email': email,
                'job_title': job_title,
                'abstracts': abstracts,
                'directions': directions,
                'education_experience': education_experience,
                'work_experience': work_experience,
                'patent': patent,
                'project': project,
                'award': award,
                'social_job': social_job,
                'picture': full_src,
                'education': education,
                'qualification': qualification,
                'job_information': job_information,
                'responsibilities': responsibilities,
                'office_address': office_address
            }
            return result

spider = SpecialSpider(
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


