# -*- coding: utf-8 -*-
# 数据提取完毕 入库失败时使用。或者
import csv
import os
from asyncio.log import logger
from utils import csv_2_df, truncate_table, df2mysql, drop_duplicate_collage, local_engine, sf_engine, save_as_json
from urllib import parse

school_id = 104
college_id = 281
school_name = '上海交通大学'
college_name = '自然科学研究院'

img_url_head = ''

data_real = {
"姓名": "金石",
"电话": "",
"邮箱": "",
"职称": "",
"个人简介": "",
"教育经历": "",
"工作经历": "",
"研究方向": "",
"人才称号": "",
"行政称号": "",
"专利": "",
"科研项目": "",
"荣誉/获奖": "Sigma Xi Young Faculty Award, Georgia Tech, 1997\nFeng Kang Prize for Scientific Computing, Chinese Academy of Sciences, 2001\nDistinguished Overseas Young Scientist Award , National Science Foundation of China, 2002-2005.\nVan Vleck Distinguished Research Prize, Department of Mathematics, University of Wisconsin-Madison, 2007-2011.\nMorningside Silver Medal of Mathematics, Fourth International Congress of Chinese Mathematicians, Dec. 2007.\nCopernicus Visiting Scientist,, University of Ferrara, Italy, June 2010\nVilas Associate Award,, University of Wisconsin-Madison, 2010-2012\nSupervised a National Excellent Doctoral Thesis of China (honorable mention), Ministry of Education of China, 2012\nInaugural class of Fellow of the American Mathematical Society (AMS Fellow), 2012.\nFellow of the Society for Industrial and Applied Mathematics (SIAM Fellow), 2013.\nVilas Distinguished Achievement Professorship, University of Wisconsin-Madison, 2015.\nNelder Visiting Fellow, Imperial College, London, UK, 2018.\nInvited Speaker, International Congress of Mathematicians (ICM) , Rio de Janeiro, Brazil, 2018.\n(Inaugural) Best Article Award , Research in the Mathematical Sciences, Springer, 2019.\nOne of the Best Papers of 2019 , M3AS.\nInaugural class of Fellow of China Society of Industrial and Applied Mathematics (CSIAM Fellow)， 2020.\nThe Jean-Morlet Chair, CIRM, France, 2021.\nJournal of Computational Physics Seminar series (based on articles selected by the editorial board for being particularly innovative and/or having had significant recent impact)，Nov. 2021.\nFellow of European Academy of Sciences, 2021.\nForeign Member of Academia Europaea, 2021.\nTop Ten Advances in Sciences and Technology of Shanghai Jiao Tong University in year 2020, (for works in Random Batch Methods in interacting particle systems and molecular dynamics), 2022.\nJournal of Computational Physics Seminar series (based on articles selected by the editorial board for being particularly innovative and/or having had significant recent impact)，Nov. 2023.",
"照片地址": "https://ins.sjtu.edu.cn/people/shijin/images/people-6a3d39e5.jpg",
"最高学历": "",
"最高学位": "",
"职位": "",
"办公地点": "",
"科研论文": "[234] Junpeng Hu, Shi Jin, Lei Zhang, Quantum algorithms for multiscale partial differential equations, (SIAM) Multiscale Model. Simulation 22， 1030–1067， 2024.\nShi Jin and Nana Liu, Quantum simulation of discrete linear dynamical systems and simple iterative methods in linear algebra via Schrodingerisation, Proc. Royal Soc. London A, 480, 20230370, 2024.\nShi Jin, Xiantao Li， Nana Liu and Yue Yu, Quantum Simulation for Quantum Dynamics with Artificial Boundary Conditions, SIAM J. Sci. Comp., 46， B403–B421， 2024.\nYiwen Lin, Shi Jin, Error estimates of a bi-fidelity method for a multi-phase Navier-Stokes-Vlasov-Fokker-Planck system with random inputs, Kinetic and Related Models 17, 807-837， 2024.\nShi Jin and Nana Liu, Quantum algorithms for nonlinear partial differential equations, Bull. Math. Sci., 194，103457， 2024.",
"源地址": "https://ins.sjtu.edu.cn/people/shijin/#former-ph-d-students"
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
