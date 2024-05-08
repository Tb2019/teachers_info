import asyncio
import re
from urllib import parse

import aiohttp
from lxml import etree

from crawler import ReCrawler
from utils import get_response_async

school_name = '宁夏大学'
college_name = '物理学院'
school_id = 4
college_id = 17
start_urls = ['https://phys.nxu.edu.cn/szdw/wlx1.htm',
              'https://phys.nxu.edu.cn/szdw/wlx1/4.htm',
              'https://phys.nxu.edu.cn/szdw/wlx1/3.htm',
              'https://phys.nxu.edu.cn/szdw/wlx1/2.htm',
              'https://phys.nxu.edu.cn/szdw/wlx1/1.htm',
              'https://phys.nxu.edu.cn/szdw/jcwlsyzx1.htm']

a_s_xpath_str = '//div[@class="ej_nr_box_main"]/div[@class="ej_szdw"]/ul/li/a'
target_div_xpath_str = '//div[@id="vsb_content_4" or @id="vsb_content_501" or @id="vsb_content" or @id="vsb_content_2"]'
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
class SpecialReCrawler(ReCrawler):
    def parse_index(self, index_page, url):
        page = etree.HTML(index_page)
        a_s = page.xpath(self.a_s_xpath_str)
        for a in a_s:
            name = a.xpath('.//text()')
            if name:
                name = name[5]
                name = re.sub(self.name_filter_re, '', name)
                link = a.xpath('./@href')[0]
                link = parse.urljoin(url, link)
                img = a.xpath('.//img/@src')[0]
                img = parse.urljoin(url, img)
            else:
                continue
            yield name, link, img

    def get_detail_page(self, index_result):
        loop = asyncio.get_event_loop()
        session = aiohttp.ClientSession()
        tasks = [get_response_async(url, session, name=name, img=img) for name, url, img in index_result if len(name) >= 2]
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

            # 姓名
            name = info_s[0][1]

            # 学校id
            school_id = self.school_id

            # 学院id
            college_id = self.college_id

            # 电话
            phone = None
            try:
                phone_list = self.phone_pattern.findall(all_content)
                if len(phone_list) > 1:
                    phone = ','.join(phone_list)
                else:
                    phone = phone_list[0]
            except:
                pass

            # 邮箱
            email = None
            try:
                email_list = self.email_pattern.findall(all_content)
                if len(email_list) > 1:
                    email = ','.join(email_list)
                else:
                    email = email_list[0]
            except:
                pass

            # 职称
            job_title = None
            try:
                job_title = self.job_title_pattern.findall(all_content)[0]
            except:
                pass

            # 个人简介
            abstracts = None
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
            full_src = info_s[1][1]

            # 学位、学历
            qualification = None
            education = None
            try:
                qualification = self.qualification_pattern.findall(all_content)[0]
                if qualification == '学士':
                    education = '本科'
                else:
                    education = '研究生'
            except:
                pass

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
                'social_job': social_job,
                'picture': full_src,
                'education': education,
                'qualification': qualification,
                'job_information': job_information,
                'responsibilities': responsibilities,
                'office_address': office_address
            }
            return result



spider = SpecialReCrawler(
                   school_name=school_name,
                   college_name=college_name,
                   school_id=school_id,
                   college_id=college_id,
                   # name_filter_re=r'导师简介',
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
                   save2target='simple'
                   )

spider.run()


