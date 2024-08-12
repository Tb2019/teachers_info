from utils import get_response, get_response_async, result_dict_2_df, df2mysql
from lxml import etree
import asyncio
import aiohttp
import re
import pandas as pd
from urllib import parse
from sqlalchemy import create_engine


def parse_index(index_page):
    page = etree.HTML(index_page)
    a_s = page.xpath('//div[@id="wp_content_w22_0"]//a')
    for a in a_s:
        name = a.xpath('.//text()')
        if name:
            name = name[0]
            name = re.sub(r'\s?\xa0\s?', '', name)
            link = a.xpath('./@href')[0]
        else:
            continue
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
        target_div = page_tree.xpath('//div[@class="content_txt"]')[0]
    except:
        return None
    all_content_sep = ''.join([re.sub(r'\s*', '', i) + ';' for i in target_div.xpath('.//text()') if re.sub(r'\s*', '', i)])
    all_content = ''.join([re.sub(r'\s*', '', i) for i in target_div.xpath('.//text()') if re.sub(r'\s+', '', i)])

    # 姓名
    name = re.sub(r'\s*', '', info_s[0][1])

    # school_id
    school_id = 2

    # 学院id
    college_id = 2

    # 职称
    job_title = None
    try:
        job_title = job_title_pattern.findall(all_content_sep)[0]
    except:
        try:
            job_title = re.findall(r'讲师|副教授|教授|研究员|\w{0,2}(?:工程师|实验师)', all_content)[0]
        except:
            pass

    # 研究方向
    directions = None
    try:
        directions = directions_pattern.findall(all_content)[0]
    except:
        directions_pattern_2 = re.compile(r'研究;?(?:领域|内容);?(?:：|:)?(.*?);', re.S)
        try:
            if len(directions_pattern_2.findall(all_content_sep)[0].replace(';', '')) > 5:
                directions = directions_pattern_2.findall(all_content_sep)[0].replace(';', '')
        except:
            pass

    # 图片
    full_src = None
    try:
        src = target_div.xpath('.//img/@src')[0]
        full_src = parse.urljoin(url, src)
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

    # job_information
    job_information = 1

    # responsibilities
    responsibilities = None

    # 个人简介
    abstracts = None
    try:
        abstracts = abstracts_pattern.findall(all_content)[0]
    except:
        try:
            abstracts_pattern_2 = re.compile(r'(^{name}.*?)(?=电子??邮|招生专业)'.format(name=name))
            abstracts = abstracts_pattern_2.findall(all_content)[0]
        except:
            pass

    # 办公室地点
    address = None

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
        'office_address': address
    }
    return result


if __name__ == '__main__':
    start_urls = ['https://jdxy.shzu.edu.cn/sssdsjj/list.htm', 'https://jdxy.shzu.edu.cn/bssdsjj/list.htm']
    result_df = pd.DataFrame()
    engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/alpha_search?charset=utf8')

    job_title_pattern = re.compile(r'职称;?(?:：|:);?(.*?);', re.S)
    directions_pattern = re.compile(r'研究(?:领域|内容)(?:：|:)?(.*?)(?=(?:\d、\w{2,})??科研项目)', re.S)
    phone_pattern = re.compile(r'(?<!\d)1\d{10}|\d{4}-\d{7}(?!\d)', re.S)
    email_pattern = re.compile(r'[a-zA-Z0-9._-]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9._-]+')
    qualification_pattern = re.compile(r'博士|硕士|学士', re.S)
    abstracts_pattern = re.compile('基本情况(1.*?2.*?)3、', re.S)

    for url in start_urls:
        index_page = get_response(url)
        index_result = parse_index(index_page)
        detail_pages = get_detail_page(index_result)
        for detail_page in detail_pages:
            result = parse_detail(detail_page)
            if result:
                result_df = result_dict_2_df(result_df, result)
            else:
                continue
            # break
        # break

    # 去重
    result_df.drop_duplicates(inplace=True, keep='first', subset=['name', 'phone', 'email'])
    # 保存至数据库
    df2mysql(engine=engine, df=result_df, table_name='search_teacher_before')
