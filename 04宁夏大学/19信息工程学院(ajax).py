"""
ajax
"""
import requests
import pandas as pd
from fake_headers import Headers
from utils import result_dict_2_df, drop_duplicate_collage, df2mysql, local_engine, sf_engine, save_as_json

headers = Headers(headers=True).generate()
base_url = 'https://xxgc.nxu.edu.cn/system/resource/tsites/portal/queryteacher.jsp?collegeid=1186&isshowpage=false&postdutyid=0&postdutyname=&facultyid=&disciplineid=0&rankcode=0&jobtypecode=&enrollid=0&pageindex={page_index}&pagesize=10&login=true&profilelen=10&honorid=0&pinyin=&teacherName=&searchDirection=&viewmode=10&viewOwner=1804930476&viewid=1049495&siteOwner=1804930476&viewUniqueId=u12&showlang=zh_CN&actiontype='
school_name = '宁夏大学'
college_name = '信息工程学院'
school_id = 4
college_id = 19
result_df = pd.DataFrame()

for i in range(7):
    url = base_url.format(page_index=i+1)
    resp = requests.get(url, headers=headers).json()
    teachers_info = resp['teacherData']
    result = {}
    for teacher_info in teachers_info:
        result['name'] = teacher_info['name']
        result['school_id'] = school_id
        result['college_id'] = college_id
        result['phone'] = None
        result['email'] = teacher_info['email']
        result['job_title'] = teacher_info['prorank'] if teacher_info['prorank'] != '' else None
        result['abstracts'] = None
        result['directions'] = teacher_info['yjfx'] if teacher_info['yjfx'] != '' else None
        result['education_experience'] = None
        result['work_experience'] = teacher_info['workexperience'] if teacher_info['workexperience'] != '' else None
        result['patent'] = None
        result['project'] = None
        result['award'] = teacher_info['honor'] if teacher_info['honor'] != '' else None
        result['social_job'] = None
        result['picture'] = teacher_info['picUrl'] if teacher_info['picUrl'] != '' else None
        result['education'] = None
        result['qualification'] = None
        result['job_information'] = 1
        result['responsibilities'] = None
        result['office_address'] = teacher_info['officeLocation'] if teacher_info['officeLocation'] != '' else None
        print(result)
        result_df = result_dict_2_df(result_df, result)

result_df = drop_duplicate_collage(result_df)

# df2mysql(engine=local_engine, df=result_df, table_name='search_teacher_test')
df2mysql(engine=sf_engine, df=result_df, table_name='search_teacher_simple')
# 保存成json至本地
save_as_json(result_df, school_name, college_name)

