import re
import requests
import pandas as pd

from utils import result_dict_2_df, drop_duplicate_collage, df2mysql, sf_engine, save_as_json, local_engine

base_url = 'https://math.fudan.edu.cn/_wp3services/generalQuery?queryObj=articles'
img_url_head = 'https://math.fudan.edu.cn/'
school_name = '复旦大学'
college_name = '数学科学学院'
school_id = 105
college_id = 120
result_df = pd.DataFrame()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
    'Content-Length': '974',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'math.fudan.edu.cn'
}

for page in range(16):
    post_data = {
        'siteId': '629',
        'columnId': '30607',
        'pageIndex': str(page + 1),
        'rows': '8',
        'conditions': '[]',
        'orders': '[{"field":"letter","type":"asc"}]',
        'returnInfos': '[{"name":"id"},{"name":"title"},{"name":"mircImgPath"},{"name":"coverImgPath"},{"name":"publishTime"},{"name":"publisher"},{"name":"phColName"},{"name":"publishOrg"},{"name":"source"},{"name":"imgLogo"},{"name":"fileLogo"},{"field":"shortTitle","name":"shortTitle"},{"name":"f1"},{"name":"f2"},{"name":"f3"},{"name":"f4"},{"name":"f10"},{"name":"f11"},{"name":"f12"},{"field":"summary","pattern":[{"name":"lp","value":"150"}],"name":"summary"}]'
    }
    teacher_info_s = requests.post(base_url, data=post_data, headers=headers).json()['data']
    result = {}
    for teacher_info in teacher_info_s:
        result['name'] = teacher_info['title']
        result['school_id'] = school_id
        result['college_id'] = college_id

        link = teacher_info['url']
        resp = requests.get(link, headers=headers)
        resp.encoding = 'utf-8'
        page = resp.text

        result['phone'] = teacher_info['f11'] if teacher_info['f11'] != '' else None
        if result['phone'] and len(result['phone']) == 8:
            result['phone'] = '021-' + result['phone']

        result['email'] = teacher_info['f12'] if teacher_info['f12'] != '' else None
        result['email'] = re.sub(r'\(?\s?at\s?\)?|\(?\s?AT\s?\)?|\[?\s?at\s?]?|\[?\s?AT\s?]?', '@', result['email'])

        result['job_title'] = teacher_info['f2'] if re.sub(r'\s*', '', teacher_info['f2']) else None
        result['abstracts'] = None

        summary = teacher_info['summary']
        result['directions'] = re.search(r'研究方向：(.*?)主讲课程', summary, re.S).group(1) if re.search(r'研究方向：(.*?)主讲课程', summary, re.S) else None
        if not result['directions']:
            result['directions'] = None

        result['education_experience'] = None
        result['work_experience'] = None
        result['patent'] = None
        result['project'] = None
        result['award'] = None
        result['social_job'] = None
        result['picture'] = img_url_head + teacher_info['mircImgPath'] if teacher_info['mircImgPath'] else None
        result['education'] = None
        result['qualification'] = None
        result['job_information'] = 1
        result['responsibilities'] = teacher_info['phColName'] if teacher_info['phColName'] else None
        result['office_address'] = teacher_info['f10'] if teacher_info['f10'] else None

        try:
            if re.search(r'代表论著：</strong></p>(.*?)<strong.*?><span.*?>个人主页', page, re.S):
                result['paper'] = re.search(r'代表论著：</strong></p>(.*?)(?:<strong.*?>)?<span.*?>个人主页', page, re.S).group(1)
            elif re.search(r'代表论著：</strong></p>(.*?)<p><strong>个人主页', page, re.S):
                result['paper'] = re.search(r'代表论著：</strong></p>(.*?)<p><strong>个人主页', page, re.S).group(1)
            else:
                result['paper'] = None
        except:
            result['paper'] = None
        print(result)
        result_df = result_dict_2_df(result_df, result)

result_df = drop_duplicate_collage(result_df)

# df2mysql(engine=local_engine, df=result_df, table_name='search_teacher_test')
df2mysql(engine=sf_engine, df=result_df, table_name='search_teacher')
# 保存成json至本地
save_as_json(result_df, school_name, college_name)
