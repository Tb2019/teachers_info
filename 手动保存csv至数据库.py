# -*- coding: utf-8 -*-
# 数据提取完毕 入库失败时使用。或者
import csv
import os
from asyncio.log import logger
from utils import csv_2_df, truncate_table, df2mysql, drop_duplicate_collage, local_engine, sf_engine, save_as_json
from urllib import parse

school_id = 89
college_id = 479
school_name = '中山大学'
college_name = '网络空间安全学院'

img_url_head = ''

data_real = {
"姓名": "戴宪华",
"电话": "",
"邮箱": "issdxh@mail.sysu.edu.cn",
"职称": "教授",
"个人简介": "戴宪华，教授，博士生导师。目前主要研究领域为无线移动通信、人工智能深度学习算法（图像识别，自然语言处理）、生物信息处理。近年来，在领域内发表论文200余篇，其中SCI、EI收录论文150余篇；申请国内发明专利60余项 。已先后主持完成包括6项国家自然科学基金项目在内的共20项省市级项目、参与包括华为、阿里、浩鲸云等公司的多项企业合作、应用技术落地项目。主要从事信号处理类、通信类课程教学，每年2门本科生课程课堂教学、1门研究生课程课堂教学。截止目前共培养毕业(含校外培养)博士生20+、硕士150+。",
"教育经历": "国内某大学 声呐专业 工学学士\n东南大学 信号与信息处理专业 工学硕士\n东南大学 信号与信息处理专业 工学博士\n华南理工大学 通信与信息系统专业 博士后\n美国新泽西理工学院(NJIT)电机与计算机工程系（ECE）访问学者",
"工作经历": "",
"研究方向": "",
"人才称号": "",
"行政称号": "",
"专利": "申请国内发明专利60余项 。",
"科研项目": "国家自然科学基金项目，《重大疾病多组学与医学大数据挖掘 基础理论及关键技术》，时间2018.01-2022.01，67万，在研；\n广东省自然科学基金重大基础研究培育， 《下一代千兆 NG-DSL 通信系统关键技术研究》 ，时间 2015,1-2018,12，100 万，在研，主持；\n广州市科技计划项目，《异构无线网络的资源管理与调度》，项目编号：20143500042050472，2014.01-2015.12，8万，主持；\n国家自然科学基金项目《细胞命运控制统计模型建模与机理分析》，项目批准号：61174163，时间：2012,1-2015,12。主持；\n国家自然科学基金项目《基于隐藏导频的感知无线电时变信道估计与 长超前预测》 ，项目批准号：60772132；起止时间：2008，1-2009，12。主持；\n国家自然科学基金项目《基于信息几何的真核生物基因表达与系统调控的新理论新方法研》 ，项目批准号：60474075；起止时间：2005,1-2005,12。主持；\n国家自然科学基金项目《线性时变系统盲辨识与长超前预测理论研究及应用》 ，项目批准号：60272068；起止时间：2003,1-2005,12。主持；\n国家自然科学基金项目《非线性自适应信号处理新理论新方法的研究》 ，项目批准号：69872021；起止时间：1999,1-2001,12。主持；\n教育部骨干教师资助项目《盲信号处理理论及应用研究》，2000-2001。主持；\n教育部科学技术研究重点项目《基于盲信号处理的现代通信理论与技术研究》， 2002，1-2004，12。主持；\n广东省自然科学基金《非线性自适应信号处理理论及应用》，1999-2001。主持；\n广东省自然科学基金《基于信息几何的非线性信号处理》，1998-1999。主持；\n华为等企业委托横向项目多项。",
"荣誉/获奖": "",
"照片地址": "",
"最高学历": "研究生",
"最高学位": "博士",
"职位": "教授",
"办公地点": "",
"科研论文": "Guishan Zhang, Zhiming Dai, Xianhua Dai. C-RNNCrispr: Prediction of CRISPR/Cas9 sgRNA activity using convolutional and recurrent neural networks. Computational and Structural Biotechnology Journal, 18 (2020): 344-354. [SCI]期刊论文\nGuishan Zhang, Yiyun Deng, Qingyu Liu, Bingxu Ye, Zhiming Dai, Yaowen Chen, Xianhua Dai. Identifying circular RNA and predicting its regulatory interactions by machine learning. Frontiers in Genetics 11(2020) DOI: 10.3389/fgene.2020.00655  [SCI]期刊论文\nBaoxian Yu, Changjian Guo, Sen Zhang, Tianjian Zuo, Lei Liu, Han Zhang, Xianhua Dai, Alan Pak Tao Lau, Chao Lu. Chromatic dispersion mitigation using a SEFDM based diversity technique for IM/DD long reach optical links [J]. Optics Express, ,2019, 27(26), 38579-38592 [SCI]期刊论文\nBaoxian Yu, Changjian Guo, Langyu Yi, Han Zhang, Jie Liu, Xianhua Dai, Alan Pak Tao Lau, Chao Lu. 150-Gb/s SEFDM IM/DD transmission using log-MAP Viterbi decoding for short reach optical links [J],  Optics Express，2018, 26(24), 31075-31084. [SCI]期刊论文\nBaoxian Yu, Han Zhang, Xudong Hong, Changjian Guo, Alan Pak Tao Lau, Chao Lu, Xianhua Dai. Channel equalisation and data detection for SEFDM over frequency selective fading channels [J]. Communications, IET, 2018, 12(18):2315-2323 [SCI]期刊论文",
"源地址": "https://scst.sysu.edu.cn/members/members01/1410202.htm"
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
