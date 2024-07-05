# -*- coding: utf-8 -*-
# 数据提取完毕 入库失败时使用。或者
import csv
import os
from asyncio.log import logger
from utils import csv_2_df, truncate_table, df2mysql, drop_duplicate_collage, local_engine, sf_engine, save_as_json
from urllib import parse

school_id = 106
college_id = 2
school_name = '清华大学'
college_name = '土木水利学院'

img_url_head = ''

data_real = {
"姓名": "朱颖心",
"电话": "010-62782746",
"邮箱": "zhuyx@mail.tsinghua.edu.cn",
"职称": "教授",
"个人简介": "   ",
"研究方向": "可持续建筑与建筑节能研究\n人体热舒适理论研究",
"人才称号": "",
"行政称号": "",
"专利": "",
"科研项目": "[1]      国家自然科学基金面上项目52178079，\"热环境对睡眠热舒适影响的关键问题研究\"，2022.1-2025.12，负责人。\n[2]      国家自然科学基金面上项目51678330，\"建筑环境适应性热舒适的机理研究\"，2017.1-2020.12，负责人。\n[3]      国家重点研发计划课题2018YFC0705003，\"地下交通建筑节能关键技术与设备开发\"，2018.7~2021.6，负责人\n[4]      国际能源署-建筑与社区节能国际合作项目：IEA-EBC Annex 69: Strategy and Practice of Adaptive Thermal Comfort in Low Energy Buildings（适应性热舒适在低能耗建筑中的应用策略与实践），2015.1- 2021.12，负责人\n[5]      国家“十二五”科技支撑计划课题 2014BAJ04B03，“大型航站楼绿色建筑关键技术研究与示范”，2014.1-2017.12，负责人\n[6]      973项目子课题 2012CB720104-2，座舱热舒适设计参数优化，2012.1-2016.9，负责人\n[7]      国家自然科学基金重点项目 50838003，动态热环境与人体热舒适的基础研究，2009.1-2012.12，负责人\n[8]      国家“十一五”科技支撑计划课题 2006BAJ01A01，“建筑节能设计方法与模拟分析软件开发”，2006.9-2010.12，负责人",
"荣誉/获奖": "[1]      2020年 吴元炜暖通空调奖，中国建筑学会暖通空调分会\n[2]      2018年度 清华大学教学优秀奖\n[3]      2018年 井上宇市亚洲国际奖，日本“空气调和×卫生工学”学会\n[4]      2013年 清华大学“教书育人”奖\n[5]      2012年 清华大学优秀博士学位论文指导教师\n[6]      2008年度 北京市高等学校教学名师，2008年6月24日，北京市教委\n[7]      2007年度 宝钢教育基金会优秀教师奖\n[8]      2003年 清华大学“教书育人”奖\n[9]      2003年 清华大学“良师益友”奖\n[10]   1997年度 北京市优秀教师",
"照片地址": "http://www.arch.tsinghua.edu.cn/upload_files/image/1650584695821_9A.png",
"最高学历": "研究生",
"最高学位": "博士",
"职位": "教授",
"办公地点": "中国北京海淀区 清华大学建筑学院建筑技术科学系（清华大学二校门东北侧 旧土木工程馆219室）",
"科研论文": "[1]     Jia Xinyu, Cao Bin, Zhu Yingxin. A Climate Chamber Study on Subjective and Physiological Responses of Airport Passengers from Walking to a Sedentary Status in Summer. Building and Environment, 207(2022) 108547.\n[2]     Huang Yenhsiang, Jia Xinyu, Zhu Yingxin, Zhang Deyin, Lin Borong. Research on indoor spaces and passenger satisfaction with terminal buildings in China, Journal of Building Engineering, 43(2021) 102873\n[3]     Wang Zihan, Cao Bin, Zhu Yingxin. Questionnaire survey and field investigation on sleep thermal comfort and behavioral adjustments in bedrooms of Chinese residents. Energy and Buildings, 2021, 253: 111462.\n[4]     Jia Xinyu, Huang Yenhsiang, Cao Bin, Yingxin Zhu, Wang Chunqing. Field Investigation on Thermal Comfort of Passengers in an Airport Terminal in the Severe Cold Zone of China. Building and Environment, 2021, 189: 107514.\n[5]     Xinyu Jia, Bin Cao, Yingxin Zhu, Yenhsiang Huang. Field Studies on Thermal Comfort of Passengers in Airport Terminals and High-Speed Railway Stations in Summer. Building and Environment, 2021, 206: 108319",
"源地址": "http://www.arch.tsinghua.edu.cn/info/rw_jzhj/1476"
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
