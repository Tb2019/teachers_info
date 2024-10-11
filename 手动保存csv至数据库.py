# -*- coding: utf-8 -*-
# 数据提取完毕 入库失败时使用。或者
import csv
import os
from asyncio.log import logger
from utils import csv_2_df, truncate_table, df2mysql, drop_duplicate_collage, local_engine, sf_engine, save_as_json
from urllib import parse

school_id = 93
college_id = 363
school_name = '南开大学'
college_name = '化学学院'

img_url_head = ''

data_real = {
"姓名": "于勐",
"电话": "",
"邮箱": "nkyu2023@nankai.edu.cn",
"职称": "副教授",
"个人简介": "于勐，博士，副教授，应用化学与工程研究所，毕业于南开大学，天津人。",
"教育经历": "2009年9月 − 2013年7月，上海交通大学电子信息与电气工程学院，本科\n2013年8月 − 2015年5月，美国南加州大学维特比工程学院，硕士\n2015年6月 − 2019年6月，南开大学电子信息与光学工程学院，博士",
"工作经历": "2019年7月 – 2022年6月，南开大学化学学院，博士后\n2022年7月 – 2023年9月，南开大学电子信息与光学工程学院，博士后\n2023年10月至今，南开大学化学学院，副教授",
"研究方向": "能源材料化学，电催化材料与器件",
"人才称号": "",
"行政称号": "",
"专利": "获发明专利授权专利1项",
"科研项目": "作为项目负责人或骨干成员承担国家自然科学基金青年项目、国家重点研发计划“催化科学”专项等科研任务。",
"荣誉/获奖": "2022年天津市自然科学二等奖（第二完成人）\n第二十次全国电化学大会优秀论文奖\nJournal of Energy Chemistry2022年作者交流会最佳报告奖",
"照片地址": "https://chem.nankai.edu.cn/_upload/article/images/df/0f/38a6228f424cb1595751e78a505d/3263b494-6b8c-452d-9e90-c1fb364996f5.jpg",
"最高学历": "研究生",
"最高学位": "博士",
"职位": "副教授",
"办公地点": "天津市南开区卫津路94号南开大学联合楼A703室",
"科研论文": "1. Jinhan Li, Keqiang Xu, Fangming Liu, Youzeng Li, Yanfang Hu, Xijie Chen, Huan Wang*, Wence Xu, Youxuan Ni, Guoyu Ding, Tete Zhao, Meng Yu*, Wei Xie, Fangyi Cheng*. Hollow Hierarchical Cu2O-Derived Electrocatalysts Steering CO2 Reduction to Multi-Carbon Chemicals at Low Overpotentials. Advanced Materials 2023, 35, 2301127.\n2. Tete Zhao, Jinhan Li, Jiuding Liu, Fangming Liu, Keqiang Xu, Meng Yu*, Wence Xu, Fangyi Cheng*. Tailoring the Catalytic Microenvironment of Cu2O with SiO2 to Enhance C2+ Product Selectivity in CO2 Electroreduction. ACS Catalysis 2023, 13, 4444.\n3. Tete Zhao, Xupeng Zong, Jiuding Liu, Jialei Chen, Keqiang Xu, Xiao Wang, Xijie Chen, Wutong Yang, Fangming Liu, Meng Yu*, Fangyi Cheng*. Functionalizing Cu nanoparticles with fluoric polymer to enhance C2+ roduct selectivity in membraned CO2 reduction. Applied Catalysis B: Environmental 2024, 340, 123281.\n4. Meng Yu#, Fangming Liu#, Jinhan Li, Jiuding Liu, Yudong Zhang, Fangyi Cheng*. Multidimensional nonstoichiometric electrode materials for electrochemical energy conversion and storage. Advanced Energy Materials 2021, 2100640.\n5. Meng Yu, Jinhan Li, Fangming Liu, Jiuding Liu, Wence Xu, Honglu Hu, Xijie Chen, Weichao Wang, Fangyi Cheng*. Anionic formulation of electrolyte additive towards stable lectrocatalytic oxygen evolution in seawater splitting. Journal of Energy Chemistry 2022, 72, 361.",
"源地址": "https://chem.nankai.edu.cn/2019/0906/c24393a540862/page.htm"
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
    "教育经历": data_real["教育经历"],
    "工作经历": data_real["工作经历"],
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
