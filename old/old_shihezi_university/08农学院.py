import re
from crawler import ReCrawler


school_id = 2
college_id = 8
start_urls = ['https://nxy.shzu.edu.cn/jsml/list.htm']
a_s_xpath_str = '//div[@id="wp_content_w6_0"]//p[@class="teacher_new"]//a'
target_div_xpath_str = '//div[@portletmode="simpleArticleAttri"]'

directions_pattern_list = [
                            re.compile(r'研究方向(?::|：)?(.*?)(?=个人简介)', re.S),
                            re.compile(r'研究方向(?::|：)?(.*?)(?=一、工作简历)', re.S),
                            re.compile(r'研究领域(?::|：)?(.*?)(?=主持)')
                          ]

abstracts_pattern_list = [
                            re.compile(r'个人简介(.*?)(?=一、教学情况)')
                         ]

office_address_pattern_list = [
                                re.compile(r'办公室(?::|：)(.*?)(?=(?:E-|e-|E\.|e\.)??mai)')
                              ]

spider = ReCrawler(school_id=school_id,
                   college_id=college_id,
                   start_urls=start_urls,
                   a_s_xpath_str=a_s_xpath_str,
                   target_div_xpath_str=target_div_xpath_str,
                   directions_pattern_list=directions_pattern_list,
                   abstracts_pattern_list=abstracts_pattern_list,
                   office_address_pattern_list=office_address_pattern_list,
                   save2target=True
                   )

spider.run()
