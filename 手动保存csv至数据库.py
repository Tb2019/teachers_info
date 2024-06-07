# -*- coding: utf-8 -*-
# 数据提取完毕 入库失败时使用。或者
import csv
import os
from asyncio.log import logger
from utils import csv_2_df, truncate_table, df2mysql, drop_duplicate_collage, local_engine, sf_engine, save_as_json
from urllib import parse

school_id = 91
college_id = 149
school_name = '华东师范大学'
college_name = '物理与电子科学学院'

img_url_head = 'https://faculty.ecnu.edu.cn/'

data_real = {
"姓名":"田博博",
"电话":"",
"邮箱":"bbtian@ee.ecnu.edu.cn",
"职称":"教授",
"个人简介":"田博博，物理与电子科学学院电子科学系教授，博士生导师。2016年获法国Paris-Saclay大学和中国科学院大学双博士学位（Ph.D.）。主讲本科专业基础课《半导体物理》、《人工智能导论》和《理论力学》，教学获第五届上海高校青年教师教学比赛优秀奖，第十三届华东师范大学青年教师教学比赛一等奖。指导教育部A类科创比赛获得国家级一等奖3项，二等奖1项，省部级一等奖1项，二等奖2项。\n研究方向为基于铁电材料的类脑智能器件。主持含国家自然基金（3项）和上海市项目（3项）在内的科研项目10余项，在Nat. Mater.、Nat. Electron.、Appl. Phys. Rev.、Nat. Commun.等国际重要期刊发表SCI论文100余篇。入选国家优青，中国博士后创新人才计划和中国科学院院长特别奖。担任中国神经科学学会类脑智能分会委员会委员，以及InfoMat (IF:22.7)、NML (IF:26.6)、IJEM (IF:14.7)、Exploration和Brain-X期刊的青年编委。",
"研究方向":"依托上海类脑智能材料与器件研究中心和极化材料与器件教育部重点实验室，重点利用铁电信息材料开展类脑智能器件、存储、存算一体、感存算一体计算的研究，相关成果发表于Nat. Mater.、Nat. Electron.、Appl. Phys. Rev.、Nat. Commun.、InfoMat、Adv. Funct. Mater.、Adv. sci.等国际重要期刊。欢迎研究生和青年人才加入科研团队。",
"专利":"",
"科研项目":"主持含国家自然科学基金（3项）、省部级项目（5项）在内的科研项目10余项。入选国家级青年、省部级杰青和中国博士后创新等人才计划。",
"荣誉/获奖":"教学：\n获得第五届上海高校青年教师教学比赛优秀奖，第十三届华东师范大学青年教师教学比赛一等奖，指导教育部A类科创比赛获得国家级一等奖3项，二等奖1项，省部级一等奖1项，二等奖2项。\n科研：\n中国科学院院长特别奖，中科院优博百篇，中国电子教育学会优博，中国博士后创新人才，上海市扬帆人才，上海市晨光人才，国家级青年人才，省部级杰青......",
"照片地址":"https://faculty.ecnu.edu.cn/_upload/article/images/3a/5b/afaa6191485eb4ee90f4bba8ab4b/4dbd2be0-83de-4336-a08a-5d9be5a5fd4f_s.png",
"最高学历":"研究生",
"最高学位":"博士",
"职位":"教授",
"办公地点":"上海市东川路500号 华东师范大学信息楼",
"科研论文":"1. Guangdi Feng#, Qiuxiang Zhu#, Xuefeng Liu, Luqiu Chen, Xiaoming Zhao, Jianquan Liu, Shaobing Xiong, Kexiang Shan, Zhenzhong Yang, Qinye Bao, Fangyu Yue, Hui Peng, Rong Huang, Xiaodong Tang, Jie Jiang, Wei Tang, Xiaojun Guo, Jianlu Wang, Anquan Jiang, Brahim Dkhil, Bobo Tian*, Junhao Chu and Chungang Duan. A ferroelectric fin diode for robust non-volatile memory, Nature Communications, 15, 513 (2024). https://doi.org/10.1038/s41467-024-44759-5 \n2.  Guangjian Wu#, Xumeng Zhang#, Guangdi Feng#, Jingli Wang, Keji Zhou,  Jinhua Zeng, Danian Dong, Fangduo Zhu, Chenkai Yang, Xiaoming Zhao,  Danni Gong, Mengru Zhang, Bobo Tian*, Chungang Duan, Qi  Liu*, Jianlu Wang*, Junhao Chu and Ming Liu. Ferroelectric-defined  reconfigurable homojunctions for in-memory sensing and computing, Nature Materials, 22, 1499 (2023). https://www.nature.com/articles/s41563-023-01676-0\n3. Jie Lao#, Mengge Yan#, Bobo Tian*, Chunli  Jiang, Chunhua Luo, Zhuozhuang Xie, Qiuxiang Zhu, Zhiqiang Bao, Ni  Zhong, Xiaodong Tang, Linfeng Sun, Guangjian Wu, Jianlu Wang, Hui Peng*,  Junhao Chu, and Chungang Duan*. Ultralow-Power Machine Vision with  Self-Powered Sensor Reservoir, Advanced Science, 9 (15), 2106092 (2022). (高被引) https://onlinelibrary.wiley.com/doi/full/10.1002/advs.202106092\n4. Guangjian Wu#, Bobo Tian#, Lan Liu#, Wei Lv, Shuang Wu, Xudong Wang, Yan Chen, Jingyu Li, Zhen Wang, Shuaiqin Wu,Hong Shen, Tie Lin, Peng Zhou*, Qi Liu, Chungang Duan, Shantao Zhang, Xiangjian Meng, Shiwei Wu, Weida Hu, Xinran Wang, Junhao Chu and Jianlu Wang*. Programmable transition metal dichalcogenide homojunctions controlled by nonvolatile ferroelectric domains, Nature Electronics, 3, 43 (2020) (高被引)  https://www.nature.com/articles/s41928-019-0350-y\n5. Bobo Tian, Jianlu Wang*, Stephane Fusil, Yang Liu, Xiaolin Zhao, Shuo Sun, Hong Shen, Tie Lin, Jinglan Sun, Chungang Duan*, Manuel Bibes, Agnes Barthélémy, Brahim Dkhil, Vincent Garcia*, Xiangjian Meng and Junhao Chu. Tunnel electroresistance through organic ferroelectrics. Nature Communications 7, 11502 (2016) https://www.nature.com/articles/ncomms11502"
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
