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

url = 'https://gr.xjtu.edu.cn/c/'

data_real = {
"姓名": "王卫林",
"电话": "",
"邮箱": "weilinwang@xjtu.edu.cn",
"职称": "副教授",
"个人简介": "王卫林，副教授，硕士生导师。2019年获得南开大学有机化学理学博士学位，2020年11月进入化学学院任助理教授，从事科研工作。",
"研究方向": "碳碳不饱和键的官能团化转化以及药物、天然产物全合成等相关研究。",
"专利": "",
"科研项目": "",
"荣誉/获奖": "",
"照片地址": "/documents/9410113/0/%E5%9B%BE%E7%89%871.jpg/9e3cc580-4c48-836b-c88c-3b34b67ce72c?t=1618888233863",
"最高学历": "研究生",
"最高学位": "博士",
"职位": "助理教授,副教授",
"办公地点": "陕西省西安市长安区沣西新城中国西部科技创新港19号楼4166室",
"科研论文": "Angew. Chem. Int. Ed.\nCommun. Chem.\nOrg.lett., Chem. Eur. J.(Hot Paper), Org. Chem. Front., J. Org. Chem., Adv. Synth. Catal."
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
    # df2mysql(engine=sf_engine, df=result_df, table_name='search_teacher')
    save_as_json(result_df, school_name, college_name, path=1)
