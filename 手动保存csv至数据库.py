# -*- coding: utf-8 -*-
# 数据提取完毕 入库失败时使用。或者
import csv
import os
from asyncio.log import logger
from utils import csv_2_df, truncate_table, df2mysql, drop_duplicate_collage, local_engine, sf_engine, save_as_json
from urllib import parse

school_id = 83
college_id = 154
school_name = '山东大学'
college_name = '电气工程学院'

img_url_head = ''

data_real = {
"姓名":"张杰",
"电话":"13086681699",
"邮箱":"zhangjie@scu.edu.cn",
"职称":"教授",
"个人简介":"  张杰教授，博士生导师。1987年本科毕业于原成都科技大学，1987年至1991年在杭州照相机械研究所工作，1991年至1994在四川大学高分子材料成型加工专业攻读硕士学位，毕业后留校任教。2002年获博士学位，2004年至2005年在英国 Loughborough University作访问学者，2007年晋升教授，是四川省海外高层次留学人才、四川省学术和技术带头人后备人选。先后担任中国模具标准化技术委员会委员/专家组成员、中国生产工程学会模具制造专业委员会委员、《塑料机械》杂志编委、成都市机械工程学会模具分会理事长、成都市模具工业协会常务理事等职。\n主要从事先进聚合物加工方法和技术的研究，通过材料凝聚态结构的设计与定构，实现聚合物材料的高性能化。如在注射成型过程中引入振动场的振动注射成型技术、在挤出过程中通过施加周向剪切场实现复合管材高性能化的挤出成型技术、聚合物基功能复合材料3D打印加工技术、聚合物熔体解缠结技术、模具CAD/CAE技术、微注塑成型技术等。主持或参加了包括国家自然科学基金重大科研仪器研制项目、国家自然科学基金重点项目、国家自然科学基金国际合作重大项目、国家自然科学基金面上项目、四川省科技支撑项目、教育部留学回国人员科研启动基金、高分子材料工程国家重点实验室主任基金、高分子材料工程国家重点实验室自主课题、聚合物分子工程国家重点实验室（复旦大学）开放课题、大连理工大学精密与特种加工教育部重点实验室开放课题、四川大学青年基金在内的多个项目，同时主持过多个与企业合作的横向项目。\n共发表学术论文140多篇，其中以第一作者或通讯作者在包括Macromolecules、Carbon、Additive Manufacturing、Composites Part B-Engineering、 Polymer等杂志上发表SCI收录论文90余篇。主编专著两部，已授权专利8项。已培养硕博士研究生39人，在读11人。2020年获四川省科学技术进步一等奖、2018年获中国循环经济协会科学技术奖一等奖、2016年获佛山市科学技术二等奖。",
"研究方向":"主要从事先进聚合物加工方法和技术的研究，通过材料凝聚态结构的设计与定构，实现聚合物材料的高性能化。",
"专利":"已授权专利8项",
"科研项目":"主持或参加了包括国家自然科学基金重大科研仪器研制项目、国家自然科学基金重点项目、国家自然科学基金国际合作重大项目、国家自然科学基金面上项目、四川省科技支撑项目、教育部留学回国人员科研启动基金、高分子材料工程国家重点实验室主任基金、高分子材料工程国家重点实验室自主课题、聚合物分子工程国家重点实验室（复旦大学）开放课题、大连理工大学精密与特种加工教育部重点实验室开放课题、四川大学青年基金在内的多个项目，同时主持过多个与企业合作的横向项目。",
"荣誉/获奖":"2020年获四川省科学技术进步一等奖、2018年获中国循环经济协会科学技术奖一等奖、2016年获佛山市科学技术二等奖。",
"照片地址":"https://cpse.scu.edu.cn/__local/5/BC/DF/483C0A6D191906AA87CF953261C_28A7C300_520D4.jpg",
"最高学历":"研究生",
"最高学位":"博士",
"职位":"教授",
"办公地点":"",
"科研论文":"1. Jiang, Yixin; Leng, Jie; Zhang, Jie*. A high-efficiency way to improve the shape memory property of 4D-printed polyurethane/polylactide composite by forming in situ microfibers during extrusion-based additive manufacturing, ADDITIVE MANUFACTURING , 2021, 38\n2. Luo, Jiaxu; Liu, Mingjin; Chen, Jin; Min, Jie; Fu, Qiang*; Zhang, Jie*. Effectively maintaining the disentangled state of isotactic polypropylene in the presence of graphene nanoplatelet, POLYMER, 2021, 226\n3. Hong, Rui; Jiang, Yi-Xin; Leng, Jie; Liu, Ming-Jin; Shen, Kai-Zhi; Fu, Qiang; Zhang, Jie*. Synergic Enhancement of High-density Polyethylene through Ultrahigh Molecular Weight Polyethylene and Multi-flow Vibration Injection Molding: A Facile Fabrication with Potential Industrial Prospects, CHINESE JOURNAL OF POLYMER SCIENCE, 2021, 39(6): 756-769\n4. Jiang, Yixin; Wu, Junjie; Leng, Jie; Cardon, Ludwig; Zhang, Jie*. Reinforced and toughened PP/PS composites prepared by Fused Filament Fabrication (FFF) with in-situ microfibril and shish-kebab structure, POLYMER, 186\n5. Liu, Mingjin; Luo, Jiaxu; Chen, Jin; Gao, Xueqin; Fu, Qiang; Zhang, Jie*. Unique Slow Crack Growth Behavior of Isotactic Polypropylene: The Role of Shear Layer-Spherulites Layer Alternated Structure, POLYMERS , 2020, 12(11)"
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
