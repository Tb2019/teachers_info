import asyncio
import re
from urllib import parse

import pandas as pd
import requests
from loguru import logger
from lxml import etree
import json
from crawler import ReCrawler
from utils import semaphore, headers, result_dict_2_df, drop_duplicate_collage, truncate_table, df2mysql, local_engine, \
    sf_engine, save_as_json

school_name = '广西大学'
college_name = '化学化工学院'
school_id = 9
college_id = 70
base_url = 'https://prof.gxu.edu.cn/backend/openapi/openSearch/findByCondition?dwlx=2&dwh=30400&xm=&xkml=&yjxk=&dslx=&firstLetter=&pageNum={pagenum}&pageSize=12'
start_urls = [base_url.format(pagenum=pagenum+1) for pagenum in range(15)]

a_s_xpath_str = None
target_div_xpath_str = None
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

def get_response(url):
    logger.info(f'crawling {url}...')
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        # resp.encoding = 'utf-8'
        logger.info(f'successfully get {url}')
        return resp.json()
    logger.warning(f'can not get {url}')

async def get_response_async(url, session, **kwargs):
    async with semaphore:
        try:
            logger.info(f'async crawling {url}...')
            async with session.get(url, headers=headers) as resp:
                if resp.ok:
                    return await resp.json(), [*zip(kwargs.keys(), kwargs.values())]
        except:
            pass

class SpecialSpider(ReCrawler):
    def parse_index(self, index_json, url):
        # index_json = json.loads(index_json)
        info_list = index_json['resData']['list']
        for info in info_list:
            gh = info['GH']
            name = info['XM']
            name = re.sub(r'\s*', '', name)
            name = re.sub(self.name_filter_re, '', name)
            link = 'https://prof.gxu.edu.cn/backend/openapi/openSearch/getTeachInfoByGH?GH=' + gh
            yield name, link

    def parse_detail(self, detail_page, url):
        if detail_page:
            json_info, info_s = detail_page
            print(json_info)
            json_info = json.loads(json_info)
            if json_info['resData']:
                name = info_s[0][1]

                phone = re.sub(r'\s*', '', json_info['resData']['baseInfo']['tel']) if json_info['resData']['baseInfo']['tel'] and re.sub(r'\s*', '', json_info['resData']['baseInfo']['tel']) else None
                if phone:
                    if len(phone) < 11:
                        phone = '0771-' + phone
                    elif len(phone) == 11:
                        phone = re.sub(r'(0771)(\d{7})', r'\1-\2', phone)
                    else:
                        phone = re.sub(r'\+??86-??771', '0771', phone)
                        phone = re.sub(r'\+86', '', phone)

                email = re.sub(r'\s*', '', json_info['resData']['baseInfo']['email']) if json_info['resData']['baseInfo']['email'] and re.sub(r'\s*', '', json_info['resData']['baseInfo']['email']) else None
                job_title = re.sub(r'\s*', '', json_info['resData']['baseInfo']['zhicheng']) if json_info['resData']['baseInfo']['zhicheng'] and re.sub(r'\s*', '', json_info['resData']['baseInfo']['zhicheng']) else None
                abstracts = json_info['resData']['largeMsg']['zyxxjx'] if json_info['resData']['largeMsg']['zyxxjx'] and re.sub(r'\s*', '', json_info['resData']['largeMsg']['zyxxjx']) else None
                directions = json_info['resData']['largeMsg']['zyyjfx'] if json_info['resData']['largeMsg']['zyyjfx'] and re.sub(r'\s*', '', json_info['resData']['largeMsg']['zyyjfx']) else None
                education_experience = None
                work_experience = None
                patent = None
                project = json_info['resData']['largeMsg']['zckyxm'] if json_info['resData']['largeMsg']['zckyxm'] and re.sub(r'\s*', '', json_info['resData']['largeMsg']['zckyxm']) else None
                award = json_info['resData']['largeMsg']['zz'] if json_info['resData']['largeMsg']['zz'] and re.sub(r'\s*', '', json_info['resData']['largeMsg']['zz']) else None
                social_job = json_info['resData']['largeMsg']['xsjz'] if json_info['resData']['largeMsg']['xsjz'] and re.sub(r'\s*', '', json_info['resData']['largeMsg']['xsjz']) else None
                full_src = json_info['resData']['baseInfo']['pic'] if json_info['resData']['baseInfo']['pic'] and re.sub(r'\s*', '', json_info['resData']['baseInfo']['pic']) else None

                qualification = re.sub(r'\s*', '', json_info['resData']['baseInfo']['topedu']) if json_info['resData']['baseInfo']['topedu'] and re.sub(r'\s*', '', json_info['resData']['baseInfo']['topedu']) else None
                education = re.sub(r'\s*', '', json_info['resData']['baseInfo']['ZHXWMC']) if json_info['resData']['baseInfo']['ZHXWMC'] and re.sub(r'\s*', '', json_info['resData']['baseInfo']['ZHXWMC']) else None
                # if qualification:
                #     print(qualification)
                #     qualification = re.search(r'博士|硕士|学士', qualification).group()
                #     if qualification == '博士' or '硕士':
                #         education = '研究生'
                #     else:
                #         education = '本科'
                # else:
                #     education = None

                job_information = 1
                responsibilities = None
                office_address = json_info['resData']['baseInfo']['address'] if json_info['resData']['baseInfo']['address'] and re.sub(r'\s*', '', json_info['resData']['baseInfo']['address']) else None


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

    def run(self):
        result_df = pd.DataFrame()
        for url in self.start_urls:
            index_json = get_response(url)
            index_result = self.parse_index(index_json, url)

            detail_pages = self.get_detail_page(index_result)
            for detail_page in detail_pages:
                # print('detail', detail_page)
                result = self.parse_detail(detail_page, url)
                print(result)
                # 防止网页本身为空
                if result:
                    result_df = result_dict_2_df(result_df, result)
                else:
                    continue

        # 去重
        # result_df.drop_duplicates(inplace=True, keep='first', subset=['name', 'email'])
        result_df = drop_duplicate_collage(result_df)

        # 保存至数据库
        if self.save2target == 'no':
            pass
        elif self.save2target == 'test':
            truncate_table(host='localhost', user='root', password='123456', database='alpha_search', port=3306,
                           table_name='search_teacher_test')
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


