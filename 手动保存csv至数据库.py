# -*- coding: utf-8 -*-
# 数据提取完毕 入库失败时使用。或者
import csv
import os
from asyncio.log import logger
from utils import csv_2_df, truncate_table, df2mysql, drop_duplicate_collage, local_engine, sf_engine, save_as_json
from urllib import parse

school_id = 110
college_id = 3
school_name = '哈尔滨工业大学'
college_name = '材料科学与工程学院'

img_url_head = ''

data_real = {
"姓名": "赵连城",
"电话": "",
"邮箱": "",
"职称": "中国工程院院士",
"个人简介": "赵连城是中国著名的光电信息科学与工程专家，为推进光电信息科学与工程应用作出了突出贡献，赵连城心系国家发展，积极为中国功能材料产业的发展建言献策，赵连城十分关心中国工程院的工作，积极参加中国工程院的各项活动，为中国工程院的发展作出了重要贡献，赵连城热爱祖国、追求真理、尊重科学、勇于创新、严谨治学、为人师表、敬业奉献，是中国工程科技界的楷模和学习的榜样。（中国工程院原院长周济评）",
"研究方向": "分子学\n材料科学\n信息科学\n光电薄膜\n分子荧光",
"人才称号": "",
"行政称号": "",
"专利": "",
"科研项目": "",
"荣誉/获奖": "",
"照片地址": "https://ysg.ckcest.cn/ysgOld/uploadfile/acInfoHome/7d80ebff-e120-4ebb-b455-d62cbe6c6d9b.png",
"最高学历": "本科",
"最高学位": "学士",
"职位": "",
"办公地点": "",
"科研论文": "",
"源地址": "https://ysg.ckcest.cn/html/details/274/index.html"
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
    "人才称号": data_real["人才称号"],
    "行政称号": data_real["行政称号"],
    "教育经历": "",
    "工作经历": "",
    "专利": data_real["专利"],
    "科研项目": data_real["科研项目"],
    "荣誉/获奖": data_real["荣誉/获奖"],
    "科研论文": data_real["科研论文"],
    "社会兼职": "",
    "照片地址": parse.urljoin(img_url_head, data_real["照片地址"]),
    "最高学历": data_real["最高学历"],
    "最高学位": data_real["最高学位"],
    "在职信息": 1,
    "职位": data_real["职位"],
    "办公地点": data_real["办公地点"],
    "源地址": data_real["源地址"]
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
