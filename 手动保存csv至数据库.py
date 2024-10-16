# -*- coding: utf-8 -*-
# 数据提取完毕 入库失败时使用。或者
import csv
import os
from asyncio.log import logger
from utils import csv_2_df, truncate_table, df2mysql, drop_duplicate_collage, local_engine, sf_engine, save_as_json
from urllib import parse

school_id = 91
college_id = 387
school_name = '华东师范大学'
college_name = '地理科学学院'

img_url_head = ''

data_real = {
"姓名": "姜雪峰",
"电话": "021-62233009",
"邮箱": "xfjiang@chem.ecnu.edu.cn",
"职称": "教授",
"个人简介": "姜雪峰，华东师范大学二级教授，中国化学会会士，英国皇家化学会会士，上海市政协委员（第十三、十四届），上海市青联副主席，上海市青科协副主席。国家杰青、国家优青、国家万人，教育部青年长江学者、新世纪优秀人才、霍英东基金，上海市领军人才、优秀学术带头人、东方学者及优秀跟踪、五四青年奖章、青年岗位能手。曾获2024年全国颠覆性技术创新大赛奖，2023年全国创新争先奖，2023年上海市十大青年科技杰出贡献奖，2023年上海市海聚英才全球创新创业大赛金奖，2023年上海市未来产业风云奖，2023年上海市科学技术普及一等奖，2022年上海市大众科学传播杰出人物，2021年上海产学研合作优秀项目奖二等奖，2020年中美化学与化学生物学教授协会杰出教授奖，2020年上海市科普贡献个人一等奖，2019年中国均相催化青年奖，2019年亚洲联合化学会Rising Stars Lectureship Award，2018年IUPAC元素周期表青年科学家硫元素代言人，2017年药明康德生命化学研究奖，德国Thieme Chemistry Journal Award，日本ACP Lectureship Award，2020-2023连续四年Elsevier中国高被引学者。中国化学会有机化学学科委员会委员，中国化学会糖化学专业委员会，中国化学会公共安全化学专业委员会委员，中国化学会催化委员会均相催化专业委员会委员，中国化学会科普工作委员会委员，中国化学会青委会委员，中国化工学会专业委员会委员，中国感光协会委员，中国生物医药产业链创新转化（CBIITA）联合体原料药专委会副主委。中国青年科技工作者协会理事，上海科技传播协会理事，上海市科普作协理事，上海科普协会院士专家指导团。《Green Synthesis and Catalysis》、《Essential Chem》、《化学教育》、《化学试剂》副主编，《National Science Review》、《Science Bulletin》、《化学通讯》编委，美国化学会《ACS Sustainable Chemistry & Engineering》、《Organometallics》，Wiley《European Journal of Organic Chemistry》、《Heteroatom Chemistry》、《Journal of Sulfur Chemistry》、《Phosphorus Sulfur Silicon and the Related Elements》，《Tetrahedron》、《Tetrahedron Letters》顾问编委。",
"教育经历": "2008-2011： 美国Scripps研究所，博士后，导师：K. C.Nicolaou教授\n2003-2008： 中国科学院上海有机化学研究所，博士，导师：麻生明 院士\n1999-2003： 西北大学化学与材料科学学院，学士",
"工作经历": "2011.9-至今：华东师范大学化学系，教授，博士生导师",
"研究方向": "1）合成方法创制导向的药用天然产物全合成、功能材料合成。\n2）科学本质建模导向的高端仪器开发、合成自动化与智能化。",
"人才称号": "",
"行政称号": "",
"专利": "",
"科研项目": "国家杰出青年科学基金（22125103）\n国家优秀青年科学基金（21722202，结题优秀）\n国家自然科学基金“面上基金”（21971065, 21672069, 21472050, 21272075）\n“万人计划”青年拔尖人才\n教育部“长江学者奖励计划”青年项目（2017）\n教育部“新世纪优秀人才”（120178）\n教育部“霍英东基金”（141011）\n教育部“博士点博导基金”（20130076110023）\n教育部“创新团队发展计划”基金（2012, 2017, 参与）\n教育部首批优秀创新创业导师（2017）\n教育部“国家培养计划”授课专家（2017）\n国家重点研发计划：“农业生物药物分子靶标发现与绿色药物分子设计” (2017YFD0200500, 参与）\n科技部“973”（2015CB856600, 参与）\n上海市基础研究领域项目“室温低能耗真实塑料的降解及单体的回收”（22JC1401000，主持）\n上海市“优秀学术带头人”（20XD1421500）\n上海市“青年岗位能手”（2015）\n上海市“青年五四奖章” (2014)\n上海市“青年科技启明星” (15QA1401800, 结题优秀)\n上海市“人才发展资金” (2011022, 结题)\n上海市普陀区“拔尖人才” (2013, 结题)\n上海市基础研究领域项目“模拟维生素B6与B12相关酶仿生构建手性胺的研究”（20JC1416800, 参与）\n上海市基础研究领域项目“电化学氧化促进的碳氢键选择性转化”（18JC1415600, 参与）\n上海市教委协同创新团队项目（SSMU-ZLCX20180501, 参与）",
"荣誉/获奖": "华东师范大学青年科学奖（A类）（2019）\n紫江优秀青年学者（2015，结题优秀）\n青年英才学者（2011，结题优秀）\n2024 全国颠覆性技术创新大赛\n2023 全国创新争先奖\n2023 上海市十大青年科技杰出贡献奖\n2023 上海市海聚英才全球创新创业大赛金奖\n2023 上海市科学技术普及一等奖\n2023 上海市高价值专利运营大赛高校组第一名\n2023 未来产业风云奖\n2023 春申金字塔杰出人才\n2022 Elsevier中国高被引学者\n2022  生命科学新力量年度人物\n2022 上海市大众科学传播杰出人物\n2021 中科院Clarivate化学与材料科学十大热点前沿：\n\t1. 二氧化硫插入策略合成磺酰类功能分子； 2. 非共价相互作用（卤键、硫键）\n2021  Elsevier2020年中国高被引学者\n2021 上海市产学研合作项目二等奖\n2020 上海市科普贡献奖个人一等奖\n2020 中美化学与化学生物学教授协会杰出教授奖(CAPA Distinguished Faculty Award) \n2019 中国均相催化青年奖\n2019 “Asian Rising Stars” Lectureship Award\n2019  2018 RSC Top 1%高被引中国作者\n2019 Excellent Research Advisor in ACS Shanghai Chapter \n2018 Ambassador of “Sulfur”in “Periodic Table of Younger Chemists”\n2017 药明康德生命化学研究奖 ( WuXi AppTec)\n2016 Asian Core Program Lectureship Award (Singapore)\n2015 New Organosulfur Chemistry at Pacifichem  (Co-chairman, Hawaii, USA)\n2014 Asian Core Program Lectureship Award ( Japan)\n2014 Asian Core Program Lectureship Award (Singapore)\n2013 Thieme Chemistry Journal Award(Germany)",
"照片地址": "https://faculty.ecnu.edu.cn/_upload/article/images/54/03/fe0f0eef4c9489fa42f7e3acab76/9b6fe313-c1f5-4e26-9275-5d64db8e4b61_s.jpg",
"最高学历": "研究生",
"最高学位": "博士",
"职位": "教授",
"办公地点": "上海市普陀区中山北路3663号化学馆A-321室",
"科研论文": "214. Photouranium-Catalyzed C−F Activation Hydroxylation via Water Splitting,X. Zhao, L. Bai, J. Li,  X. Jiang*,J. Am. Chem. Soc. 2024, 146, 11173-11180.\n213. Bilateral Unsymmetrical Disulfurating Reagent Design for Polysulfide Construction,Q. Yu, X. Zhang, X. Jiang*,Angew. Chem. Int. Ed. 2024, e202408158.\n212. From Polyester Plastics to Diverse Monomers via Low-Energy Upcycling,L. Ji, J. Meng, C. Li, M. Wang, X. Jiang*,Advanced Science 2024, 11, 2403002.\n211. C-SuFEx Linkage of Sulfonimidoyl Fluorides and Organotrifluoroborates,S. Zhao, D. Zeng, M. Wang*, X. Jiang*,Nat. Commun. 2024, 15, 727.\n210. From Aryl Chlorides to Phenols: Photouranium-Catalyzed Hydroxylation via Water-splitting,M. Sun, L. Bai, C. Li, X. Jiang*,Chem Catal. 2024, 4, 101027.",
"源地址": "https://faculty.ecnu.edu.cn/_s34/jxf/main.psp"
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
