# -*- coding: utf-8 -*-
# 数据提取完毕 入库失败时使用。或者
import csv
import os
from asyncio.log import logger
from utils import csv_2_df, truncate_table, df2mysql, drop_duplicate_collage, local_engine, sf_engine, save_as_json
from urllib import parse

school_id = 86
college_id = 152
school_name = '华南理工大学'
college_name = '电子与信息学院'

img_url_head = ''

data_real = {
"姓名":"陈锐",
"电话":"",
"邮箱":"	chen_rui@tju.edu.cn",
"职称":"讲席教授",
"个人简介":"陈锐教授，英国拉夫堡大学（Loughborough University）低碳动力工程的终身教授，天津大学一级讲席教授，上海科学院新能源技术研究所氢能首席科学家，同时在西安交通大学，北京石油化工学院，厦门理工学院等多所大学任兼职教授。\n陈锐教授拥有近40年的学术研究和产业发展经验，是英国氢能和燃料电池研究计划科学委员会成员，科学研究涵盖低碳能源技术的建模和实验领域，内容包括热工学、电化学、流体动力学和系统工程。在英国，已培养博士34人、博士后12人，辅导访问学者20人，发表科研论文220 余篇（引用近6000，h指数37），作为项目负责人领导了40多个有资助研究项目，总计超过700万英镑，作为共同研究者参与了超过5500万英镑的科研项目，同英国、欧盟、中国、美国、韩国、日本、印度等多国的领先行业和科研机构在氢能和燃料电池等低碳技术领域有着广泛的合作。\n近5年主持和参与了20余科研项目，包括英国商业、能源和工业战略部（BEIS）“英国氢气质量标准热能承包示范Hy4Heat”；英国工程和物理科学研究基金会（EPSRC）与路虎（JLR）“电动自动驾驶汽车的智能热能管理”，与Bosch“两级低温氢气燃烧”，与英国太空系统公司（BAE Systems）“下一代无人机氢燃料电池推进系统”；英国文化协会（British Council）“高能量密度甲醇燃料电池的新型催化剂和流场设计”；中国国家自然科学基金国际合作重点项目“极板-电极一体化质子交换膜燃料电池多场耦合传输机理研究”（英方负责人）。\n陈锐教授的研究涵盖应用热流体和应用电化学，以控制排放和提高能量效率为目标，把能源工程领域的研究策略定位于高效率低排放的先进发动机燃烧、燃料电池及其相应的理论分析， 形成了热科学（Thermosciences）、电化学（Electrochemistry）、燃料（Fuels）、混合动力（Hybrid）四大科研领域。自1996年拉夫堡大学任职以来，已发表科技论文200余篇，负责数十项科研项目总计约6万英镑，参与多项科研项目总计约3千万英镑。",
"研究方向":"Electro-chemistry: PEM Fuel Cells; catalytic reactions; degradation; catalyst agglomeration; electrochemistry impedance spectrum (EIS); battery diagnostics; water polymer electrolysis; H2O2-NaBH4 liquid fuel cell.\nThermo-science: thermo-electric waste heat energy recoveries; avionic thermal analysis and management; combustion kinetics; engine downsize; multi-mode combustion; alternative fuels; catalytic burner; fuel catalytic reforming; battery thermal management; characteristics of super-critical water.\nFluid-dynamics: multi-phase multi-dimensional mass and heat transfer; gas diffusion and numeric modelling; x-ray tomography.\nSystem engineering: avionic environmental control system (ECS); water and thermal management of regenerative fuel cell; More electric aircraft hydrogen propulsion.",
"专利":"",
"科研项目":"1.“ATF: Moving the UK automotive sector to zero emissions: Classic Car ElectRificatiOn (CICERO)”, Innovate UK (Ref. No.84685), 2020-2022\n2.“重点国际（地区）合作研究项目：极板-电极一体化质子交换膜燃料电池多场耦合传输机理研究”, 中国国家自然科学基金会 National Natural Science Foundation of China (51920105010), 2020 – 12.2024\n3.“Fuel Cell Modelling for Military Applications”, MBDA UK Limited, 2019 – 2020\n4.“Hydrogen Quality Standard Contractor for UK hydrogen for heat demonstration (Hy4Heat)”, Department for Business, Energy and Industrial Strategy (BEIS): 1525/06/2018, 2017 – 2021\n5.“Design and development of a four-wheeled electric vehicle for research, teaching and outreach in Tamil Nadu, India”, The Royal Academy of Engineering, 2019 (2 years)\n6.“Battery extreme environment charge and discharge evaluations”, Mahle Powertrain Ltd., 2019\n7.“Intelligent Thermal Energy Management for Battery Electric and Autonomous Vehicles”, Jaguar Land Rover & EPSRC (iCASE18000088), 2019 – 2023.\n8.“Investigation of methane/hydrogen combustion in Euro VI engines for heavy duty vehicles”, Ricardo and University of Brighton Project, 2018 – 2021.\n9.“Two-Stage Low-Temperature Hydrogen Combustion”, Engineering and Physical Sciences Research Council (EPSRC) and Bosch Thermotechnology Ltd., 2017 – 2021.\n10.“Methanol Fed High Energy Density Fuel Cell System with Novel Catalyst and Flow Field Design”, British Council DST-UKIERI-2016-17-0023, 2017 – 2020.",
"荣誉/获奖":"",
"照片地址":"/upload/teacherImg/4f5526b0ba064612a45af9e96598038e.png",
"最高学历":"研究生",
"最高学位":"博士",
"职位":"讲席教授",
"办公地点":"天津市南开区卫津路92号天津大学先进内燃动力全国重点实验室",
"科研论文":"1.(2024) che zhizhao, tao xingxiao, sun kai, chen rui, lqf01, liu huaiyu, zwz409, wang tianyou, “Effect of gas diffusion layer parameters on cold start of PEMFCs with metal foam flow field”. APEN-D-23-07037R1, Applied Energy.\n2.(2023) Xingxiao Tao, Kai Sun, Rui Chen, Mengshan Suo, Huaiyu Liu, Zhizhao Che, Tianyou Wang, “Two-phase flow in porous metal foam flow fields of PEM fuel cells”. Chemical Engineering Science. Volume 282, 5 December 2023, 119270 https://doi.org/10.1016/j.ces.2023.119270\n3.(2023) Zhen Zeng, Kai Sun, Rui Chen, Mengshan Suo, Zhizhao Che, and Tianyou Wang, “Variation of Critical Crystallization Pressure for the Formation of Square Ice in Graphene Nanocapillaries”. The Journal of Physical Chemistry C - ACS Publications. 2023, 127, 30, 14874–14882. https://doi.org/10.1021/acs.jpcc.3c00619\n4.(2023) Milon Miah, Poulami Hota, Tapas Kumar Mondal, Rui Chen, Shyamal K. Saha, “Mixed metal sulfides (FeNiS2) nanosheets decorated reduced graphene oxide for efficient electrode materials for supercapacitors”. Journal of Alloys and Compounds. Volume 933, 5 February 2023, 167648. https://doi.org/10.1016/j.jallcom.2022.167648\n5.(2023) Ren Zhang, Lin Chen, Haiqiao Wei, Jinguang Li, Yi Ding, Rui Chen, Jiaying Pan, “Experimental investigation on reactivity-controlled compression ignition (RCCI) combustion characteristic of n-heptane/ammonia based on an optical engine”. International Journal of Engine Research. Volume 24, Issue 6. https://doi.org/10.1177/14680874221124452"
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
