# -*- coding: utf-8 -*-
# 数据提取完毕 入库失败时使用。或者
import csv
import os
from asyncio.log import logger
from utils import csv_2_df, truncate_table, df2mysql, drop_duplicate_collage, local_engine, sf_engine, save_as_json
from urllib import parse

school_id = 95
college_id = 321
school_name = '华中科技大学'
college_name = '电子信息与通信学院'

img_url_head = ''

data_real = {
"姓名": "陈柯",
"电话": "",
"邮箱": "chenke@hust.edu.cn",
"职称": "副教授",
"个人简介": "陈柯，男，1977年生，博士，华中科技大学副教授。1999年本科毕业于华中科技大学电子与信息工程系通信工程专业并留校任教，2002年获得华中科技大学电子与信息工程系电磁场与微波技术专业硕士学位，2010年获得华中科技大学电子与信息工程系通信与信息系统专业博士学位。2013年12月~2014年12月以访问学者身份选派到美国科罗拉多大学Boulder分校ECEE系CET实验室进行交流学习并开展科研工作。主要的研究方向为无源微波遥感、探测。2010年作为负责人承担完成国家自然科学基金青年基金项目“盐度遥感综合孔径微波辐射计干涉测量理论与方法研究”的科研工作；2011年作为主要执行负责人承担完成了应用单位合作项目“二维毫米波综合孔径辐射计阵列成像系统”、“微波遥感探测仪总体方案指标分析与仿真”的研究工作；2012年作为负责人正在承担国家自然科学基金面上项目“基于综合孔径的地球静止轨道气象卫星毫米波大气探测载荷理论与关键技术研究”。在美国期间参与CET实验室项目‘Hydrometric Tracking Simulator’的研究。在IEEE TGRS，IEEE GRSL、Journal of Infrared Millimeter and Terahertz Waves、微波学报等权威学术期刊以及国际国内学术会议上发表论文十余篇，多篇被SCI、EI收录。",
"教育经历": "1999年本科毕业于华中科技大学电子与信息工程系通信工程专业并留校任教\n2002年获得华中科技大学电子与信息工程系电磁场与微波技术专业硕士学位\n2010年获得华中科技大学电子与信息工程系通信与信息系统专业博士学位。",
"工作经历": "2013年12月~2014年12月以访问学者身份选派到美国科罗拉多大学Boulder分校ECEE系CET实验室进行交流学习并开展科研工作。",
"研究方向": "无源微波遥感、探测",
"人才称号": "",
"行政称号": "",
"专利": "",
"科研项目": "2010年作为负责人承担完成国家自然科学基金青年基金项目“盐度遥感综合孔径微波辐射计干涉测量理论与方法研究”的科研工作；2011年作为主要执行负责人承担完成了应用单位合作项目“二维毫米波综合孔径辐射计阵列成像系统”、“微波遥感探测仪总体方案指标分析与仿真”的研究工作；2012年作为负责人正在承担国家自然科学基金面上项目“基于综合孔径的地球静止轨道气象卫星毫米波大气探测载荷理论与关键技术研究”。在美国期间参与CET实验室项目‘Hydrometric Tracking Simulator’的研究。",
"荣誉/获奖": "",
"照片地址": "http://eic.hust.edu.cn/aprofessor/chenke/index.files/chenke_27192_image002.png",
"最高学历": "研究生",
"最高学位": "博士",
"职位": "副教授",
"办公地点": "",
"科研论文": "• Ke Chen, Yaoting Zhu，XiChen Guo, Wei Guo, QingXia Li, LiangQi Gui, Wei Ni. Design of 8mm-band Aperture Synthetic Radiometer and Imaging Experiment. Journal of Infrared, Millimeter and Terahertz Waves, 2010, 31 (6): 724-734. 	\n• Guoping Hu、*Ke Chen、Quanliang Huang、Wei Guo、Qingxia Li、Liangqi Gui、Yingbiao Cheng ，Brightness Temperature Calculation of Lunar Crater: Interpretation of Topographic Effect on Microwave Data From Chang’E ，IEEE Transactions on Geoscience and Remote Sensing, 52(8), pp 4499-4510, 2014/08/15	\n• 陈柯、赖利、*贺锋、李召阳 ，基于NUFFT算法的综合孔径辐射计图像反演方法 ，微波学报	\n• 陈柯，朱耀庭，郭伟，李青侠，桂良启，靳嵘. Ka波段毫米波综合孔径辐射计成像研究. 微波学报，2010，26（2）：85～89.	\n• Ke Chen、 Wei Guo、 Hong Yang、 Rong Jin、 Guanli Yi、 Fei Hu、 Jinhai Sun ，Error model and calibration 2012of synthetic aperture interferometric radiometer based on visibility function ，Geoscience and Remote Sensing Symposium (IGARSS), 2012 IEEE International, 2012/7/22-2012/7/27, pp 4633-4636, Munich, 2012/7/22",
"源地址": "http://eic.hust.edu.cn/aprofessor/chenke/index.htm"
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
