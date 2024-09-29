# -*- coding: utf-8 -*-
# 数据提取完毕 入库失败时使用。或者
import csv
import os
from asyncio.log import logger
from utils import csv_2_df, truncate_table, df2mysql, drop_duplicate_collage, local_engine, sf_engine, save_as_json
from urllib import parse

school_id = 104
college_id = 251
school_name = '上海交通大学'
college_name = '医学院'

img_url_head = ''

data_real = {
"姓名": "谢幼专",
"电话": "",
"邮箱": "phoque711@163.com",
"职称": "",
"个人简介": "",
"教育经历": "",
"工作经历": "",
"研究方向": "脊柱外科，生物材料，组织工程，骨质疏松，脊柱康复",
"人才称号": "",
"行政称号": "",
"专利": "",
"科研项目": "",
"荣誉/获奖": "内镜手术联合富血小板血浆治疗腰椎间盘突出症\n老年常见骨关节疾病综合康复体系研究\n可控释β-磷酸三钙抗生素缓释系统的试制及 其缓释规律的研究\n抗结核生物陶瓷仿生人工椎体的构建及其生物学特性研究\n利用原位诱导包膜促进大段骨缺损修复的研究",
"照片地址": "https://daoshi.shsmu.edu.cn/Telerik.Web.UI.WebResource.axd?imgid=94bc7d1dd57f4b918568d1f7bd61bf58&type=rbi",
"最高学历": "",
"最高学位": "",
"职位": "硕士生导师",
"办公地点": "上海市制造局路639号7号楼13楼上海交通大学医学院附属第九人民医院骨科",
"科研论文": "A novel biocompatible PDA/IR820/DAP coating for antibiotic/photodynamic/photothermal triple therapy to inhibit and eliminate Staphylococcus aureus biofilm.Junkai Zeng, Yitong Wang, Zhenyu Sun,Haishuang Chang, Mi Cao, Jie Zhao,Kaili Lin, Youzhuan Xie （通讯作者）.Chemical Engineering Journal 2020\nOsteoblastic and anti-osteoclastic activities of strontium-substituted silicocarnotite ceramics: In vitro and in vivo studies.Junkai Zeng, Jingshu Guo, Zhenyu Sun, Fanyan Deng, Congqin Ning, Youzhuan Xie （通讯作者）.Bioactive materials 2020.\nNanosized-Ag-doped porous β-tricalcium phosphate for biological applications.Junjie Yuan, Baoxin Wang, Chen Han, Xiaoyan Huang, Haijun Xiao, Xiao Lu, Jianxi Lu, Dong Zhang, Feng Xue,Youzhuan Xie （通讯作者）.	Materials Science & Engineering C 2020 ",
"源地址": "https://daoshi.shsmu.edu.cn/Pages/TeacherInformationView.aspx?uid=EE784F55-5362-4A67-A81C-4DDC2DF79D11&from=s&pId=all&tId="
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
