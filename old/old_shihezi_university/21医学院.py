import re
from crawler import ReCrawler


school_id = 2
college_id = 21
start_urls = ['https://yixy.shzu.edu.cn/dsjj_yjs/list{i}.htm'.format(i=i+1) for i in range(26)]

a_s_xpath_str = '//div[@id="wp_news_w6"]//a'
target_div_xpath_str = '//div[@portletmode="simpleArticleTitle"]'

directions_pattern_list = [
                            re.compile(r'研究领域(?::|：)?(.*?)邮箱'),
                            re.compile(r'研究(?:方向|内容)(?::|：)?(.*?)。')
                            # re.compile(r'研究方向(?::|：)?(.*?)(?=个人简介)', re.S),
                            # re.compile(r'研究方向(?::|：)?(.*?)(?=一、工作简历)', re.S),
                            # re.compile(r'研究领域(?::|：)?(.*?)(?=主持)')
                          ]

abstracts_pattern_list = [
                            re.compile(r'科研学术工作经历与教育背景(?::|：)?(.*?)科研项目'),
                            re.compile(r'基本情况(?::|：)?(.*?)\(\d\)学术论文'),
                            re.compile(r'基本情况(?::|：)?(.*?)(?:\d.?)?主要研究内容'),
                            re.compile(r'基本情况(?::|：)?(.*?)联系方式'),
                         ]

responsibilities_pattern_list = [
                                    re.compile(r'学术兼职情况(?::|：)?(.*?)八、基本情况')
]

office_address_pattern_list = [
                                re.compile(r'通讯地址(?::|：)?(.*?)学术兼职')
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


