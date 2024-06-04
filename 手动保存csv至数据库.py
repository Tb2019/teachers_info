# -*- coding: utf-8 -*-
# 数据提取完毕 入库失败时使用。或者
import csv
import os
from asyncio.log import logger
from utils import csv_2_df, truncate_table, df2mysql, drop_duplicate_collage, local_engine, sf_engine, save_as_json
from urllib import parse

school_id = 93
college_id = 147
school_name = '南开大学'
college_name = '化学学院'

img_url_head = ''

data_real = {
"姓名":"王浩",
"电话":"16622807600",
"邮箱":"hao@nankai.edu.cn",
"职称":"特聘副研究员",
"个人简介":"王浩，博士，副研究员，元素有机化学研究所，毕业于南开大学，山东诸城人。",
"研究方向":"有机合成化学与理论计算化学",
"专利":"申请中国发明专利 4 项，其中3项已授权",
"科研项目":"王浩博士先后主持国家自然科学基金委青年项目 (2019), 中国博士后科学基金面上一等项目 (2018) 和特别资助项目 (2019) 和南开大学百名青年学科带头人培养项目 (2023), 骨干参与国家基金委重大项目-集成项目 (2023) 等科研项目",
"荣誉/获奖":"曾获首届全国博士后创新创业大赛优胜奖 (2021)、南开大学优秀博士学位论文 (2019)、研究生国家奖学金 (2014, 2017) 等奖励。",
"照片地址":"https://chem.nankai.edu.cn/_upload/article/images/…ac1265be/033e1447-2e1a-498a-a66e-6d5a57e4d950.png",
"最高学历":"研究生",
"最高学位":"博士",
"职位":"博士生导师",
"办公地点":"天津市南开区卫津路94号南开大学天南楼D703室",
"科研论文":"1. Wang, H., Jung, H., Song, F., Zhu, S., Bai, Z., Chen, D., He, G., Chang, S.,* Chen, G.* Nitrene-Mediated Intermolecular N–N Coupling for Efficient Synthesis of Hydrazides. Nat. Chem. 2021, 13, 378-385.\n2. Bai, Z., Zhu, S., Hu, Y., Yang, P., Chu, X., He, G., Wang, H.,* Chen, G.* Copper-catalyzed Amidation of Thiols with Dioxazolones: New Sulfenamide Reagents for Synthesis of Unsymmetrical Disulfides Nat. Commun. 2022, 13, 6645.\n3. Jia, S., Huang, Y., Wang, Z., Fan, F., Fan, B., Sun, H., Wang, H.,* Wang, F.* Hydroamination of Unactivated Alkenes with Aliphatic Azides J. Am. Soc. Chem. 2022, 144, 16316-16324.\n4. Bai, Z., Song, F., Wang, H.,* Cheng, W., Zhu, S., Huang, Y., He, G., Chen, G.* Nitrene-mediated P–N Coupling Under Iron Catalysis. CCS Chem. 2022, 4, 2258–2266. \n5. Chen, X.#, Wang, H.# (co-first author), Du, S., Driess, M., Mo, Z* Deoxygenation of Nitrous Oxide and Nitro Compounds Using Bis(N-Heterocyclic Silylene)Amido Iron Complexes as Catalysts. Angew. Chem., Int. Ed. 2022, 61, e202114598."
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
    "照片地址": parse.urljoin(img_url_head, data_real["照片地址"]),
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
