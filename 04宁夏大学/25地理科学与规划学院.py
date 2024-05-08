# json格式的字符串
import pandas as pd
import requests
import re
from fake_headers import Headers
from lxml import etree
import json
from urllib.parse import urljoin

from utils import result_dict_2_df, drop_duplicate_collage, sf_engine, df2mysql, save_as_json, local_engine

school_name = '宁夏大学'
college_name = '地理科学与规划学院'
school_id = 4
college_id = 25
url = 'https://geo.nxu.edu.cn/szdw/zzjzg.htm'
headers = {
        'Host': "geo.nxu.edu.cn",
        'Referer': "https://geo.nxu.edu.cn/szdw/rcjh.htm",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
}
phone_pattern = re.compile(r'(?<!\d)1\d{10}(?!\d)|(?<!\d)\d{4}-\d{7}(?!\d)', re.S)
result_df = pd.DataFrame()
result = {}


resp = requests.get(url, headers=headers)
resp.encoding = 'utf-8'
json_string = re.search(r'<ul id="showdatainfo">.*?<script>.*?var ret =\s*?(.*?)(?<=]);', resp.text, re.S).group(1)
# print(json_string)
teacher_info_list = json.loads(json_string)
# print(teacher_info_list)
for teacher_info in teacher_info_list:
    result['name'] = teacher_info['title']
    result['school_id'] = school_id
    result['college_id'] = college_id
    result['phone'] = re.search(phone_pattern, teacher_info['showAbstract']).group() if re.search(phone_pattern, teacher_info['showAbstract']) else None
    result['email'] = teacher_info['fields']['yx'] if teacher_info['fields']['yx'] else None
    result['job_title'] = None
    try:
        result['job_title'] = teacher_info['fields']['zc'] if teacher_info['fields']['zc'] else None
    except:
        pass
    result['abstracts'] = None
    result['directions'] = teacher_info['fields']['yjfx'] if teacher_info['fields']['yjfx'] else None
    result['education_experience'] = None
    result['work_experience'] = None
    result['patent'] = None
    result['project'] = None
    result['award'] = None
    result['social_job'] = None
    result['picture'] = urljoin(url, teacher_info['picUrl']['asString']) if teacher_info['picUrl']['asString'] else None
    result['education'] = None
    result['qualification'] = None
    result['job_information'] = 1
    result['responsibilities'] = None
    result['office_address'] = None
    # todo:其他信息可以通过teacher_info['url']['asString']获取详情页链接，然后解析详情页获得
    print(result)
    # break
    result_df = result_dict_2_df(result_df, result)
    # print(len(result_df))

result_df = drop_duplicate_collage(result_df)

# df2mysql(engine=local_engine, df=result_df, table_name='search_teacher_test')
df2mysql(engine=sf_engine, df=result_df, table_name='search_teacher_simple')
# 保存成json至本地
save_as_json(result_df, school_name, college_name)
