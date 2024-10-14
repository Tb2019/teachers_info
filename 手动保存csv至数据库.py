# -*- coding: utf-8 -*-
# 数据提取完毕 入库失败时使用。或者
import csv
import os
from asyncio.log import logger
from utils import csv_2_df, truncate_table, df2mysql, drop_duplicate_collage, local_engine, sf_engine, save_as_json
from urllib import parse

school_id = 91
college_id = 380
school_name = '华东师范大学'
college_name = '数学科学学院'

img_url_head = ''

data_real = {
"姓名": "赵强",
"电话": "022-83662855",
"邮箱": "qiangzhao@nankai.edu.cn",
"职称": "教授",
"个人简介": "博士，南开大学生命科学学院暨药物化学生物学国家重点实验室教授（博士生导师），教育部生物活性材料重点实验室副主任，天津市重点实验室主任。先后获得国家杰出青年科学基金（2019）、国家优秀青年科学基金（2015）和天津市杰出青年科学基金（2018）资助。入选天津市131创新型人才第一层次。担任中国生物医学工程学会理事、中国解剖学会血管分会常委、中国生物医学工程学会干细胞工程技术分会常委、中国生理学会基质生物学分会委员（青委会主委）、Fundamental Research编委、Engineered Regeneration 副主编等。",
"教育经历": "2004/3 - 2006/9，天津大学，材料学，博士 \n2001/9 - 2004/2，天津大学，材料学，硕士 \n1997/9 - 2001/7，西北工业大学，高分子材料与工程，学士",
"工作经历": "2014/12 - 至今， 南开大学，生命科学学院，教授 \n2009/11 – 2014/12，南开大学，生命科学学院，副教授 \n2014/3 - 2014/4， 英国伦敦大学国王学院，医学院，访问学者 \n2006/9 - 2009/9， 香港城市大学，物理与材料科学系，博士后研究员",
"研究方向": "主要从事心血管生物材料与再生医学研究，利用工程材料科学、化学生物学等新技术、新方法，开展交叉研究，发展用于心血管修复再生与心血管疾病治疗的新材料与新技术。主持国家重点研发计划等省部级以上科研项目10余项。在国际权威学术期刊Nat Chem Biol、Nat Commun、Cell Rep、Adv Mater、Cir Res、Adv Sci、J Am Soc Nephrol、Biomaterials、J Control Release等发表SCI收录论文90余篇，论文他人引用>4000次，学术影响h-指数=38。在国际权威出版机构RSC、Springer等出版著作章节6部。申请并获得授权发明多项。先后获得天津市自然科学一等奖（2019，2/11）和天津市科技进步二等奖（2016，1/8；2021，5/8）。",
"人才称号": "",
"行政称号": "",
"专利": "",
"科研项目": "1. 国家杰出青年科学基金项目“心血管生物材料” (项目批准号：81925021)，项目负责人\n2. 国家重点研发计划-战略性国际科技创新合作重点专项“基于化学生物学‘凸凹互补’原理的工程化酶的理性设计与医学应用” (项目批准号：2018YFE0200500)，项目负责人\n3. 国家优秀青年科学基金项目“心血管生物材料” (项目批准号：81522023)，项目负责人\n4. 国家自然科学基金创新研究群体项目“组织器官损伤的修复与再生” (项目批准号：81921004)，项目骨干\n5. 国家自然科学基金重大研究计划（培育项目）“通过仿生天然细胞外基质构建功能型人工血管促进组织再生重构” (项目批准号：91639113)，项目负责人\n6. 国家自然科学基金（面上项目）“基于化学生物学“凸凹互补”原理构建靶向一氧化氮递送系统用于缺血性疾病治疗” (项目批准号：81871500)，项目负责人\n7. 国家自然科学基金（面上项目）“具有微/纳米复合纤维结构的小口径人工血管构建及对组织再生的引导作用” (项目批准号：81371699)，项目负责人\n8. 国家自然科学基金（青年基金）“人工血管材料的多重功能化修饰及空间分布调控” (项目批准号：81000680)，项目负责人\n9. 国家自然科学基金（国际（地区）合作与交流项目）“用于血管再生的新型生物材料研究” (项目批准号：81310108034)，项目负责人\n10. 高等学校博士学科点专项科研基金（新教师类）“活性人工血管的构建和功能评价”(项目批准号：20100031120021)， 项目负责人\n11. 天津市杰出青年科学基金“心血管生物材料” (项目批准号：18JCJQJC46900)，项目负责人\n12. 天津市应用基础与前沿技术研究计划（自然科学基金）青年项目资金“通过可控降解和功能梯度改善细胞向支架材料内生长” (项目批准号：12JCQNJC09300)， 项目负责人\n13. 分子科学国家实验室开放基金“具有可控释放一氧化氮（NO）功能的心血管生物材料研究”，项目",
"荣誉/获奖": "国家杰出青年科学基金（2019）\n国家优秀青年科学基金（2015）\n天津市杰出青年科学基金（2018）\n天津市“131人才”第一层次（2018）\n南开大学“百名青年学科带头人”（2016）\n南开大学第七届“良师益友”奖（2016）",
"照片地址": "https://sky.nankai.edu.cn/_upload/article/images/29/9c/2532c7f94dd9a4b29918d126efcb/31db881c-4dc3-464a-9a61-767353f42926_s.jpg",
"最高学历": "研究生",
"最高学位": "博士",
"职位": "教授",
"办公地点": "天津市南开区卫津路南开大学分子生物学研究所209",
"科研论文": "1. Hou J, Pan Y, Zhu D, Fan Y, Feng G, Wei Y, Wang H, Qin K, Zhao T, Yang Q, Zhu Y, Che Y, Liu Y, Cheng J*, Kong D, Wang PG, Shen J*, Zhao Q*. Targeted delivery of nitric oxide via a “bump-and-hole”-based enzyme-prodrug pair. Nat Chem Biol 2019, 15: 151-60 (recommended by F1000).\n2. Zhu D, Hou J, Qian M, Jin D, Hao T, Pan Y, Wang H, Wu S, Liu S, Wang F, Wu L, Zhong Y, Yang Z, Che Y, Shen J, Kong D, Yin M*, Zhao Q*. Nitrate-functionalized patch confers cardioprotection and improves heart repair after myocardial infarction via local nitric oxide delivery. Nat Commun 2021, 12: 4501.\n3. Wang F, Qin K, Wang K, Wang H, Liu Q, Qian M, Chen S, Sun Y, Hou J, Wei Y, Hu Y, Li Z, Xu Q*, Zhao Q*. Nitric oxide improves regeneration and prevents calcification in bio-hybrid vascular grafts via regulation of vascular stem/progenitor cells. Cell Rep 2022, 39:110981.\n4.  Midgley AC, Wei Y, Li Z, Kong D, Zhao Q*. Nitric oxide–releasing biomaterial regulation of the stem cell microenvironment in regenerative medicine. Adv Mater 2020, e1805818.\n5.  Hao T, Qian M, Zhang Y, Liu Q, Midgley AC, Liu Y, Che Ye, Hou J, Zhao Q*. An injectable dual-function hydrogel protects against myocardial ischaemia/reperfusion injury by modulating ROS/NO disequilibrium. Adv Sci 2022, 9: 2105408. ",
"源地址": "https://sky.nankai.edu.cn/zq1/list.htm"
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
