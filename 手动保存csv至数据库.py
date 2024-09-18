# -*- coding: utf-8 -*-
# 数据提取完毕 入库失败时使用。或者
import csv
import os
from asyncio.log import logger
from utils import csv_2_df, truncate_table, df2mysql, drop_duplicate_collage, local_engine, sf_engine, save_as_json
from urllib import parse

school_id = 104
college_id = 148
school_name = '上海交通大学'
college_name = '机械与动力工程学院'

img_url_head = ''

data_real = {
"姓名": "王如竹",
"电话": "021-34206548",
"邮箱": "rzwang@sjtu.edu.cn",
"职称": "教授",
"个人简介": "",
"教育经历": "1987.09―1990.05上海交通大学制冷与低温工程学科博士生;\n1988.4-1990.3在联邦德国柏林自由大学物理系低温实验室博士生联合培养\n1984.09―1987.02上海交通大学制冷与低温工程学科硕士生\n1980.09―1984.07上海交通大学制冷设备与低温技术专业本科生",
"工作经历": "1987.02―1987.08 上海交通大学动力机械工程系 助教\n1990.08―1992.12 上海交通大学动力机械工程系　讲师\n1992.12―1994.12 上海交通大学动力机械工程系　副教授\n1994.12― 上海交通大学动力机械工程系　教授\n1993.10―1997.08 上海交通大学制冷与低温工程研究所所长\n1997.06-2001.12 上海交通大学动力与能源工程学院副院长\n1999.09- 上海交通大学制冷与低温工程研究所所长\n2001.05-2007.10 上海交通大学太阳能发电及制冷工程研究中心常务副主任\n2001.12-2006.12 上海交通大学机械与动力工程学院副院长\n2007.11- 上海交通大学太阳能发电及制冷工程研究中心主任",
"研究方向": "制冷空调中的能源利用；\n低品位热能制冷技术；\n绿色建筑能源系统；\n热泵技术及其应用；\nEnergy-Water-Air Nexus;\n规模化储热与能质调控",
"人才称号": "",
"行政称号": "",
"专利": "累计专利163项，其中 1 EU patent, 1 USA patent, and 161 CN patents\n[1] R.Z. Wang, Y.D. Tu. T.S. Ge. Self-contained air conditioning system and use method. 2021, EP3457038. (UK, Germany, France, Italy, Spain)\n[2] R.Z. Wang, Y.D. Tu. T.S. Ge. Unitary air conditioning systems with temperature and humidity loosely- coupled control and use method. US Patent 16/300.571\n[3] B.Y. ZHAO, Y. LI, R.Z. Wang, M. HUANG, X.F. ZHANG, Y.Y. JIANG. Photovoltaic ice storage air conditioner prediction control method and photovoltaic ice storage air conditioner using same. 2021. CN Patent CN202010943649.2.\n[4] S. DU; Z.X. WANG; R.Z. WANG, H.Y. LI. S-type tube bundle falling film absorber. 2021. CN Patent CN201911108064.2.\n[5] T.S. Ge, J.Y. Wu, X.C. Zhu, F. Yang, R.Z. Wang. Overall structure adsorbent based on amine functionalized silica sol, preparation method and application. 2021. CN Patent CN202110484154.2.\n[6] Z.G. Wang, R.Z. Wang. Room air conditioner based on moisture storage heat exchanger and evaporation pre-treatment. 2021. CN Patent CN202010763200.8.\n[7] F.F. Deng, C.X. Wang, R.Z. Wang, S. Du, H. Zou. Greenhouse heat and humidity control, energy-saving and water-saving device and method. 2021. CN Patent CN202110391351.X.\n[8] H. Zou, C.X. Wang, R.Z. Wang, S. Du, F.F. Deng. Greenhouse heat storage and dehumidification equipment and working methods. 2021. CN Patent CN202110368370.0.\n[9] Q.W. Pan, R.Z. Wang. Adsorption type refrigeration system and operation method thereof. 2021. CN Patent CN202110290387.9.\n[10] Q.W. Pan, R.Z. Wang, H. Liu, K. Yu, Y. M. Open adsorption heat storage system and control method. 2021. CN Patent CN202110277121.0.",
"科研项目": "2019-2021， 上海交通大学-上海汉钟精机有限公司联合研究中心（300万元），负责人。\n2019.07-2022.06，上海交通大学-欧菲汽车热管理联合研究中心（600万元），负责人。\n2021.01-2025.12 国家自然科学基金重点项目“大温升热泵及蒸汽发生系统的循环构建与应用适应性研究”（52036004）（380万元）；负责人；在研。\n2023.01-2027.12 国家自然科学基金委重大项目 “规模化热能存储转换与能质调控机理和方法”（52293410 ) (1483.08万元）；负责人；在研。\n2023.08-2026.08 上海交通大学机械与动力工程学院—日出东方控股股份有限公司热泵关键技术联合研究中心 (项目编号：23H010203075)（600万元）；负责人；在研。",
"荣誉/获奖": "2012年度上海市优秀共产党员\n2013年度全国五一劳动奖章\n2014年度科技部重点领域创新团队负责人\n2015年国家自然科学基金委创新群体负责人\n2015年 全国先进工作者\n2016年 “万人计划”领军人才\n国际学术奖励：\n\n2013年英国制冷学会颁发的J&E Hall Gold Medal, (制冷大奖，全球第37人，首位华人）；\n2017年亚洲制冷学术奖励Asia Academic Award of Refrigeration(中国首位）；\n2018年日本传热学会颁发的Nukiyama Memorial Award (热科学大奖，全球第4人，中国首位）。\n2019年国际制冷学会颁发的IIR-Gustav Lorentzen Medal(国际制冷最高奖，全球第5人，首位华人）。\n2021年国际能源署（IEA）Rittinger国际热泵奖（Peter Ritter von Rittinger International Heat Pump Award，国际热泵最高奖，首位华人）。\n2021年国际吸收吸附热泵Georg Alefeld纪念奖（每3年1人，首位华人）\n2023年国际能源奖（Global Energy Prize) (每年1-3人，设立20届来首位中国获奖者）\n教学奖励：\n2010年所指导的齐守良博士论文“ 微通道中液氮流动和换热特性研究 ”获得全国优秀博士学位论文提名奖；\n2012年所指导的李廷贤博士论文“ 新型多效双重热化学吸附制冷循环研究 ”获得全国优秀博士学位论文提名奖；\n2013年所指导的葛天舒博士论文“ 转轮式两级除湿空调理论与实验研究 ”获得全国优秀博士学位论文提名奖；\n2016年所指导的郑旭博士论文“小温差再生的干燥剂的优选及其在除湿换热器中的应用”获得首届上海交通大学优秀博士学位论文奖励。\n2014年上海市教学成果二等奖，可再生能源新生研讨课的创新与实践，｛王如竹、葛天舒、李勇｝\n2014年“强化节能减排意识，提升创新实践能力，创建与推进全国大学生节能减排竞赛”国家级教学成果二等奖。（第7获奖人）\n科研奖励：\n2020年中国节能协会节能减排科技进步一等奖“宽环温高效节能空气源热泵供暖关键技术及产业化”（骆铭文，王如竹，张光鹏，胡斌，翟晓强，杨国忠）\n2022年上海市自然科学一等奖“高密度热储能及热调控原理与方法“ (李廷贤、王如竹、张鹏、仵斯）\n2022年中国科技产业化促进会科学技术奖”杰出贡献奖“；\n2022年何梁何利基金科学与技术创新奖；\n2023年中国机械工业科学技术奖一等奖“低温余热高效利用的吸收式热泵技术与应用”（王如竹，徐震原，毛洪财，杜帅，王炎丽，王红斌，贺湘晖，陆紫生，徐建虎，金德禄）",
"照片地址": "https://me.sjtu.edu.cn/upload/image/20191221/20191221072642.jpg",
"最高学历": "研究生",
"最高学位": "博士",
"职位": "制冷与低温工程研究所所长",
"办公地点": "上海市东川路800号 上海交大机械与动力工程学院A楼404室",
"科研论文": "Wang, Xueyang，Lin, Zhenhui，Gao, Jintong，Xu, Zhenyuan，Li, Xiuqiang*，Xu, Ning，Li, Jinlei，Song, Yan，Fu, Hanyu，Zhao, Wei，Wang, Shuaihao，Zhu, Bin，Wang, Ruzhu，Zhu, Jia*. Solar steam-driven membrane filtration for high flux water purification. Nat Water 1, 391–398 (2023). https://doi.org/10.1038/s44221-023-00059-8\nPrimož Poredoš and Ruzhu Wang. Sustainable cooling with water generation. Science 380,458-459(2023).DOI:10.1126/science.add1795\nShan, H., Poredoš, P., Ye, Z., Qu, H., Zhang, Y., Zhou, M., Wang, R., Tan, S. C., All-Day Multicyclic Atmospheric Water Harvesting Enabled by Polyelectrolyte Hydrogel with Hybrid Desorption Mode. Adv. Mater. 2023, 2302038. https://doi.org/10.1002/adma.202302038\nHao Zou, Chenxi Wang, Jiaqi Yu, Danfeng Huang*, Ronggui Yang*, Ruzhu Wang*, Eliminating greenhouse heat stress with transparent radiative cooling film, Cell Reports Physical Science, 2023, 101539, https://doi.org/10.1016/j.xcrp.2023.101539.，\nZhao Shao, Yu-Cheng Tang, Haotian Lv, Zhi-Shuo Wang, Primož Poredoš, Yaohui Feng, Ruikun Sun, Xi Feng, Zhihui Chen, Zhenxuan Gao, Dong-Dong Zhou*, Jie-Peng Zhang*, Ruzhu Wang*. High-performance solar-driven MOF AWH device with ultra-dense integrated modular design and reflux synthesis of Ni2Cl2(BTDD), Device, 2023, 100058, ttps://doi.org/10.1016/j.device.2023.100058.",
"源地址": "https://me.sjtu.edu.cn/teacher_directory1/wangruzhu.html"
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
