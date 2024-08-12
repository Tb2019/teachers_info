import re

import requests
from fake_headers import Headers
import asyncio
import aiohttp
from utils import get_response_async, result_dict_2_df, drop_duplicate_collage, local_engine, df2mysql, truncate_table, \
    sf_engine, save_as_json
import pandas as pd
from lxml import etree
from urllib import parse

school_name = '复旦大学'
college_name = '软件学院'
school_id = 105
college_id = 129
headers = Headers(headers=True).generate()
url = 'https://software.fudan.edu.cn/_wp3services/generalQuery?queryObj=articles'
data = {
    "siteId": "619",
    "columnId": "29336",
    "pageIndex": "1",
    "rows": "999",
    "orders": "[]",
    "returnInfos": "[{\"field\":\"title\",\"name\":\"title\"},{\"field\":\"f1\",\"name\":\"f1\"},{\"field\":\"f2\",\"name\":\"f2\"},{\"field\":\"f3\",\"name\":\"f3\"},{\"field\":\"f7\",\"name\":\"f7\"},{\"field\":\"f9\",\"name\":\"f9\"},{\"field\":\"mircImgPath\",\"name\":\"mircImgPath\"}]",
    "conditions": "[]"
}


def parse_index(index_resp):
    teachers_info = index_resp['data']
    for teacher_info in teachers_info:
        name = teacher_info['title']
        detail_url = teacher_info['wapUrl']
        yield name, detail_url

def get_detail_page(index_result):
    loop = asyncio.get_event_loop()
    session = aiohttp.ClientSession(headers=headers)
    tasks = [get_response_async(detail_url, session, name=name) for name, detail_url in index_result]
    detail_pages = loop.run_until_complete(asyncio.gather(*tasks))
    session.connector.close()
    return detail_pages

def parse_detail(detail_page):
    html, name_info = detail_page
    name = name_info[0][1]
    page = etree.HTML(html)

    phone = page.xpath('//div[@class="news_con"]/div[contains(text(), "电话")]/text()')
    phone = ''.join(phone)
    phone = re.sub(r'电话(?::|：)', '', phone)
    phone = phone if phone else None
    if phone:
        phone = re.sub(r'(?:-|\*)\d{3}', '', phone)
        if len(phone) == 8:
            phone = '021-' + phone

    email = page.xpath('//div[@class="news_con"]/div[contains(text(), "邮件")]/text()')
    email = ''.join(email)
    email = re.sub(r'邮件(?::|：)', '', email)

    job_title = page.xpath('//div[@class="news_con"]/div[contains(text(), "职称")]/text()')
    job_title = ''.join(job_title)
    job_title = re.sub(r'职称(?::|：)', '', job_title)

    office_address = page.xpath('//div[@class="news_con"]/div[contains(text(), "地址")]/text()')
    office_address = ''.join(office_address)
    office_address = re.sub(r'地址(?::|：)', '', office_address)

    directions = page.xpath('//div[@class="news_con"]/div[contains(text(), "研究方向/工作内容")]/text()')
    directions = ''.join(directions)
    directions = re.sub(r'研究方向/工作内容(?::|：)', '', directions)

    picture = page.xpath('//div[@class="news_imgs"]/img/@src')
    picture = ''.join(picture)
    if picture:
        picture = parse.urljoin(url, picture)

    result = {
        'name': name,
        'school_id': school_id,
        'college_id': college_id,
        'phone': phone,
        'email': email,
        'job_title': job_title,
        'abstracts': None,
        'directions': directions,
        'education_experience': None,
        'work_experience': None,
        'patent': None,
        'project': None,
        'award': None,
        'social_job': None,
        'picture': picture,
        'education': None,
        'qualification': None,
        'job_information': 1,
        'responsibilities': None,
        'office_address': office_address
    }
    print(result)
    return result


if __name__ == '__main__':
    result_df = pd.DataFrame()

    ajax_resp = requests.post(url, data=data, headers=headers).json()
    index_result = parse_index(ajax_resp)
    detail_pages = get_detail_page(index_result)
    for detail_page in detail_pages:
        result = parse_detail(detail_page)
        result_df = result_dict_2_df(result_df, result)

    result_df = drop_duplicate_collage(result_df)

    # truncate_table(host='localhost', user='root', password='123456', database='alpha_search', port=3306,
    #                table_name='search_teacher_test')
    # df2mysql(engine=local_engine, df=result_df, table_name='search_teacher_test')
    df2mysql(engine=sf_engine, df=result_df, table_name='search_teacher')
    # 保存成json至本地
    save_as_json(result_df, school_name, college_name)
