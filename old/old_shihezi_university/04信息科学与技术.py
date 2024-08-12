from utils import get_response, get_response_async, result_dict_2_df, df2mysql, engine
from lxml import etree
import asyncio
import aiohttp
import re
import pandas as pd
from urllib import parse


def parse_index(index_page):
    page = etree.HTML(index_page)
    a_s = page.xpath('//div[@portletmode="simpleList"]/ul//a')
    for a in a_s:
        name = re.sub(r'\w+(?:—|-)+', '', a.xpath('.//text()')[0])
        link = parse.urljoin(url, a.xpath('./@href')[0])
        yield name, link


def get_detail_page(index_result):
    loop = asyncio.get_event_loop()
    session = aiohttp.ClientSession()
    tasks = [get_response_async(url, session, name=name) for name, url in index_result if len(name) >= 2]
    detail_pages = loop.run_until_complete(asyncio.gather(*tasks))
    session.connector.close()
    return detail_pages


def parse_detail(detail_page):
    page, info_s = detail_page
    page_tree = etree.HTML(page)
    try:
        target_div = page_tree.xpath('//div[@portletmode="simpleArticleAttri"]')[0]
    except:
        return None
    all_content = ''.join([re.sub(r'\s*', '', i) for i in target_div.xpath('.//text()') if re.sub(r'\s+', '', i)])
    all_content = re.sub('-{5,}', '', all_content)

    # 姓名
    name = re.sub(r'\s*', '', info_s[0][1])

    # 学校id
    school_id = 2

    # 学院id
    college_id = 4

    # 职称
    job_title = None
    try:
        job_title = re.findall(r'教授|副教授|讲师|研究员|\w{0,3}(?:工程师|实验师)', all_content)[0]
    except:
        pass

    # 电话
    phone = None
    try:
        phone_list = phone_pattern.findall(all_content)
        if len(phone_list) > 1:
            phone = ','.join(phone_list)
        else:
            phone = phone_list[0]
    except:
        pass

    # 邮箱
    email = None
    try:
        email_list = email_pattern.findall(all_content)
        if len(email_list) > 1:
            email = ','.join(email_list)
        else:
            email = email_list[0]
    except:
        pass

    # 学位、学历
    qualification = None
    education = None
    try:
        qualification = qualification_pattern.findall(all_content)[0]
        if qualification == '学士':
            education = '本科'
        else:
            education = '研究生'
    except:
        pass

    # 图片
    full_src = None
    try:
        src = target_div.xpath('.//img/@src')[0]
        full_src = parse.urljoin(url, src)
    except:
        pass

    # 研究方向
    directions = None
    for directions_pattern in directions_pattern_list:
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

    # 个人简介
    abstracts = None
    for abstracts_pattern in abstracts_pattern_list:
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

    # 办公室地点
    office_address = None
    try:
        office_address = office_address_pattern.findall(all_content)[0]
    except:
        pass

    # job_information
    job_information = 1

    # responsibilities
    responsibilities = None
    try:
        responsibilities = responsibilities_pattern.findall(all_content)[0]
    except:
        pass

    result = {
        'name': name,
        'school_id': school_id,
        'college_id': college_id,
        'job_title': job_title,
        'directions': directions,
        'picture': full_src,
        'phone': phone,
        'email': email,
        'qualification': qualification,
        'education': education,
        'job_information': job_information,
        'responsibilities': responsibilities,
        'abstracts': abstracts,
        'office_address': office_address
    }
    # print(result)
    return result

if __name__ == '__main__':
    start_urls = [
        'https://cs.shzu.edu.cn/js/list.htm',
        'https://cs.shzu.edu.cn/fjs/list.htm',
        'https://cs.shzu.edu.cn/fjs/list2.htm',
        'https://cs.shzu.edu.cn/dzxxzsds/list.htm',
        'https://cs.shzu.edu.cn/dzxxzsds/list2.htm',
        'https://cs.shzu.edu.cn/dzxxzsds/list3.htm',
        'https://cs.shzu.edu.cn/wlkjaqxsds/list.htm',
        'https://cs.shzu.edu.cn/tsqbxzsds/list.htm'
    ]

    phone_pattern = re.compile(r'(?<!\d)1\d{10}|\d{4}-\d{7}(?!\d)', re.S)
    email_pattern = re.compile(r'[a-zA-Z0-9._-]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9._-]+', re.S)
    qualification_pattern = re.compile(r'博士|硕士|学士', re.S)
    directions_pattern_list = [re.compile(r'研究领域(.*?)(?=系别|.荣誉)', re.S),
                               re.compile(r'主要研究内容(?:：|:)(.*?)(?=4)', re.S),
                               re.compile(r'研究兴趣(.*?).科研项目')
                               ]
    abstracts_pattern_list = [
        re.compile(r'工作经历(.*?).研究领域.*?.荣誉及奖励(.*?).开授', re.S),
        re.compile(r'基本情况(.*?)3')
    ]
    office_address_pattern = re.compile(r'办公室(\w*?)系别', re.S)
    responsibilities_pattern = re.compile(r'职务(\w*)电子信箱', re.S)

    result_df = pd.DataFrame()

    for url in start_urls:
        index_page = get_response(url)
        index_result = parse_index(index_page)

        detail_pages = get_detail_page(index_result)
        for detail_page in detail_pages:
            result = parse_detail(detail_page)
            # 防止网页本身为空
            if result:
                result_df = result_dict_2_df(result_df, result)
            else:
                continue
            # break
        # break
    # 去重
    result_df.drop_duplicates(inplace=True, keep='first', subset=['name', 'phone'])
    # 保存至数据库
    df2mysql(engine=engine, df=result_df, table_name='search_teacher_before')
