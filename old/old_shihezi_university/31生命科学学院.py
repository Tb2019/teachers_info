import re
from crawler import ReCrawler


school_id = 2
college_id = 31
start_urls = ['https://skxy.shzu.edu.cn/xyyjsdsjj/list{i}.htm'.format(i=i+1) for i in range(4)]

a_s_xpath_str = '//div[@portletmode="simpleList"]//table[@class="wp_article_list_table"]//a'
target_div_xpath_str = '//div[@class="wp_articlecontent"]'

directions_pattern_list = [
                            re.compile(r'研究内容(?::|：)?(.*?)\d.目前承担科研项目', re.S),
                            re.compile(r'研究内容(?::|：)?(.*?)\d.承担的科研项目', re.S),
                            re.compile(r'研究内容(?::|：)?(.*?)\d.主持承担科研项目', re.S),
                            re.compile(r'研究内容(?::|：)?(.*?)\d.近年承担科学教研项目', re.S),
                            re.compile(r'研究方向(?::|：)?(.*?)\d.主要研究内容', re.S),
                            re.compile(r'研究方向(?::|：)?(.*?)\w.主持项目', re.S),
                            re.compile(r'研究方向(?::|：)?(.*?)\w.个人介绍', re.S),
                            re.compile(r'研究方向(?::|：)?(.*?)\w.主持的科研项目', re.S),
                            re.compile(r'研究方向(?::|：)?(.*?)\w.主持或参与科研基金项目', re.S),
                            re.compile(r'研究方向(?::|：)?(.*?)\w.招生专业', re.S),
                            re.compile(r'研究方向(?::|：)?(.*?)\w.目前承担科研项目', re.S),
                            re.compile(r'研究内容(?::|：)?(.*?)\w.目前主持科研项目', re.S)
                          ]

abstracts_pattern_list = [
                            re.compile(r'^(.*?)学术简历', re.S),
                            re.compile(r'^(.*?)教育背景', re.S),

                            re.compile(r'基本情况(?::|：)?(.*?)\d.主要研究内容', re.S),
                            re.compile(r'照片(.*?)\d.主要研究方向', re.S),
                            re.compile(r'^(.*?)\d.学习和工作经历', re.S),
                            re.compile(r'^(.*?)\d.科研与学术', re.S),
                            re.compile(r'^(.*?)\w.工作经历', re.S),
                            re.compile(r'^(.*?)\w.主要成果', re.S),
                            re.compile(r'^(.*?)目前承担科研项目', re.S),
                            re.compile(r'基本情况(?::|：)?(.*?)\d.研究项目', re.S),
                            re.compile(r'基本情况(?::|：)?(.*?)目前承担科研项目', re.S),
                            re.compile(r'^(.*?)电子邮箱', re.S)
                         ]

responsibilities_pattern_list = [
                                    re.compile(r'学术兼职(?::|：)?(.*?)教育背景'),
                                    re.compile(r'学术兼职(?::|：)?(.*?)主讲课程')
                                ]

office_address_pattern_list = [
                                re.compile(r'通讯地址(?::|：)?(.*?)\d.邮编')
                              ]

spider = ReCrawler(school_id=school_id,
                   college_id=college_id,
                   name_filter_re=r'导师简介',
                   start_urls=start_urls,
                   a_s_xpath_str=a_s_xpath_str,
                   target_div_xpath_str=target_div_xpath_str,
                   directions_pattern_list=directions_pattern_list,
                   abstracts_pattern_list=abstracts_pattern_list,
                   office_address_pattern_list=office_address_pattern_list,
                   responsibilities_pattern_list=responsibilities_pattern_list,
                   save2target=True
                   )

spider.run()


