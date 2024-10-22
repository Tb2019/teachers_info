# -*- coding: utf-8 -*-
# 数据提取完毕 入库失败时使用。或者
import csv
import os
from asyncio.log import logger
from utils import csv_2_df, truncate_table, df2mysql, drop_duplicate_collage, local_engine, sf_engine, save_as_json
from urllib import parse

school_id = 90
college_id = 444
school_name = '电子科技大学(dp)'
college_name = '电子科技大学重庆微电子产业技术研究院'

img_url_head = ''

data_real = {
"姓名": "张文旭",
"电话": "028-61831506",
"邮箱": "xwzhang@uestc.edu.cn",
"职称": "副教授",
"个人简介": "",
"教育经历": "Sept.1995~July 1999, Electronic Material and Device at UESTC，\n1995年9月~1999年7月：磁性材料 专业，本科，信息材料工程学院，电子科技大学\nSept.1999~Apr 2002, Material Physics and Chemistry at UESTC，\n1999年9月~2002年4月：材料物理与化学 专业，硕士，导师：杨仕清 教授，微电子与固体电子学院，电子科技大学\nFeb.2003~June,2004, Tongji Univ. German courses，\n2003年2月~2004年6月：德语培训，同济大学\nSept.2004~July, 2008, theoretical physics under Prof. Helmut Eschrig, at TU Dresden，\n2004年9月~2008年7月：理论物理 专业，博士，Dresden工业大学，德国",
"工作经历": "2014年7月~8月， 丹麦工业大学，访问研究\n2011年8月~今 ，电子科技大学，副教授\n2008年8月~2011年7月，电子科技大学，讲师\n2002年4月~2008年7月，电子科技大学，助教\nApr. 2002- July. 2008, Teaching assistant at UESTC, Chengdu, China\nAug. 2008~July, 2011, Lecturer at UESTC, Chengdu, China\nAug. 2011~now Associate Professor at UESTC\nJuly. 2014~Aug. 2014, Visiting scienctists, Denmark Technical University",
"研究方向": "1. Electronic structure and magnetism by density functional theory （Main direction）材料的电子结构，输运特性及磁性能等第一性原理计算\n2. Micromagnetic simulations (experienced)微磁学模拟\n3. Magnetic thin films, esp. magnetoresistance thin films and ferrites for microwave devices",
"人才称号": "",
"行政称号": "",
"专利": "",
"科研项目": "",
"荣誉/获奖": "",
"照片地址": "https://cq.uestc.edu.cn/__local/6/E5/D8/AFA378EE20C7E59AA2218FAFB2C_CEA5944B_C50A.jpg",
"最高学历": "研究生",
"最高学位": "博士",
"职位": "教授",
"办公地点": "",
"科研论文": "[36]Qiuru Wang,Wenxu Zhang*, Bin Peng, and Wanli Zhang, Inverse spin Hall effects in Nd doped SrTiO3,AIP ADVANCES7, 125218 (2017), https://doi.org/10.1063/1.4986324\n[35]Wenxu Zhang*, Jiantao Qin, Zhishuo Huang, Wanli Zhang, THE MECHANISM OF LAYER NUMBER AND STRAIN DEPENDENT BANDGAP OF 2D CRYSTAL PtSe2,J. Appl. Phys., 122, 205701 (2017) https://doi.org/10.1063/1.5000419\n[34]Qiuru Wang,Wenxu Zhang*,Bin Peng, Huizhong Zeng, and Wanli Zhang, Spin to charge conversion at the conducting TiO2surface,Phys. Status Solidi RRL,1700149 (2017), https://doi.org/10.1002/pssr.201700149\n[33]Wenxu Zhang*, Qiuru Wang, Bin Peng, Huizhong Zeng, Wee Tee Soh, Chong Kim Ong, and Wanli Zhang, Spin galvanic effect at the conducting SrTiO3surfaces,Appl. Phys. Lett.. 109, 262402 (2016); doi: 10.1063/1.4973479\n[32]Wenxu Zhang*, Ting Wu, Bin Peng, Wanli Zhang, Resistivity dependence of the spin mixing conductance and the anisotropic magnetoresistance in permalloy,Journal of Alloys and Compounds696 (2017) 234-238; DOI:/10.1016/j.jallcom.2016.11.274",
"源地址": "https://cq.uestc.edu.cn/info/1115/1629.htm"
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
