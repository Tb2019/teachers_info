import asyncio
import re
from urllib import parse

import aiohttp
from lxml import etree
from lxml.html import tostring

from crawler import ReCrawler
from utils import get_response_async

school_name = '复旦大学'
college_name = '物理学系'
school_id = 105
college_id = 121
start_urls = [
                'https://phys.fudan.edu.cn/7476/list.htm'
              ]

a_s_xpath_str = '//table[@class="wp_editor_art_paste_table"]/tbody/tr[position()>1]'
target_div_xpath_str = '//div[@class="Article_Content"]'

# # 电话
# phone_xpath = None

# # 邮箱
# email_xpath = None

# # 职称
# job_title_xpath = None

# # 学位
# qualification_xpath = None

# 研究方向
# directions_pattern_list = [
#                             re.compile(r'(?<!教学与)研究领域(?:：|:)(.*?(?:\.|。)?)(?:\^\^)?[A-Z]', re.S),
#                             re.compile(r'教学与研究领域(?:：|:)(.*?(?:\.|。)?)(?:\^\^)?[A-Z]', re.S)
#                           ]
directions_xpath = '//*[contains(text(), "教学与研究领域")]/ancestor::p[1]/self::*|//*[contains(text(), "教学与研究领域")]/ancestor::p/following-sibling::*'
paper_xpath = '//*[contains(text(), "Publications")]/ancestor::p[1]/self::*|//*[contains(text(), "Publications")]/ancestor::p/following-sibling::*'

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

# # 专利
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

# # 社会兼职
# social_job_pattern_list = [
#                                     re.compile(r'', re.S),
#                                     re.compile(r'', re.S)
#                                 ]
# social_job_xpath = None

# # 图片
# img_xpath = None


class SpecialSpider(ReCrawler):
    def parse_index(self, index_page, url):
        page = etree.HTML(index_page)
        a_s = page.xpath(self.a_s_xpath_str)
        for a in a_s:
            name = ' '.join(a.xpath('.//a//text()'))
            # print(name)
            if name:
                name = ''.join(name)
                if not re.match(r'[A-Za-z\s]*$', name, re.S):  # 中文名替换空格
                    name = re.sub(r'\s*', '', name)
                name = re.sub(self.name_filter_re, '', name)
                link = a.xpath('.//a/@href')[0]
                link = parse.urljoin(url, link)

                try:
                    job_title = a.xpath('./td[not(@rowspan) and @bgcolor][2]//text()')[0]
                except:
                    job_title = None
                try:
                    office_address = ''.join(a.xpath('./td[not(@rowspan) and @bgcolor][5]//text()'))
                except:
                    office_address = None

                try:
                    phone = a.xpath('./td[not(@rowspan) and @bgcolor][4]//text()')[0]
                    phone = re.sub(r'\+86-21-|-', '', phone)
                except:
                    phone = None

                try:
                    email = a.xpath('./td[not(@rowspan) and @bgcolor][3]//text()')[0]
                except:
                    email = None
            else:
                print('未解析到name，请检查：a_s_xpath_str')
                continue
            yield name, link, job_title, office_address, phone, email

    def get_detail_page(self, index_result):
        loop = asyncio.get_event_loop()
        session = aiohttp.ClientSession()
        tasks = [get_response_async(url, session, name=name, job_title=job_title, office_address=office_address, phone=phone, email=email) for name, url, job_title, office_address, phone, email in index_result if len(name) >= 2]
        detail_pages = loop.run_until_complete(asyncio.gather(*tasks))
        session.connector.close()
        return detail_pages

    def parse_detail(self, detail_page, url):
        if detail_page:
            page, info_s = detail_page
            page_tree = etree.HTML(page)
            try:
                target_div = page_tree.xpath(self.target_div_xpath_str)[0]
            except:
                print('未发现内容标签', url)
                return None
            all_content = ''.join(
                [re.sub(r'\s*', '', i) for i in target_div.xpath('.//text()') if re.sub(r'\s+', '', i)]
            )
            all_content = re.sub(r'-{5,}', '', all_content)

            content_with_label = tostring(target_div, encoding='utf-8').decode('utf-8')


            # 姓名
            name = info_s[0][1]

            # 学校id
            school_id = self.school_id

            # 学院id
            college_id = self.college_id

        # if not self.api:  # 不使用第三方api解析
            # 电话
            phone = None
            if info_s[3][1]:
                phone = info_s[3][1]
            else:
                if self.phone_xpath:
                    try:
                        phone_list = target_div.xpath(self.phone_xpath)
                        phone = ','.join(phone_list) if ','.join(phone_list) else None
                    except:
                        print('phone_xpath错误')
                else:
                    try:
                        phone_list = list(set(self.phone_pattern.findall(all_content)))
                        if len(phone_list) > 1:
                            phone = ','.join(phone_list)
                        else:
                            phone = phone_list[0]
                        # phone = re.sub(r'——', '-', phone)
                    except:
                        pass
                if phone:
                    phone = re.sub(r'\+?86-(\d+-)?', '', phone)
            if phone and len(phone) == 8:
                phone = '021-' + phone

            # 邮箱
            email = None
            if info_s[4][1]:
                email = info_s[4][1]
            else:
                if self.email_xpath:
                    try:
                        email_list = target_div.xpath(self.email_xpath)
                        email = ','.join(email_list) if ','.join(email_list) else None
                    except:
                        print('email_xpath错误')
                else:
                    try:
                        email_list = list(set(self.email_pattern.findall(all_content)))
                        if len(email_list) > 1:
                            email = ','.join(email_list)
                        else:
                            email = email_list[0]
                        # email = re.sub(r'(?:\(at\)|\(AT\)|\[at]|\[AT])', '@', email)
                    except:
                        pass
                if email:
                    email = re.sub(r'\(?\s?at\s?\)?|\(?\s?AT\s?\)?|\[?\s?at\s?]?|\[?\s?AT\s?]?', '@', email)
                    email = re.sub(r'Website', '', email)

            # 职称
            job_title = None
            if info_s[1][1]:
                job_title = info_s[1][1]
            else:
                if self.job_title_xpath:
                    try:
                        job_title_list = target_div.xpath(self.job_title_xpath)
                        job_title = ','.join(job_title_list) if ','.join(job_title_list) else None
                    except:
                        print('job_title_xpath错误')
                else:
                    try:
                        job_title = self.job_title_pattern.findall(all_content)[0]
                    except:
                        pass

            # 个人简介
            abstracts = None
            if self.abstracts_xpath:
                try:
                    abstracts_list = target_div.xpath(self.abstracts_xpath)
                    abstracts = ','.join(abstracts_list) if ','.join(abstracts_list) else None
                except:
                    print('abstracts_xpath错误')
            else:
                if self.abstracts_pattern_list:
                    for abstracts_pattern in self.abstracts_pattern_list:
                        try:
                            abstracts = abstracts_pattern.findall(all_content)[0]
                            # abstracts = abstracts.replace('-', '')
                            if abstracts:
                                if isinstance(abstracts, tuple):
                                    abstracts = ';'.join(abstracts)
                                break
                            else:
                                continue
                        except:
                            continue

            # 研究方向
            directions = None
            if self.directions_xpath:
                try:
                    directions = ''
                    directions_list = target_div.xpath(self.directions_xpath)
                    for direction_element in directions_list:
                        directions += tostring(direction_element, encoding='utf-8').decode('utf-8')
                    if not directions:
                        directions = None

                except:
                    print('directions_xpath错误')
            else:
                if self.directions_pattern_list:
                    for directions_pattern in self.directions_pattern_list:
                        try:
                            directions = directions_pattern.findall(all_content)[0]
                            if directions:
                                if isinstance(directions, tuple):
                                    directions = ';'.join(directions)
                                break
                            else:
                                continue
                        except:
                            continue

            # 教育经历
            education_experience = None
            if self.education_experience_xpath:
                try:
                    education_experience_list = target_div.xpath(self.education_experience_xpath)
                    education_experience = ','.join(education_experience_list) if ','.join(education_experience_list) else None
                except:
                    print('education_experience_xpath错误')
            else:
                if self.education_experience_pattern_list:
                    for education_experience_pattern in self.education_experience_pattern_list:
                        try:
                            education_experience = education_experience_pattern.findall(all_content)[0]
                            if education_experience:
                                if isinstance(education_experience, tuple):
                                    education_experience = ';'.join(education_experience)
                                break
                            else:
                                continue
                        except:
                            continue

            # 工作经历
            work_experience = None
            if self.work_experience_xpath:
                try:
                    work_experience_list = target_div.xpath(self.work_experience_xpath)
                    work_experience = ','.join(work_experience_list) if ','.join(work_experience_list) else None
                except:
                    print('work_experience_xpath错误')
            else:
                if self.work_experience_pattern_list:
                    for work_experience_pattern in self.work_experience_pattern_list:
                        try:
                            work_experience = work_experience_pattern.findall(all_content)[0]
                            if work_experience:
                                if isinstance(work_experience, tuple):
                                    work_experience = ';'.join(work_experience)
                                break
                            else:
                                continue
                        except:
                            continue

            # 专利
            patent = None
            if self.patent_xpath:
                try:
                    patent_list = target_div.xpath(self.patent_xpath)
                    patent = ','.join(patent_list) if ','.join(patent_list) else None
                except:
                    print('patent_xpath错误')
            else:
                if self.patent_pattern_list:
                    for patent_pattern in self.patent_pattern_list:
                        try:
                            patent = patent_pattern.findall(all_content)[0]
                            if patent:
                                if isinstance(patent, tuple):
                                    patent = ';'.join(patent)
                                break
                            else:
                                continue
                        except:
                            continue

            # 科研项目
            project = None
            if self.project_xpath:
                try:
                    project_list = target_div.xpath(self.project_xpath)
                    project = ','.join(project_list) if ','.join(project_list) else None
                except:
                    print('project_xpath错误')
            else:
                if self.project_pattern_list:
                    for project_pattern in self.project_pattern_list:
                        try:
                            project = project_pattern.findall(all_content)[0]
                            if project:
                                if isinstance(project, tuple):
                                    project = ';'.join(project)
                                break
                            else:
                                continue
                        except:
                            continue

            # 荣誉/获奖信息
            award = None
            if self.award_xpath:
                try:
                    award_list = target_div.xpath(self.award_xpath)
                    award = ','.join(award_list) if ','.join(award_list) else None
                except:
                    print('award_xpath错误')
            else:
                if self.award_pattern_list:
                    for award_pattern in self.award_pattern_list:
                        try:
                            award = award_pattern.findall(all_content)[0]
                            if award:
                                if isinstance(award, tuple):
                                    award = ';'.join(award)
                                break
                            else:
                                continue
                        except:
                            continue

            # 社会兼职
            social_job = None
            if self.social_job_xpath:
                try:
                    social_job_list = target_div.xpath(self.social_job_xpath)
                    social_job = ','.join(social_job_list) if ','.join(social_job_list) else None
                except:
                    print('social_job_xpath错误')
            else:
                if self.social_job_pattern_list:
                    for social_job_pattern in self.social_job_pattern_list:
                        try:
                            social_job = social_job_pattern.findall(all_content)[0]
                            if social_job:
                                if isinstance(social_job, tuple):
                                    social_job = ';'.join(social_job)
                                break
                            else:
                                continue
                        except:
                            continue
            # 图片
            full_src = None
            if self.img_xpath:
                try:
                    img_list = target_div.xpath(self.img_xpath)
                    src = ','.join(img_list) if ','.join(img_list) else None
                except:
                    print('img_xpath错误')
            else:
                try:
                    src = target_div.xpath('.//img[@src!=""]/@src')[0]
                    # full_src = parse.urljoin(url, src)
                except:
                    pass
            full_src = parse.urljoin(url, src)

            # 论文
            paper = None
            if self.paper_xpath:
                try:
                    paper = ''
                    paper_list = target_div.xpath(self.paper_xpath)
                    for paper_element in paper_list:
                        paper += tostring(paper_element, encoding='utf-8').decode('utf-8')
                    if not paper:
                        paper = None

                except:
                    print('paper_xpath错误')
            else:
                if self.paper_pattern_list:
                    for paper_pattern in self.paper_pattern_list:
                        try:
                            paper = paper_pattern.findall(all_content)[0]
                            if paper:
                                if isinstance(paper, tuple):
                                    paper = ';'.join(paper)
                                break
                            else:
                                continue
                        except:
                            continue

            # 学位、学历
            qualification = None
            education = None
            edu_dict = {'学士': 1, '硕士': 2, '博士': 3}
            edu_code = 0
            if self.qualification_xpath:
                try:
                    qualification_list = target_div.xpath(self.qualification_xpath)
                    qualification = ','.join(qualification_list) if ','.join(qualification_list) else None
                    if qualification == '学士':
                        education = '本科'
                    elif qualification == '硕士':
                        education = '研究生'
                    elif qualification == '博士':
                        education = '研究生'
                except:
                    print('qualification_xpath错误')
            else:
                try:
                    qualification_list = self.qualification_pattern.findall(all_content)
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
            # try:
            #     qualification = self.qualification_pattern.findall(all_content)[0]
            #     if qualification == '学士':
            #         education = '本科'
            #     else:
            #         education = '研究生'
            # except:
            #     pass

            # 在职信息
            job_information = 1
            if self.job_information_pattern_list:
                for job_information_pattern in self.job_information_pattern_list:
                    try:
                        job_information = job_information_pattern.findall(all_content)[0]
                        if job_information:
                            if isinstance(job_information, tuple):
                                job_information = ';'.join(job_information)
                            break
                        else:
                            continue
                    except:
                        continue

            # 主要任职
            responsibilities = None
            if self.responsibilities_xpath:
                try:
                    responsibilities_list = target_div.xpath(self.responsibilities_xpath)
                    responsibilities = ','.join(responsibilities_list) if ','.join(responsibilities_list) else None
                except:
                    print('responsibilities_xpath错误')
            else:
                if self.responsibilities_pattern_list:
                    for responsibilities_pattern in self.responsibilities_pattern_list:
                        try:
                            responsibilities = responsibilities_pattern.findall(all_content)[0]
                            if responsibilities:
                                if isinstance(responsibilities, tuple):
                                    responsibilities = ';'.join(responsibilities)
                                break
                            else:
                                continue
                        except:
                            continue

            # 办公室地点
            office_address = None
            if info_s[2][1]:
                office_address = info_s[2][1]
            else:
                if self.office_address_xpath:
                    try:
                        office_address_list = target_div.xpath(self.office_address_xpath)
                        office_address = ','.join(office_address_list) if ','.join(office_address_list) else None
                    except:
                        print('office_address_xpath错误')
                else:
                    if self.office_address_pattern_list:
                        for office_address_pattern in self.office_address_pattern_list:
                            try:
                                office_address = office_address_pattern.findall(all_content)[0]
                                if office_address:
                                    if isinstance(office_address, tuple):
                                        office_address = ';'.join(office_address)
                                    break
                                else:
                                    continue
                            except:
                                continue

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
                'paper': paper,
                'social_job': social_job,
                'picture': full_src,
                'education': education,
                'qualification': qualification,
                'job_information': job_information,
                'responsibilities': responsibilities,
                'office_address': office_address
            }
            # return result
            if self.api:  # 使用第三方api解析
                return content_with_label, result
            else:
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
                   phone_pattern=re.compile(r'(?<!\d)(?:\+?86-)?1\d{10}(?!\d)|(?<!\d)\d{3,4}(?:-|——)\d{7,8}(?!\d)|(?:\+?86-\d+-)\d{8}', re.S),
                   email_pattern=re.compile(r'[a-zA-Z0-9._-]+(?:@|\(at\)|\(AT\)|\[at]|\[AT])(?=.{1,10}(?:\.com|\.cn|\.net))[a-zA-Z0-9_-]+\.[0-9a-zA-Z._-]+',re.S),

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
                   directions_xpath=directions_xpath,
                   paper_xpath=paper_xpath,
                   # award_xpath=award_xpath,
                   # social_job_xpath=social_job_xpath,
                   # img_xpath=img_xpath,

                   save2target='test',
                   # api=False,
                   )

spider.run()


