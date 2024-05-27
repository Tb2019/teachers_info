import os
import json
import re

import pymysql
import requests
import pandas as pd
from loguru import logger
from itertools import chain
from asyncio import Semaphore
from fake_headers import Headers
from urllib.parse import quote_plus
from sqlalchemy import create_engine


proxy = {
    'http': '127.0.0.1:7890',
    'https': '127.0.0.1:7890',
}

headers = Headers(headers=True).generate()
api_headers =  {
    'Authorization': 'Bearer pat_BeF0pCJRtoqSyqesxUUtaQgajL9EAcHzRjlI1ZqFyhGhFV3mTRfIuyKvU5nRHhIB',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Host': 'api.coze.com',
    'Connection': 'keep-alive',
}

semaphore = Semaphore(5)
semaphore_api = Semaphore(20)

api_base_url = 'https://api.coze.com/open_api/v2/chat'

sf_password = 'Shufang_@919'

# engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/alpha_search?charset=utf8')
local_engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/alpha_search?charset=utf8')
sf_engine = create_engine(f'mysql+pymysql://root:{quote_plus(sf_password)}@192.168.2.12:3306/alpha_search?charset=utf8')


def get_response(url, cn_com):
    logger.info(f'crawling {url}...')
    if cn_com == 'com':
        resp = requests.get(url, headers=headers, proxies=proxy)
    else:
        resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        resp.encoding = 'utf-8'
        logger.info(f'successfully get {url}')
        return resp.text
    logger.warning(f'can not get {url}')


async def get_response_async(url, session, **kwargs):
    async with semaphore:
        try:
            logger.info(f'async crawling {url}...')
            async with session.get(url, headers=headers) as resp:
                if resp.ok:
                    return await resp.text(encoding='utf-8'), [*zip(kwargs.keys(), kwargs.values())]
                else:
                    print('请求失败', url)
        except:
            pass


async def api_parse(result_gen, session):
    for unpack in result_gen:
        content_with_label, result = unpack
    data = {
        "conversation_id": "123",
        "bot_id": "7363503511164207109",
        "user": "123333333",
        "query": content_with_label,
        "stream": False
    }
    async with semaphore_api:
        logger.info('request api to parse')
        async with session.post(api_base_url, data=json.dumps(data), headers=api_headers, proxy='http://127.0.0.1:7890') as resp:
            if resp.ok:
                return await resp.json(), result


def result_dict_2_df(empty_df, result: dict):
    """
    将返回的字典数据转化为df，方便去重操作
    :param empty_df:
    :param result:
    :return:
    """
    temp_df = pd.DataFrame([result])
    result_df = pd.concat([empty_df, temp_df], ignore_index=True)
    return result_df


def df2mysql(engine, df, table_name):
    # engine = create_engine(engine_string)
    with engine.begin() as conn:
        df.to_sql(name=table_name, con=conn, if_exists='append', index=False)


def save_as_json(df, school_name, college_name):
    path = f'../Results/{school_name}'
    os.path.exists(path) or os.makedirs(path)

    # json_format = df.drop('id', axis=1).to_dict('records')
    json_format = df.to_dict('records')

    with open(path + f'/{college_name}.json', mode='w', encoding='utf-8') as f:
        f.write(json.dumps(json_format, ensure_ascii=False))



def get_split(element):
    """
    分割同一字段中的多个号码
    :param element:
    :return:
    """
    try:
        element = element.lower().split(',')
        return element
    except:
        return [element]

def get_most_info(df):
    """
    保留信息量最大的一条记录
    :param df:
    :return:
    """
    df['info_num'] = df.notnull().sum(axis=1)
    df.sort_values(by='info_num', inplace=True, ascending=False)
    df.drop('info_num', axis=1, inplace=True)
    return df.iloc[0]

def drop_duplicates(df):
    """
    使用集合去重。
    从第一个集合开始遍历，遇到存在交集的记录将其标记为重复
    下一轮遍历，跳过有标记的记录，直至结束
    按照标记分组，取信息量最大的一条记录
    :param df:
    :return:
    """
    if len(df) == 1:
        return df

    df['duplicate'] = None
    get_split_info = df[['phone', 'email']].applymap(get_split).values.tolist()  # 分割同一字段中的多个号码或邮箱地址
    info_set_list = [*map(lambda x: set(chain.from_iterable(x)), get_split_info)]  # 将多个号码整合为一个集合，每个号码为一个单独的元素
    # info_set_list = [*map(lambda x: set(x), df[['phone', 'email']].values.tolist())]
    for i in range(len(df)):
        if df.iloc[i].duplicate == None:
            for j in range(i+1, len(df)):
                if info_set_list[i] & info_set_list[j]:
                    df.duplicate.iloc[i] = i
                    df.duplicate.iloc[j] = i
                else:
                    df.duplicate.iloc[i] = i
        if i == len(df)-1:
            break

#         df.drop_duplicates('duplicate', inplace=True)  # 简单处理，保留第一条记录，不一定信息量最多
    df = df.groupby('duplicate', as_index=False, group_keys=False, dropna=False).apply(get_most_info)
    df.drop('duplicate', axis=1, inplace=True)

    return df

def drop_duplicate_collage(df):
    """
    按照姓名 groupby， 用 phone 和 email 构成的集合进行去重
    各记录集合若产生交集，则表明记录重复
    最后按照重复记录的缺失值情况，保留缺失值最小的一条记录
    :param df:
    :return:
    """
    df_temp = df.drop_duplicates()
    if len(df_temp) == df.name.nunique():
        return df_temp

    df_temp = df.groupby('name', as_index=False, group_keys=False, dropna=False).apply(drop_duplicates)
    return df_temp


def truncate_table(host, user, password: str, database, port, table_name):
    conn = pymysql.connect(host=host, user=user, password=password, database=database, port=port, charset='utf8')
    cursor = conn.cursor()
    sql = f'truncate table {table_name}'
    try:
        cursor.execute(sql)
        logger.info(f'truncate {table_name} successfully')
    except:
        logger.info('truncate {table_name} failed, rollback')
        conn.rollback()

def clean_phone(partition_num, dirty_phone):
    if not dirty_phone:
        return None

    phone = re.sub(r'—', '-', dirty_phone)
    phone = re.sub(r'\s', '', phone)
    phone = re.sub(r'\+?86-', '', phone)
    phone = re.sub(r'-(\d{4}$)', r'\1', phone)
    phone = re.sub(r'\d{2}-(\d+$)', '\1', phone)

    try:
        int(re.sub('-|^0', '', phone))
    except:
        return None

    if re.match(r'1\d{}10$|\d{3,4}-\d{7,8}$', phone):
        return phone
    elif len(phone) == 8:
        phone = partition_num + '-' + phone
        return phone
    else:
        return phone


def replace_quotes_in_text(node):
    if node.text and '"' in node.text:
        node.text = node.text.replace('"', '“').replace('"', '”')
    if node.tail and '"' in node.tail:
        node.tail = node.tail.replace('"', '“').replace('"', '”')
    for child in node:
        replace_quotes_in_text(child)
