import re
from crawler import ReCrawler


school_id = 2
college_id = 32
start_urls = ['https://sem.shzu.edu.cn/szdw/list.htm']

a_s_xpath_str = '//div[@frag="面板8"]//table//li//span//a'
target_div_xpath_str = '//div[@class="wp_articlecontent"]'

directions_pattern_list = [
                            re.compile(r'研究方向(?::|：)?(.*?)(?:（|\()\w(?:）|\))', re.S),
                            re.compile(r'研究内容(?::|：)?(.*?)\w.主持科研项目', re.S),
                            re.compile(r'研究内容(?::|：)?(.*?)\w.承担(?:的主要)??科研项目', re.S),
                            re.compile(r'研究内容(?::|：)?(.*?)\w.目前承担', re.S),
                            re.compile(r'研究内容(?::|：)?(.*?)\w.\w*?代表性科研成果', re.S),
                            re.compile(r'研究内容(?::|：)?(.*?)\w*?代表性科研成果', re.S),
                            re.compile(r'主要研究领域与业绩(?::|：)?(.*?)\d.目前承担科研项目'),
                            re.compile(r'研究内容(?::|：)?(.*?)\d.讲授课程'),
                            re.compile(r'研究内容(?::|：)?(.*?)\d.联系方式'),
                            re.compile(r'研究内容(?::|：)?(.*?)近年代表性科研成果'),
                            re.compile(r'研究方向(?::|：)?(.*?)科研项目'),
                          ]

abstracts_pattern_list = [

                            re.compile(r'基本情况(?::|：)?(.*?)(?:（|\()\w(?:）|\))主要研究', re.S),
                            re.compile(r'基本情况(?::|：)?(.*?)(\w.)?主要研究', re.S),
                            re.compile(r'基本情况(?::|：)?(.*?)\w.联系方式', re.S),
                            re.compile(r'基本情况(?::|：)?(.*?)\w.工作简历', re.S),

                            re.compile(r'^(.*?)(?:学术简历|教育经历|教育背景|工作经历)', re.S),
                         ]

responsibilities_pattern_list = [
                                    re.compile(r'学术兼职(?::|：)?(.*?)教育背景', re.S),
                                    re.compile(r'学术和社会兼职(.*?)\w.获得的荣誉')
                                ]

office_address_pattern_list = [
                                re.compile(r'通讯地址(?::|：)?(.*?)邮政编码', re.S)
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


