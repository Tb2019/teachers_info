from lxml import etree
from lxml.html import fromstring, tostring
import asyncio
import aiohttp
import re
import pandas as pd
from urllib import parse
from utils import get_response, get_response_async, result_dict_2_df, df2mysql, local_engine, sf_engine, \
    drop_duplicate_collage, save_as_json, truncate_table, api_parse


class ReCrawler:
    def __init__(self,
                 school_name: str,
                 college_name: str,
                 school_id: int,
                 college_id: int,
                 start_urls: list,
                 a_s_xpath_str: [str, None],
                 target_div_xpath_str: [str, None],
                 name_filter_re=r'\s*',
                 directions_pattern_list: [None, list] = None,
                 abstracts_pattern_list: [None, list] = None,
                 office_address_pattern_list: [None, list] = None,
                 job_information_pattern_list: [None, list] = None,
                 responsibilities_pattern_list: [None, list] = None,
                 education_experience_pattern_list: [None, list] = None,
                 work_experience_pattern_list: [None, list] = None,
                 patent_pattern_list: [None, list] = None,
                 project_pattern_list: [None, list] = None,
                 award_pattern_list: [None, list] = None,
                 social_job_pattern_list: [None, list] = None,
                 job_title_pattern=re.compile(r'院士|教授|副教授|讲师|副?研究员|正?高级?助理?(?:工程师|实验师)|副?主任医师', re.S),
                 phone_pattern=re.compile(r'(?<!\d)1\d{10}(?!\d)|(?<!\d)\d{3,4}(?:-|——)\d{7,8}(?!\d)', re.S),
                 # email_pattern=re.compile(r'[a-zA-Z0-9._-]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9._-]+', re.S),
                 # email_pattern=re.compile(r'[a-zA-Z0-9._-]+(?:@|\(at\)|\(AT\)|\[at]|\[AT])(?=.{1,20}(?:\.com|\.cn))[a-zA-Z0-9_-]+\.[a-zA-Z._-]+', re.S),
                 # email_pattern=re.compile(r'[a-zA-Z0-9._-]+(?:@|\(at\)|\(AT\)|\[at]|\[AT])(?=.{1,10}(?:\.com|\.cn))[a-zA-Z0-9_-]+\.[0-9a-zA-Z._-]+',re.S),
                 email_pattern=re.compile(r'[a-zA-Z0-9._-]+(?:@|\(at\)|\(AT\)|\[at]|\[AT])[a-zA-Z0-9_-]+\.[a-zA-Z._-]+', re.S),
                 qualification_pattern=re.compile(r'博士|硕士|学士', re.S),
                 save2target='test',
                 api=False,
                 # is_regular=False,
                 phone_xpath: [None, str] = None,
                 email_xpath: [None, str] = None,
                 job_title_xpath: [None, str] = None,
                 qualification_xpath: [None, str] = None,
                 directions_xpath: [None, str] = None,
                 abstracts_xpath: [None, str] = None,
                 office_address_xpath: [None, str] = None,
                 job_information_xpath: [None, str] = None,
                 responsibilities_xpath: [None, str] = None,
                 education_experience_xpath: [None, str] = None,
                 work_experience_xpath: [None, str] = None,
                 patent_xpath: [None, str] = None,
                 project_xpath: [None, str] = None,
                 award_xpath: [None, str] = None,
                 social_job_xpath: [None, str] = None,
                 img_xpath: [None, str] = None
                 ):
        """

        :param school_id: 学校id
        :param college_id: 学院id
        :param start_urls:
        :param a_s_xpath_str: 列表页超链接a标签的xpath路径
        :param target_div_xpath_str: 包含全部教师信息的div标签xpath路径
        :param directions_pattern_list:
        :param abstracts_pattern_list:
        :param name_filter_re: 过滤列表页提取到的姓名，默认过滤空白字符
        :param office_address_pattern_list:
        :param job_information_pattern_list:
        :param responsibilities_pattern_list:
        :param job_title_pattern:
        :param phone_pattern:
        :param email_pattern:
        :param qualification_pattern:
        :param save2target: 默认false，不保存至目标表；true则保存至before表
        :return:
        """
        self.school_name = school_name
        self.college_name = college_name
        self.school_id = school_id
        self.college_id = college_id
        self.start_urls = start_urls

        self.a_s_xpath_str = a_s_xpath_str
        self.target_div_xpath_str = target_div_xpath_str

        self.name_filter_re = name_filter_re

        self.directions_pattern_list = directions_pattern_list
        self.abstracts_pattern_list = abstracts_pattern_list
        self.office_address_pattern_list = office_address_pattern_list
        self.education_experience_pattern_list = education_experience_pattern_list
        self.work_experience_pattern_list = work_experience_pattern_list
        self.patent_pattern_list = patent_pattern_list
        self.project_pattern_list = project_pattern_list
        self.award_pattern_list = award_pattern_list
        self.social_job_pattern_list = social_job_pattern_list

        self.job_title_pattern = job_title_pattern
        self.phone_pattern = phone_pattern
        self.email_pattern = email_pattern
        self.qualification_pattern = qualification_pattern
        self.job_information_pattern_list = job_information_pattern_list
        self.responsibilities_pattern_list = responsibilities_pattern_list

        self.save2target = save2target

        self.api = api

        # self.is_regular = is_regular

        self.phone_xpath = phone_xpath
        self.email_xpath = email_xpath
        self.job_title_xpath = job_title_xpath
        self.qualification_xpath = qualification_xpath
        self.directions_xpath = directions_xpath
        self.abstracts_xpath = abstracts_xpath
        self.office_address_xpath = office_address_xpath
        self.job_information_xpath = job_information_xpath
        self.responsibilities_xpath = responsibilities_xpath
        self.education_experience_xpath = education_experience_xpath
        self.work_experience_xpath = work_experience_xpath
        self.patent_xpath = patent_xpath
        self.project_xpath = project_xpath
        self.award_xpath = award_xpath
        self.social_job_xpath = social_job_xpath
        self.img_xpath = img_xpath

    def parse_index(self, index_page, url):
        page = etree.HTML(index_page)
        a_s = page.xpath(self.a_s_xpath_str)
        for a in a_s:
            name = a.xpath('.//text()')
            # print(name)
            if name:
                name = ''.join(name)
                if not re.match(r'[A-Za-z\s]*$', name, re.S):  # 中文名替换空格
                    name = re.sub(r'\s*', '', name)
                name = re.sub(self.name_filter_re, '', name)
                link = a.xpath('./@href')[0]
                link = parse.urljoin(url, link)
            else:
                print('未解析到name，请检查：a_s_xpath_str')
                continue
            yield name, link

    def get_detail_page(self, index_result):
        loop = asyncio.get_event_loop()
        session = aiohttp.ClientSession()
        tasks = [get_response_async(url, session, name=name) for name, url in index_result if len(name) >= 2]
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
                    phone = re.sub(r'——', '-', phone)
                except:
                    pass
            # phone = re.sub(r'——', '-', phone)

            # 邮箱
            email = None
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
                    email = re.sub(r'\(?\s?at\s?\)?|\(?\s?AT\s?\)?|\[?\s?at\s?]?|\[?\s?AT\s?]?', '@', email)

                except:
                    pass
            # email = re.sub(r'\(?\s?at\s?\)?|\(?\s?AT\s?\)?|\[?\s?at\s?]?|\[?\s?AT\s?]?', '@', email)

            # 职称
            job_title = None
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
                    directions_list = target_div.xpath(self.directions_xpath)
                    directions = ','.join(directions_list) if ','.join(directions_list) else None
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
                    full_src = parse.urljoin(url, src)
                except:
                    pass
            # full_src = parse.urljoin(url, src)

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
                'social_job': social_job,
                'picture': full_src,
                'education': education,
                'qualification': qualification,
                'job_information': job_information,
                'responsibilities': responsibilities,
                'office_address': office_address
            }
            # return result
            if self.api:# 使用第三方api解析
                return content_with_label, result
            else:
                return result

    def parse_by_api(self, mid_result):
        loop = asyncio.get_event_loop()
        session = aiohttp.ClientSession()
        tasks = [api_parse(result_gen, session) for result_gen in mid_result]
        results = loop.run_until_complete(asyncio.gather(*tasks))
        session.connector.close()
        print(results)
        # todo:后续逻辑没有继续写
        # for result in results:
        #     api_result, direct_result = result


    def run(self):
        result_df = pd.DataFrame()
        for url in self.start_urls:
            index_page = get_response(url)
            index_result = self.parse_index(index_page, url)

            detail_pages = self.get_detail_page(index_result)
            if not self.api:
                print('直接解析')
                for detail_page in detail_pages:
                    # print('detail', detail_page)
                    result = self.parse_detail(detail_page, url)
                    # result = mid_result
                    print(result)
                    # 防止网页本身为空
                    if result:
                        result_df = result_dict_2_df(result_df, result)
                    else:
                        continue
            else:
                print('接入api')
                mid_result = [self.parse_detail(detail_page, url) for detail_page in detail_pages]
                result = self.parse_by_api(mid_result)


        # 去重
        # result_df.drop_duplicates(inplace=True, keep='first', subset=['name', 'email'])
        result_df = drop_duplicate_collage(result_df)

        # 保存至数据库
        if self.save2target == 'no':
            pass
        elif self.save2target == 'test':
            truncate_table(host='localhost', user='root', password='123456', database='alpha_search', port=3306, table_name='search_teacher_test')
            df2mysql(engine=local_engine, df=result_df, table_name='search_teacher_test')
        # elif self.save2target == 'local':
        #     df2mysql(engine=local_engine, df=result_df, table_name='search_teacher')
        elif self.save2target == 'target':
            df2mysql(engine=sf_engine, df=result_df, table_name='search_teacher')
            save_as_json(result_df, self.school_name, self.college_name)
        # elif self.save2target == 'simple':
        #     df2mysql(engine=sf_engine, df=result_df, table_name='search_teacher_simple')
        #     # 保存成json至本地
        #     save_as_json(result_df, self.school_name, self.college_name)
