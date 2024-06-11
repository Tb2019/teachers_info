# -*- coding: utf-8 -*-
import csv
import os
import re
import pandas as pd
import requests
from loguru import logger
from crawler import ReCrawler
from utils import csv_header, result_dict_2_df, drop_duplicate_collage, csv_2_df, truncate_table, \
    df2mysql, sf_engine, save_as_json, local_engine

school_name = '天津大学'
college_name = '机械工程学院'
school_id = 88
college_id = 150
img_url_head = None
partition_num = '022'
start_urls = [
                'https://me.tju.edu.cn/teacherPageNavi.action'
              ]

a_s_xpath_str = '//td[@id="teacherlist"]/table//a[@href!="#"]'
target_div_xpath_str = '/html/body/div/table[2]'

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
headers = {
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
  'Cache-Control': 'no-cache',
  'Connection': 'keep-alive',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Cookie': 'Hm_lvt_0eac3f7954950aa62e0d5e0919956fec=1718068320; Hm_lpvt_0eac3f7954950aa62e0d5e0919956fec=1718068331; JSESSIONID=3458F017089985A2FF2B6F230A729B32',
  'DNT': '1',
  'Origin': 'https://me.tju.edu.cn',
  'Pragma': 'no-cache',
  'Referer': 'https://me.tju.edu.cn/faculty_faculty.action?cla=4&userType=1',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
  'X-Requested-With': 'XMLHttpRequest',
  'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"'
}

# payload = "curr=1&count=310&limit=10&userType=1&dept=0"  # 教学科研系列
# payload = "curr=1&count=52&limit=10&userType=2&dept=0"  # 实验技术系列
payload = "curr=1&count=29&limit=10&userType=3&dept=0"  # 高教管理系列

def get_response(url, cn_com):
    logger.info(f'crawling {url}...')
    resp = requests.post(url, headers=headers, data=payload)
    if resp.status_code == 200:
        resp.encoding = 'utf-8'
        logger.info(f'successfully get {url}')
        return resp.json()
    logger.warning(f'can not get {url}')

class SpecialSpider(ReCrawler):
    def parse_index(self, index_page, url):
        teachers = index_page['data']
        for teacher in teachers:
            name = teacher['nameCn']
            id = teacher['id']
            if name:
                yield name, f'https://me.tju.edu.cn/faculty_teachers.action?cla=5&teacherid={id}'

    def run(self):
        if os.path.exists(f'{self.college_id}.csv'):
            file = open(f'{self.college_id}.csv', mode='a', newline='', encoding='utf-8')
            self.writter = csv.writer(file)
        else:
            file = open(f'{self.college_id}.csv', mode='a', newline='', encoding='utf-8')
            self.writter = csv.writer(file)
            self.writter.writerow(csv_header)
        self.result_df = pd.DataFrame()
        self.gpt_cant = []

        for url in self.start_urls:
            index_page = get_response(url, self.cn_com)  # cn_com转化为是否代理
            index_result = self.parse_index(index_page, url)

            detail_pages = self.get_detail_page(index_result)
            if self.api:
                print('接入api')
                mid_results = [self.parse_detail(detail_page, url) for detail_page in detail_pages]
                result = self.parse_by_api(mid_results)
            elif self.selenium_gpt:
                print('接入gpt')
                mid_results = [self.parse_detail(detail_page, url) for detail_page in detail_pages]
                self.parse_by_gpt(mid_results)
                print('*** too long to use gpt ***', self.gpt_cant)

            else:
                print('直接解析')
                for detail_page in detail_pages:
                    # print('detail', detail_page)
                    result = self.parse_detail(detail_page, url)
                    # result = mid_result
                    print(result)
                    # 防止网页本身为空
                    if result:
                        self.result_df = result_dict_2_df(self.result_df, result)
                    else:
                        continue
        file.close()

        # 去重
        # result_df.drop_duplicates(inplace=True, keep='first', subset=['name', 'email'])
        result_df = drop_duplicate_collage(self.result_df)

        # 保存至数据库
        if self.api:
            pass
        # gpt改用csv文件存储数据至数据库
        elif self.selenium_gpt:
            if not self.gpt_cant:
                try:
                    result_df = csv_2_df(f'./{self.college_id}.csv')
                    result_df = drop_duplicate_collage(result_df)
                    if self.save2target == 'no':
                        pass
                    elif self.save2target == 'test':
                        truncate_table(host='localhost', user='root', password='123456', database='alpha_search', port=3306,
                                       table_name='search_teacher_test')
                        df2mysql(engine=local_engine, df=result_df, table_name='search_teacher_test')
                    # elif self.save2target == 'local':
                    #     df2mysql(engine=local_engine, df=result_df, table_name='search_teacher')
                        logger.info('数据保存成功')
                    elif self.save2target == 'target':
                        df2mysql(engine=sf_engine, df=result_df, table_name='search_teacher')
                        save_as_json(result_df, self.school_name, self.college_name)
                        logger.info('数据保存成功')
                    # 删除csv
                    # os.remove(f'./{self.college_id}.csv')
                    # logger.info('csv文件已删除')
                except:
                    wait = input('数据有问题，请在excel中修改，修改完成后请输入1：')
                    if wait == '1':
                        try:
                            result_df = csv_2_df(f'./{self.college_id}.csv')
                            result_df = drop_duplicate_collage(result_df)
                            print(result_df)
                            logger.info('再次保存中...')
                            if self.save2target == 'no':
                                pass
                            elif self.save2target == 'test':
                                truncate_table(host='localhost', user='root', password='123456', database='alpha_search',
                                               port=3306,
                                               table_name='search_teacher_test')
                                df2mysql(engine=local_engine, df=result_df, table_name='search_teacher_test')
                                logger.info('数据保存成功')
                            # elif self.save2target == 'local':
                            #     df2mysql(engine=local_engine, df=result_df, table_name='search_teacher')
                            elif self.save2target == 'target':
                                df2mysql(engine=sf_engine, df=result_df, table_name='search_teacher')
                                save_as_json(result_df, self.school_name, self.college_name)
                                logger.info('数据保存成功')
                            # 删除csv
                            # os.remove(f'./{self.college_id}.csv')
                            # logger.info('csv文件已删除')
                        except:
                            logger.warning('文件仍有错误，请修改，之后手动存储，并删除csv文件')
            else:
                logger.info('存在未能解析的数据，请手动补充数据之后再手动存储数据')
        else:
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

            # update_rel_table(schoolid=self.school_id)
            # 删除csv
            os.remove(f'./{self.college_id}.csv')
            logger.info('csv文件已删除')



spider = SpecialSpider(
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


