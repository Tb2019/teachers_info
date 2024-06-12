import os
import json
import re
import time
import pymysql
import requests
import pandas as pd
import numpy as np
from loguru import logger
from itertools import chain
from asyncio import Semaphore
from fake_headers import Headers
from urllib.parse import quote_plus
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine


proxy = {
    'http': '127.0.0.1:7890',
    'https': '127.0.0.1:7890',
}

selector = {
    # 清除记录
    'com-clear-css': '#root > div:nth-child(2) > div > div > div > div > div.aSIvzUFX9dAs4AK6bTj0 > div.sidesheet-container.UMf9npeM8cVkDi0CDqZ0 > div.TH9DlQU1qwg_KGXdDYzk > div > div.nIP4BqLGD8csFme4CavI > div.WfXRc6x8M2gbaaX2HSxJ > div > div.k7y7pgLJN2EYTHcUikQA > div.AXzy5aeT38Mdxk6pvvuE > div.NyvVfPwFXFYvQFyXUtTl > button',

    'cn-clear-xpath': '//div[@class="left-actions-container--NyvVfPwFXFYvQFyXUtTl"]',

    # 文本框
    'com-textarea-xpath': '//textarea[@class="rc-textarea oTXB57QK8bQN2BKYJ2Bi oTXB57QK8bQN2BKYJ2Bi"]',
    'com-textarea-css': '#root > div:nth-child(2) > div > div > div > div > div.aSIvzUFX9dAs4AK6bTj0 > div.sidesheet-container.UMf9npeM8cVkDi0CDqZ0 > div.TH9DlQU1qwg_KGXdDYzk > div > div.nIP4BqLGD8csFme4CavI > div.WfXRc6x8M2gbaaX2HSxJ > div > div.k7y7pgLJN2EYTHcUikQA > div.AXzy5aeT38Mdxk6pvvuE > div.k5ePpJvczIMzaNIaOwKS > div > textarea',

    'cn-textarea-xpath': '//textarea[@class="rc-textarea textarea--oTXB57QK8bQN2BKYJ2Bi textarea--oTXB57QK8bQN2BKYJ2Bi"]',

    # 发送
    'com-sendtext-css': '#root > div:nth-child(2) > div > div > div > div > div.aSIvzUFX9dAs4AK6bTj0 > div.sidesheet-container.UMf9npeM8cVkDi0CDqZ0 > div.TH9DlQU1qwg_KGXdDYzk > div > div.nIP4BqLGD8csFme4CavI > div.WfXRc6x8M2gbaaX2HSxJ > div > div.k7y7pgLJN2EYTHcUikQA > div.AXzy5aeT38Mdxk6pvvuE > div.k5ePpJvczIMzaNIaOwKS > div > div > div.vr4WgM3FUuUicP3kJDOU > button',
    'com-sendtext-xpath': '//button[@class="semi-button semi-button-primary semi-button-size-small semi-button-borderless tqxhKsM_tI4KvPKo9dkI semi-button-with-icon semi-button-with-icon-only" and @aria-disabled="false"]',

    'cn-sendtext-xpath': '//div[@class="textarea-actions-right--vr4WgM3FUuUicP3kJDOU"]',
    # tokens
    'com-tokens-css': '#root > div:nth-child(2) > div > div > div > div > div.aSIvzUFX9dAs4AK6bTj0 > div.sidesheet-container.UMf9npeM8cVkDi0CDqZ0 > div.TH9DlQU1qwg_KGXdDYzk > div > div.R_WS6aCLs2gN7PUhpDB0.JlYYJX7uOFwGV6INj0ng > div > div > div.nIVxVV6ZU7gCM5i4VQIL.message-group-wrapper > div > div > div:nth-child(1) > div > div > div > div > div.chat-uikit-message-box-container__message > div > div.chat-uikit-message-box-container__message__message-box__footer > div > div.tTSrEd1mQwEgF4_szmBb > div:nth-child(3) > div > div',

    'cn-tokens-css': '#root > div:nth-child(2) > div > div > div > div > div.container--aSIvzUFX9dAs4AK6bTj0 > div.sidesheet-container.wrapper-single--UMf9npeM8cVkDi0CDqZ0 > div.message-area--TH9DlQU1qwg_KGXdDYzk > div > div.scroll-view--R_WS6aCLs2gN7PUhpDB0.scroll-view--JlYYJX7uOFwGV6INj0ng > div > div > div.wrapper--nIVxVV6ZU7gCM5i4VQIL.message-group-wrapper > div > div > div:nth-child(1) > div > div > div > div > div.chat-uikit-message-box-container__message > div > div.chat-uikit-message-box-container__message__message-box__footer > div > div.message-info-text--tTSrEd1mQwEgF4_szmBb > div:nth-child(3) > div > div',
    # 内容
    'com-content-gemini-xpath': '//pre[@class="language-json light-scrollbar_97dc0"]',
    'com-content-gpt-xpath': '//div[@class="auto-hide-last-sibling-br paragraph_1252f paragraph-element"]',

    'cn-content-xpath': '//div[@class="auto-hide-last-sibling-br paragraph_4183d"]',
    # 重新生成
    'com-regenerate-css': '#root > div:nth-child(2) > div > div > div > div > div.aSIvzUFX9dAs4AK6bTj0 > div.sidesheet-container.UMf9npeM8cVkDi0CDqZ0 > div.TH9DlQU1qwg_KGXdDYzk > div > div.R_WS6aCLs2gN7PUhpDB0.JlYYJX7uOFwGV6INj0ng > div > div > div.nIVxVV6ZU7gCM5i4VQIL.message-group-wrapper > div > div > div:nth-child(1) > div > div > div > div > div.chat-uikit-message-box-container__message > div > div.chat-uikit-message-box-container__message__message-box__footer > div > div.semi-space.semi-space-align-center.semi-space-horizontal > div:nth-child(2) > button',

    'cn-regenerate-css': '#root > div:nth-child(2) > div > div > div > div > div.container--aSIvzUFX9dAs4AK6bTj0 > div.sidesheet-container.wrapper-single--UMf9npeM8cVkDi0CDqZ0 > div.message-area--TH9DlQU1qwg_KGXdDYzk > div > div.scroll-view--R_WS6aCLs2gN7PUhpDB0.scroll-view--JlYYJX7uOFwGV6INj0ng > div > div > div.wrapper--nIVxVV6ZU7gCM5i4VQIL.message-group-wrapper > div > div > div:nth-child(1) > div > div > div > div > div.chat-uikit-message-box-container__message > div > div.chat-uikit-message-box-container__message__message-box__footer > div > div.semi-space.semi-space-align-center.semi-space-horizontal > div:nth-child(2)',

    # 切换模型
    'com-change-css': '#root > div:nth-child(2) > div > div > div > div > div.aSIvzUFX9dAs4AK6bTj0 > div.sidesheet-container.UMf9npeM8cVkDi0CDqZ0 > div.IoQhh3vVUhwDTJi9EIDK > div.LxUy6g0wgIgIWCGkQHkC.coz-bg-plus.coz-fg-secondary.Zo84sv5CjcC2ObBGEGDy.SKIazToEhtUg8ZweE2b6 > div.IJW2oexGFSA7_n0W_IUb > div > div.PLf9q929mqs4ZlidOgkc > button',

    # 下拉列表
    'com-model-list-xpath': '//div[@class="qNKhq1IFxcAMuhECsZz9"]',

    # 选择模型
    'com-gemini-1.5-flash-xpath': '//div[contains(@id, "-option-0")]',
    'com-gemini-1.5-pro-xpath': '//div[contains(@id, "-option-1")]',
    'com-gpt-4o-xpath': '//div[contains(@id, "-option-2")]',
    'com-gpt-4-turbo-xpath': '//div[contains(@id, "-option-3")]',

    # 模型输出文本长度
    'com-text-length-xpath': '//input[@class="semi-input semi-input-default" and @aria-valuemin="1"]',
    'com-text-length-ensure-1-xpath': '//input[@class="semi-input semi-input-default" and @aria-valuemin="1" and @aria-valuenow="8192"]',
    'com-text-length-ensure-2-xpath': '//input[@class="semi-input semi-input-default" and @aria-valuemin="1" and @aria-valuenow="4096"]'
}

headers = Headers(headers=True).generate()
api_headers = {
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

csv_header = ['name', 'school_id', 'college_id', 'phone', 'email', 'job_title', 'abstracts', 'directions', 'education_experience', 'work_experience', 'patent', 'project', 'award', 'paper', 'social_job', 'picture', 'education', 'qualification', 'job_information', 'responsibilities', 'office_address']


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


def save_as_json(df, school_name, college_name, path=None):
    if not path:
        path = f'../Results/{school_name}'
    # 手动保存csv时，路径要变化
    else:
        path = f'./Results/{school_name}'
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


def clean_phone(partition_num: str, dirty_phone: str):
    if not dirty_phone:
        return None

    # 格式化
    phone = re.sub(r'—', '-', dirty_phone)
    phone = re.sub(r'\((.*?)\)', r'\1', phone)
    phone = re.sub(r'^\+?(?:（|\()?86(?:）|\))?-?', '', phone)
    phone = re.sub(r'\s', '', phone)

    try:
        int(re.sub('-|^0|,', '', phone))
    except:
        return None

    if ',' not in phone:
        if len(phone) > 13 and re.search(r'-\d{3,4}$', phone):
            phone = re.sub(r'-\d{3,4}$', '', phone)
        phone = re.sub('-', '', phone)

        if re.match('^' + partition_num, phone):
            phone = re.sub('^' + partition_num, partition_num + '-', phone)
        elif re.match('^' + partition_num[1:], phone):
            phone = re.sub('^' + partition_num[1:], partition_num + '-', phone)
        elif len(phone) == 7 or len(phone) == 8:
            phone = partition_num + '-' + phone
        else:
            pass
        # elif len(phone) == 11 and phone.startswith('1'):
        #     pass
        # else:
        #     phone = None
        return phone
    else:
        res_phone = ''
        for num in phone.split(','):
            if len(num) > 13 and re.search(r'-\d{3,4}$', num):
                num = re.sub(r'-\d{3,4}$', '', num)
            num = re.sub('-', '', num)

            if re.match('^' + partition_num, num):
                num = re.sub('^' + partition_num, partition_num + '-', num)
            elif re.match('^' + partition_num[1:], num):
                num = re.sub('^' + partition_num[1:], partition_num + '-', num)
            elif len(phone) == 7 or len(phone) == 8:
                phone = partition_num + '-' + phone
            else:
                pass
            if not res_phone:  # 防止开头多一个逗号
                res_phone += num
            else:
                res_phone = res_phone + ',' + num
        return res_phone


    # phone = re.sub(r'\d{2}-(\d+$)', '\1', phone)
    # phone = re.sub(r'(?<=\d{3})-(\d{4}$)', r'\1', phone)
    # phone = re.sub(r'(?<=\d{4})-(\d{4}$)', r'\1', phone)
    # try:
    #     int(re.sub('-|^0|,', '', phone))
    # except:
    #     return None
    #
    # if re.match(r'1\d{10}$|\d{3,4}-\d{7,8}$', phone):
    #     return phone
    # elif len(phone) == 8 or len(phone) == 7:
    #     phone = partition_num + '-' + phone
    #     return phone
    # else:
    #     return phone


def replace_quotes_in_text(node):
    if node.text and '"' in node.text:
        node.text = node.text.replace('"', '“').replace('"', '”')
    if node.tail and '"' in node.tail:
        node.tail = node.tail.replace('"', '“').replace('"', '”')
    for child in node:
        replace_quotes_in_text(child)

def csv_2_df(path):
    df = pd.read_csv(path, encoding='utf-8').replace(np.nan, None)  # 不replace，则转换为json时空值为NaN，转换后为null
    return df


def change_model(count, driver):
    driver.find_element(By.CSS_SELECTOR, selector.get('com-change-css')).click()
    time.sleep(0.5)
    driver.find_element(By.XPATH, selector.get('com-model-list-xpath')).click()
    time.sleep(0.5)
    action = ActionChains(driver)
    if count == 1:
        driver.find_element(By.XPATH, selector.get('com-gemini-1.5-pro-xpath')).click()
        time.sleep(0.5)
        length_element = driver.find_element(By.XPATH, selector.get('com-text-length-xpath'))
        # 确认修改最大输出长度成功
        while True:
            try:
                length_element.click()
                length_element.send_keys(Keys.CONTROL, 'a')
                length_element.send_keys(Keys.DELETE)
                length_element.send_keys('8192')
                time.sleep(1)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, selector.get('com-text-length-ensure-1-xpath'))))
                break
            except:
                continue
        action.send_keys(Keys.ESCAPE).perform()
        time.sleep(0.5)
        logger.info('第二次重新生成，使用Gemini-pro')
    if count == 2:
        driver.find_element(By.XPATH, selector.get('com-gpt-4o-xpath')).click()
        time.sleep(0.5)
        logger.info('第三次重新生成，使用gpt-4o')
    if count == 3:
        driver.find_element(By.XPATH, selector.get('com-gpt-4-turbo-xpath')).click()
        time.sleep(0.5)
        logger.info('第四次重新生成，使用gpt-4-turbo')

def restore_model(driver):
    driver.find_element(By.CSS_SELECTOR, selector.get('com-change-css')).click()
    time.sleep(0.5)
    driver.find_element(By.XPATH, selector.get('com-model-list-xpath')).click()
    time.sleep(0.5)
    action = ActionChains(driver)

    driver.find_element(By.XPATH, selector.get('com-gemini-1.5-flash-xpath')).click()
    time.sleep(0.5)
    length_element = driver.find_element(By.XPATH, selector.get('com-text-length-xpath'))
    # 确认修改最大输出长度成功
    while True:
        try:
            length_element.click()
            length_element.send_keys(Keys.CONTROL, 'a')
            length_element.send_keys(Keys.DELETE)
            length_element.send_keys('8192')
            time.sleep(1)
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, selector.get('com-text-length-ensure-1-xpath'))))
            break
        except:
            continue
    action.send_keys(Keys.ESCAPE).perform()
    time.sleep(0.5)
    logger.info('模型已切换回gemini-flash')
