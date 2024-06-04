# -*- coding: utf-8 -*-
# 数据提取完毕 入库失败时使用。或者
import csv
import os
from asyncio.log import logger
from utils import csv_2_df, truncate_table, df2mysql, drop_duplicate_collage, local_engine, sf_engine, save_as_json
from urllib import parse

school_id = 94
college_id = 146
school_name = '西安交通大学'
college_name = '化学学院'

url = ''

data_real = {
"姓名": "王淑娟",
"电话": "",
"邮箱": "shujuanwang@mail.xjtu.edu.cn",
"职称": "副教授",
"个人简介": "王淑娟，女，博士，副教授，博士生导师,应用化学系主任。主要从事功能和智能高分子的设计、合成及其应用研究，主持国家重点研发计划项目子课题1项、国家自然科学基金项目2项、军品配套项目2项、陕西省重点研发计划项目1项、陕西省自然科学基金1项、企业合作项目10余项、中央高校基本科研业务费1项。近年来以第一作者/通讯作者身份在Journal of the American Chemical Society、Journal of Materials Chemistry A、Composite Part A: Applied Science and Manufacturing和Applied Surface Science等国内外知名刊物上发表SCI收录论文30余篇，并多次受邀在国际、国内学术会议上报告相关研究进展。目前长期担任Composite Part A: Applied Science and Manufacturing、Applied Surface Science和Polymer Degradation and Stability等期刊特约审稿人。",
"研究方向": "1. 航天耐烧蚀复合材料基体树脂研究；\n2. 动态交联可再生高分子；\n3. 绿色可再生复合材料的制备和性能；\n4. 智能可穿戴材料；\n5. 3D打印材料。",
"专利": "",
"科研项目": "",
"荣誉/获奖": "",
"照片地址": "https://gr.xjtu.edu.cn/documents/2606997/0/4yy19-h…29f36-4877-3340-34ae-ba23ded117ca?t=1679989268911",
"最高学历": "研究生",
"最高学位": "博士",
"职位": "应用化学系主任",
"办公地点": "西安交通大学化学学院化学楼215室",
"科研论文": ""
}

data = {
    "姓名": data_real["姓名"],
    "学校": school_id,
    "学院": college_id,
    "电话": data_real["电话"],
    "邮箱": data_real["邮箱"],
    "职称": data_real["职称"],
    "个人简介": data_real["个人简介"],
    "研究方向": data_real["研究方向"],
    "教育经历": "",
    "工作经历": "",
    "专利": data_real["专利"],
    "科研项目": data_real["科研项目"],
    "荣誉/获奖": data_real["荣誉/获奖"],
    "科研论文": data_real["科研论文"],
    "社会兼职": "",
    "照片地址": parse.urljoin(url, data_real["照片地址"]),
    "最高学历": data_real["最高学历"],
    "最高学位": data_real["最高学位"],
    "在职信息": 1,
    "职位": data_real["职位"],
    "办公地点": data_real["办公地点"]
}

add = input('是否需要手动增加数据？是请输入1：')
if add == '1':
    file = open(f'./{school_id}{school_name}/{college_id}.csv', mode='a', encoding='utf-8', newline='')
    writter = csv.writer(file)
    writter.writerow(data.values())
    file.close()

result_df = csv_2_df(f'./{school_id}{school_name}/{college_id}.csv')
result_df = drop_duplicate_collage(result_df)
print(result_df)
ensure = input('确定保存吗？确定输入1：')
if ensure == '1':
    logger.info('再次保存中...')
    # if save2target == 'no':
    #     pass

    # elif self.save2target == 'test':
    # truncate_table(host='localhost', user='root', password='123456', database='alpha_search', port=3306, table_name='search_teacher_test')
    # df2mysql(engine=local_engine, df=result_df, table_name='search_teacher_test')

    # elif self.save2target == 'local':
    #     df2mysql(engine=local_engine, df=result_df, table_name='search_teacher')
    # elif self.save2target == 'target':
    df2mysql(engine=sf_engine, df=result_df, table_name='search_teacher')
    save_as_json(result_df, school_name, college_name, path=1)
