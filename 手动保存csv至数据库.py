# -*- coding: utf-8 -*-
# 数据提取完毕 入库失败时使用。或者
import csv
import os
from asyncio.log import logger
from utils import csv_2_df, truncate_table, df2mysql, drop_duplicate_collage, local_engine, sf_engine, save_as_json
from urllib import parse

school_id = 110
college_id = 5
school_name = '哈尔滨工业大学'
college_name = '电气工程及自动化学院'

img_url_head = ''

data_real = {
"姓名": "聂秋月",
"电话": "18945092312",
"邮箱": "nieqiuyue@hit.edu.cn,nieqiu@sina.com",
"职称": "教授",
"个人简介": "聂秋月，哈尔滨工业大学电气工程及自动化学院，教授，博士生导师，IEEE高级会员，国家自然科学基金优秀青年基金获得者，入选哈尔滨工业大学青年拔尖人才、青年科学家工作室学术带头人。主要从事等离子体产生及参数调控技术、等离子体调制电磁波特性研究及应用研究。作为负责人主持国家“863”计划预研项目1项、国家重点研发计划课题1项、国家“973”计划项目专题1项、国家自然科学基金6项（重点项目1项、优青1项、面上2项、青年1项、专项1项）、省/部级项目和国家重点实验室开放课题3项；并担任国家重大科技基础设施（国家大科学工程）“空间环境地面模拟装置”主管设计师，全面负责临近空间等离子体环境地面模拟与研究平台建设工作。发表学术论文70余篇，累计SCI引用500余次；应邀做国际/国内会议特邀报告21次，主持专刊1项，授权国家发明专利24项，获辽宁省优秀博士学位论文奖、清华大学实验技术成果奖二等奖（排名第二）、2019年黑龙江省高校科学技术奖一等奖（第一完成人）。\n当选中国电工技术学会第九届理事会青年工作委员会副主任委员、中国电工技术学会等离子体及应用专业委员会委员、中国力学学会等离子体科学与技术专委会低温等离子体专业组副组长、IEEE senior member；任“全国高电压与放电等离子体学术会议”2018年大会副主席、2020年大会主席、2020年ICOPS空间等离子体专题召集人；CPL/CPB/物理学报青年编委、《哈尔滨工业大学学报》编委、PST客座编辑等。",
"研究方向": "",
"人才称号": "",
"行政称号": "",
"专利": "一种适用于单、双频驱动大气压介质阻挡弥散放电电学特性等效电路及其计算方法,ZL202110372586.4\n一种等离子体包覆双齿形结构的可调带阻滤波器,ZL202210017317.0\n一种多通道电弧等离子体源级联铜片水冷装置及其优化方法,ZL202110942578.9\n一种临近空间等离子体环境地面模拟装置及其模拟方法,ZL202111191959.4\n一种适用于穿舱结构的宽频段小型化天线阵列吊装机构,ZL202111086438.2",
"科研项目": "国家自然科学基金重大研究计划重点支持项目,92271202, 跨域复杂电磁环境感知与自适应信息传输关键技术研究，2023-01至2026-12，300万，在研，主持\n国家自然科学基金优秀青年科学基金项目，52022026，等离子体调控电磁波基础理论及应用技术，2021-01至2023-12，120万，在研，主持\n国家自然科学基金专项项目，11942513，第三届（2020年）全国高电压与放电等离子体学术会议，2020-01至2020-07，15万元，在研，主持\n国家自然科学基金面上项目，11875118 ，亚波长等离子体结构调制增强微波电磁辐射特性及机理研究，2019-01至2022-12，66万元，在研，主持\n国家重点研发计划项目课题，2018YFE0303105，高热负荷条件下偏滤器材料与部件行为研究，2018-12至2023-11，547万元，在研，主持",
"荣誉/获奖": "清华大学实验技术成果奖二等奖（排名第二）\n哈尔滨工业大学青年拔尖人才计划\n2016-2017年度哈尔滨工业大学优秀专兼职学生工作者\n哈尔滨工业大学优秀硕士论文指导教师\n黑龙江省高校科学技术奖一等奖（排名第一）\n哈尔滨工业大学本科生优秀毕业设计指导教师\n中国电工技术学会优秀会员",
"照片地址": "http://homepage.hit.edu.cn/file/showHP.do?d=1972&&w=200&&h=204&&1723528729053",
"最高学历": "研究生",
"最高学位": "博士",
"职位": "中国电工技术学会等离子体及应用专业委员会委员。\n中国电工技术学会第八届理事会青年工作委员会委员。\n中国电工技术学会第九届理事会青年工作委员会副主任委员。\n中国力学学会等离子体科学与技术专委会低温等离子体专业组副组长\nIEEE Senior Member。\n2016年“全国高电压与放电等离子体学术会议”技术委员会委员；2018年该会议副主席，2020年大会主席。\nThe 47th IEEE International Conference on Plasma Science（ICOPS，2020）空间等离子体专题召集人。\n2022年第20届“全国等离子体科学技术会议”共同执行主席。\n2022年第二届全国直线等离子体装置研讨会共同主席。\n哈尔滨工业大学学报期刊编委、PST期刊编委\nChinese Physics Letters (CPL)、Chinese Physics B (CPB)、《物理学报》和《物理》四刊联合青年编委；\nIEEE ACCESS、Physics of Plasmas、IEEE Transactions on plasma science、Journal of Applied Physics、Plasma science and technology、Chinese Physic B 、 物理学报 、高电压技术、 电工技术学报、中国科学：物理学 力学 天文学等期刊审稿人；",
"办公地点": "哈尔滨市南岗区一匡街2号哈工大科学园C2栋402室",
"科研论文": "Self-organized pattern formation of an atmospheric pressure plasma jet in a dielectric barrier discharge configuration;Nie, Qiu-Yue; Ren, Chun-Sheng; Wang, De-Zhen; Li, Shou-Zhe;Zhang, Jia-Liang;Kong, M. G;2007;Applied Physics Letters;90(22)：221504\nA simple cold Ar plasma jet generated with a floating electrode at atmospheric pressure;Nie, Qiu-Yue; Ren, Chun-Sheng ; Wang, De-Zhen ; Zhang, Jia-Liang;2008;Applied Physics Letters;93(1)：011503\nOnline diagnosis of electron excitation temperature in CH4+H-2 discharge plasma at atmospheric pressure by optical emission spectra;Cui JinHua ; Xu ZhenFeng ; Zhang JiaLiang ; Nie QiuYue ; Xu GenHui ; Ren LongLiang;2008;SCIENCE IN CHINA SERIES G-PHYSICS MECHANICS & ASTRONOMY;51(12)：1892-1896\nElectron dynamics and metastable species generation in atmospheric pressure non-equilibrium plasmas controlled by dual LF-RF frequency discharges;Yilin Yu1, Zhonglin Zhang *, Qiuyue Nie ,Jiacheng Zeng, Zhibo Zhao1 and Xiaogang Wang;2023;FRONTIERS IN PHYSICS;11：113725\nInvestigation on the near-field cutoff effect in a subwavelength plasma shell with near-zero permittivity;Peiqi Chen , 1 Qiuyue Nie,1,2,* Shu Lin,3 Liang Qian,4 Zhonglin Zhang , 2 Xiaogang Wang,2,4 Zhuotao Meng,1 and Guoqiang Wei4;2023;PHYSICAL REVIEW E;107, 065204",
"源地址": "http://homepage.hit.edu.cn/nieqiuyue"
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
