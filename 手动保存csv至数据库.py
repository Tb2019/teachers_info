# -*- coding: utf-8 -*-
# 数据提取完毕 入库失败时使用。或者
import csv
import os
from asyncio.log import logger
from utils import csv_2_df, truncate_table, df2mysql, drop_duplicate_collage, local_engine, sf_engine, save_as_json
from urllib import parse

school_id = 81
college_id = 649
school_name = '吉林大学'
college_name = '通信工程学院'

img_url_head = ''

data_real = {
"姓名": "李晓妮",
"电话": "",
"邮箱": "lxn@jlu.edu.cn",
"职称": "副教授",
"个人简介": "",
"教育经历": "2003.09-2007.07 哈尔滨工业大学 电子信息专业 学士\n2007.09-2009.07 吉林大学 通信与信息系统专业 硕士\n2009.09-2012.06 吉林大学 通信与信息系统专业 博士",
"工作经历": "2011.03-2012.03 坦佩雷工业大学 信号处理系 访问学者\n2012.11-2016.11 吉林大学 交通学院 博士后\n2013.12-2014.12 坦佩雷工业大学 信号处理系 博士后\n2012.07-至今 吉林大学 教师",
"研究方向": "视频与图像处理\n计算机视觉\n机器学习",
"人才称号": "",
"行政称号": "",
"专利": "",
"科研项目": "1.吉林省科技厅高新处，智能化外墙喷涂系统关键技术研究，2021.07-2024.06，项目负责人\n2.吉林省科技厅国际科技合作处，基于机器学习的下一代可伸缩视频编码技术研究，2020.01-2022.12，项目负责人\n3.吉林省教育厅，SHVC编码快速算法关键技术研究，2016.01-2018.12，项目负责人\n4.吉林省科技厅国际科技合作处，车联网环境下行人检测技术研究，2014.01-2016.12，项目负责人\n5.吉林省科技厅计划处，基于人眼视觉特性的H.264/AVC视频编码快速算法研究，2013.01-2015.12，项目负责人\n6.横向项目，管道漏磁内检测信号显示分析系统开发，2021.05-2023.09，项目负责人\n7.横向项目，基于机器视觉的复杂工件自动喷涂系统开发，2020.12-2022.12，项目负责人",
"荣誉/获奖": "",
"照片地址": "https://dce.jlu.edu.cn/__local/0/85/CA/4F833402CA1FB8AF915AC40D19C_1498066D_A154.png",
"最高学历": "研究生",
"最高学位": "博士",
"职位": "教师",
"办公地点": "",
"科研论文": "1. Xiaoni Li, Mianshu Chen, Zhaowei Qu, Jimin Xiao and Moncef Gabbouj. An effective CU size decision method for quality scalability in SHVC. Multimedia tools and applications. 2017,76:8011-8030.\n2. 李晓妮，陈绵书，桑爱军，曲昭伟. 质量可伸缩高性能视频编码中增强层快速算法. 吉林大学学报（工学版），2017 , 47(2):670-676.\n3. 李晓妮，陈贺新，陈绵书，蒙塞夫•嘎博基. 基于H.264运动估计的音视频同步编码技术研究. 吉林大学学报（工学版）2012, 42(5): 1321-1326.\n4. Xiaoni Li，Hexin Chen, Dazhong Wang and Xiaoiyin Qi. Research on Audio-Video Synchronization Coding Based on Mode Selection in H.264. Applied Mechanics and Materials, 2012, 182-183: 701-705.",
"源地址": "https://dce.jlu.edu.cn/info/1067/1313.htm"
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
