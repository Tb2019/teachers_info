from utils import get_response, get_response_async, result_dict_2_df, df2mysql, engine
from lxml import etree
import asyncio
import aiohttp
import re
import pandas as pd
from urllib import parse


def parse_index(index_page):
    page = etree.HTML(index_page)
    a_s = page.xpath('//div[@id="wp_content_w6_0"]//a')
    for a in a_s:
        name = a.xpath('.//text()')
        if name:
            name = name[0]
            name = re.sub(r'\s', '', name)
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
        target_div = page_tree.xpath('//div[@class="infobox"]')[0]
    except:
        return None
    all_content = ''.join([re.sub(r'\s*', '', i) for i in target_div.xpath('.//text()') if re.sub(r'\s+', '', i)]).replace('-', '')

    # 姓名
    name = re.sub(r'\s*', '', info_s[0][1])

    # 学校id
    school_id = 2

    # 学院id
    college_id = 3

    # 职称
    job_title = None
    try:
        job_title = re.findall(r'讲师|副教授|教授|研究员|\w{0,3}(?:工程师|实验师)', all_content)[0]
    except:
        pass

    # 研方向究
    directions = None
    try:
        directions = directions_pattern.findall(all_content)[0]
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
    try:
        responsibilities = responsibilities_pattern.findall(all_content)[0]
    except:
        pass

    # 个人简介
    abstracts = None
    try:
        abstracts = abstracts_pattern.findall(all_content)[0]
        # abstracts = abstracts.replace('-', '')
    except:
        pass

    # 办公室地点
    office_address = None
    try:
        office_address = office_address_pattern.findall(all_content)[0]
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
    return result


if __name__ == '__main__':
    start_urls = [
        'https://spxy.shzu.edu.cn/zjrc/list.htm',
        'https://spxy.shzu.edu.cn/2935/list.htm',
        'https://spxy.shzu.edu.cn/2936/list.htm',
        'https://spxy.shzu.edu.cn/js/list.htm',
    ]
    result_df = pd.DataFrame()

    directions_pattern = re.compile(r'教育背景.*?研究方向(?::|：)?(.*?)(?:科研项目|学术论文|承担教学)', re.S)
    phone_pattern = re.compile(r'(?<!\d)1\d{10}|\d{4}-\d{7}(?!\d)', re.S)
    email_pattern = re.compile(r'[a-zA-Z0-9._-]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9._-]+', re.S)
    qualification_pattern = re.compile(r'博士|硕士|学士', re.S)
    responsibilities_pattern = re.compile(r'职位(?::|：)?(.*?)个人简介', re.S)
    abstracts_pattern = re.compile(r'个人简介(?::|：)?(.*?)社会兼职', re.S)
    office_address_pattern = re.compile(r'通讯地址(?::|：)?(.*?)(?:职位|个人简介)')


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
    result_df.drop_duplicates(inplace=True, keep='first', subset=['name', 'phone', 'email'])
    # 保存至数据库
    df2mysql(engine=engine, df=result_df, table_name='search_teacher_before')