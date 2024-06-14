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
"姓名":"冯文杰",
"电话":"",
"邮箱":"eewjfeng@scut.edu.cn",
"职称":"教授",
"个人简介":"冯文杰：男, 1985年1月生，2013年10月毕业于南京理工大学，获工学博士学位，现为华南理工大学电信学院教授，博士生导师，国家优青(2018)，广东省毫米波太赫兹重点实验室副主任，曾任电磁仿真与射频感知工信部重点实验室副主任。主要研究领域为微波/毫米波电路与器件。曾获得2015年“江苏省科学技术二等奖”、2021年中国电子学会科技进步二等奖、2017年江苏省“青蓝工程”优秀青年骨干教师、2018年ACES-China青年科学家奖等。\n主持国家及省部级等项目共计10余项。在国际期刊和会议上发表论文200余篇，其中SCI收录IEEE期刊论文110余篇 (IEEE Transactions论文80余篇)，论文引用5000余次。受邀合作编写英文书籍的一章 , 获授权国家发明专利30余项。目前担任多个SCI期刊的副主编。已培养江苏省优秀硕士论文2名，获国内外学术会议最佳学生论文奖4项。",
"研究方向":"微波毫米波集成电路、天线理论与技术、电路封装等",
"专利":"[1] 一种高效率滤波天线阵列及通信设备，发明专利，2021.12.14授权， 发明人：冯文杰，程俊淇，施永荣，倪啸宇，伍文斌，车文荃，薛泉，专利号：ZL202111118032.8\n[2] 基于180°理想反相器的三频平衡式耦合器,发明专利，2021.2.12授权， 发明人：冯文杰，赵宇，车文荃，陈海东，尹蕊，商玉霞，专利号：ZL 201710736136.2\n[3] 基于SSPPs的四端口差分结构，发明专利，2021.3.2授权，发明人：冯文杰，冯炎皓，段茜文，袁淼，郭璐，专利号：ZL201910377061.2\n[4] 基于脊间隙波导的毫米波高增益高辐射效率槽天线阵列，发明专利，2021.5.4授权，发明人：冯文杰，倪啸宇，施永荣，郭璐，沈瑞亮，王慧，专利号：ZL202110114394.3\n[5] 一种紧凑高增益双极化差分滤波天线，发明专利，2020.5.22授权，发明人：冯文杰，荀孟祝，杨琬琛，车文荃，陈思，孟倩，专利号：ZL201811327158.4",
"科研项目":"1. 国家自然科学基金重点项目（62231014）：多功能集成封装的微波毫米波无源器件与电路，2023.1-2027.12，在研，项目负责人\n2. 国家重点研发计划“6G高密度射频前端技术”专项课题（2020YFB1807405）：高密度射频芯片与天线封装互连技术，2020.12-2023.11, 在研，项目负责人\n3. 国家自然科学基金优秀青年科学基金项目（61822110）：微波电路与器件-可重构微波电路与器件的理论和技术研究，2019.1-2021.12, 结题，项目负责人\n4. 国家自然科学基金青年基金项目（61401206）：基于LTCC的宽带及平衡式滤波电路的设计方法与应用研究，2015.1-2017.12, 结题，项目负责人\n5. 江苏省自然科学基金青年基金项目（BK20140791）：新型宽带LTCC滤波电路的设计方法与应用研究，2014.7-2017.6, 结题，项目负责人\n6. 装备发展部预先研究项目（61404130407）：新型太赫兹天线技术，2019.1-2020.12, 结题，项目负责人\n7. 校企合作基金项目（61971387）：W波段基板封装与电路集成技术，2020.1-2021.6，结题，项目负责人\n8. 中国航天科技集团有限公司第八研究院，横向项目，校准天线阵列采购，2022.1.-2022.6,结题，项目负责人\n9. 中国航天科技集团有限公司第八研究院，产学研合作基金， 面向相控阵集成应用的新型三维复杂网络理论与技术研究，2021.1-2022.12，项目负责人；\n10. 中国人民解放军****, 横向项目, 0.15um工艺GaN微波集成电路技术, 2022-01 至2024-06, 在研, 项目负责人",
"荣誉/获奖":"2018.08  2018年国家优秀青年科学基金获得者\n2016.02  2015年江苏省科技进步二等奖\n2021.12  2021年中国电子学会科技进步二等奖\n2017.05  2017 年江苏省 “青蓝工程”优秀青年骨干教师\n2015.09  2015 年江苏省优秀博士论文\n2017.12  2017年中国电子教育学会首届优秀博士学位论文提名奖\n2018.07  ACES-China 2018青年科学家奖",
"照片地址":"https://yanzhao.scut.edu.cn/public/GetPhotoFile.aspx?file=iPEeevCNsCC!B844T52NgSMXw4wrATfPzFDDOX9CTKyWZTw2FjIIXvcG7D5La9hU",
"最高学历":"研究生",
"最高学位":"博士",
"职位":"教授",
"办公地点":"广州市天河区五山路381号电子与信息学院",
"科研论文":"[1] Wenjie Feng, Quan Xue and Wenquan Che, “Compact Planar Magic-T Based on the Double-Sided Parallel-Strip Line and the Slotline Coupling,” IEEE Transactions on Microwave Theory and Techniques, vol. 58, no. 11, pp. 2915–2923, Nov. 2010.\n[2] Wenjie Feng, Wenquan Che, “Novel Wideband Differential Bandpass Filters Based on T-Shaped Structure,” IEEE Transactions on Microwave Theory and Techniques, vol. 60, no. 6, pp. 1560–1568, Jun. 2012.\n[3] Wenjie Feng, Wenquan Che, Yumei Chang, Suyang Shi and Quan Xue, “High Selectivity Fifth-Order Wideband Bandpass Filters With Multiple Transmission Zeros Based on Transversal Signal-Interaction Concepts,” IEEE Transactions on Microwave Theory and Techniques, vol. 61, no. 1, pp. 89–97, Jan. 2013.  \n[4] Wenjie Feng, Haotian Zhu, Wenquan Che, Quan Xue, “Wideband In-Phase and Out-of-Phase Balanced Power Dividing and Combining Networks”, IEEE Transactions on Microwave Theory and Techniques, vol. 62, no. 5, pp. 1192–1202, May 2014.\n[5] Wenjie Feng, Chaoying Zhao, Wenquan Che, Quan Xue, “Wideband Balanced Network with High Isolation Using Double-Sided Parallel-Strip Line”, IEEE Transactions on Microwave Theory and Techniques, vol. 63, no. 12, pp. 4113–4118, Dec. 2015."
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
