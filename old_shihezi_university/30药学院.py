import re
from crawler import ReCrawler


school_id = 2
college_id = 30
start_urls = ['https://yaoxy.shzu.edu.cn/sssds/list{i}.htm'.format(i=i+1) for i in range(6)]

a_s_xpath_str = '//div[@portletmode="simpleColumnAttri"]//div[@class="right-iteam"]//a'
target_div_xpath_str = '//div[@class="displayinfo_pc"]'

# directions_pattern_list = [
#                             re.compile(r'研究领域(?::|：)?(.*?)邮箱'),
#                             re.compile(r'研究(?:方向|内容)(?::|：)?(.*?)。')
#                           ]

abstracts_pattern_list = [
                            re.compile(r'基本信息(?::|：)?(.*?)二、'),
                         ]

# responsibilities_pattern_list = [
#                                     re.compile(r'学术兼职情况(?::|：)?(.*?)八、基本情况')
# ]

office_address_pattern_list = [
                                re.compile(r'通讯地址(?::|：)?(.*?)\d.邮编')
                              ]

spider = ReCrawler(school_id=school_id,
                   college_id=college_id,
                   school_name='02石河子大学',
                   college_name='药学院',
                   name_filter_re=r'\s导师简介|硕士生导师',
                   start_urls=start_urls,
                   a_s_xpath_str=a_s_xpath_str,
                   target_div_xpath_str=target_div_xpath_str,
                   # directions_pattern_list=directions_pattern_list,
                   abstracts_pattern_list=abstracts_pattern_list,
                   office_address_pattern_list=office_address_pattern_list,
                   # responsibilities_pattern_list=responsibilities_pattern_list,
                   save2target='no'
                   )

spider.run()


