import scrapy
import re
from lxml import etree
from urllib.parse import urljoin
from old_shihezi_university.items import TeacherItem


class HuaxuehuagongSpider(scrapy.Spider):
    name = "01huaxuehuagong"
    allowed_domains = ["hgxy.shzu.edu.cn"]
    start_urls = ["https://hgxy.shzu.edu.cn/jsml/list.psp"]

    def parse(self, resp, **kwargs):
        href_pattern = re.compile(r'^https.*?page\.htm$', re.S)
        a_s = resp.xpath('//div[@id="wp_content_w107_0"]/table//td/a')
        for a in a_s:
            name = a.xpath('.//text()').extract_first()
            # a.xpath('./span/text()').extract_first() if a.xpath('./span') else a.xpath('./text()').extract_first()
            href = a.xpath('./@href').extract_first()
            if not href_pattern.match(href):
                continue
            request_ = scrapy.Request(url=href, callback=self.parse_detail)
            request_.name = name
            yield request_
            # break

    def parse_detail(self, resp, **kwargs):
        item = TeacherItem()

        # 姓名
        name = re.sub(r'\s?\xa0\s?', '', resp.name)
        # print(name)

        page = etree.HTML(resp.text)
        all_content_sep = ''.join([content.strip() + ';' for content in page.xpath('//div[@frag="窗口107"]//text()')])
        all_content = ''.join([content.strip() for content in page.xpath('//div[@frag="窗口107"]//text()')])

        # print(all_content_sep)

        # 职称
        job_title_pattern = re.compile('职称：;?(.*?);')
        try:
            job_title = job_title_pattern.findall(all_content_sep)[0]
        except:
            job_title = resp.selector.re('讲师|副教授|教授')[0]
        # print(job_title)

        # 研究方向
        direction_pattern = re.compile(r'(?:研究|科研);?方向;?(?:：|:)?;{0,2}(.*?;)(?=(?:.{1,6}(?:：|:))|个人简介|教育工作经历)', re.S)
        direction = direction_pattern.findall(all_content_sep)[0].replace(';', '')
        # print(direction)

        # 图片
        try:
            picture_url = page.xpath('//div[@frag="窗口107"]//img/@src')[0]
            picture = urljoin(resp.url, picture_url)
        except:
            picture = None
        # print(picture)

        # 电话
        try:
            phone_pattern = re.compile(r'电话(?:：|:)(\d{11})|(\d{4}-\d{7})', re.S)
            phone = phone_pattern.findall(all_content_sep)[0]
            p_1, p_2 = phone
            if p_1:
                phone = p_1
            else:
                phone = p_2
        except:
            phone = None
        # print(phone)

        # 邮箱
        try:
            # email_pattern = re.compile(r'邮箱(?:：|:);?([0-9a-zA-Z._-]+;?@;?[0-9a-zA-Z._-]+;?\.[0-9a-zA-Z._-])', re.S)
            email_pattern = re.compile(
                r'(?:邮箱|E-mail)(?:：|:)([0-9a-zA-Z._-]+\s?@[0-9a-zA-Z._-]+\.[0-9a-zA-Z._-]+)', re.S
            )
            email = list(set(email_pattern.findall(all_content)))[0]
        except:
            email = None
        # print(name)
        # print(email)

        # 学位、学历
        try:
            qualification_pattern = re.compile(r'博士|硕士|学士')
            qualification = qualification_pattern.findall(all_content)[0]
            if qualification == '学士':
                education = '本科'
            else:
                education = '研究生'
        except:
            qualification = None
            education = None
        # print(name, qualification, education)

        # 个人简介
        try:
            abstracts_pattern = re.compile(
                r'个人简介(?:：|:)?(.*?)(?=科研项目(?:：|:)?|代表性论文(?:：|:)?|研究方向(?:：|:)?)', re.S
            )
            abstracts = abstracts_pattern.findall(all_content)[0]
        except:
            abstracts = None
        # print(name, abstracts)

        # 办公地点
        try:
            communi_address_pattern = re.compile(r'(?<!实验室)地址(?:：|:);?(.*?);')
            communi_address = communi_address_pattern.findall(all_content_sep)[0].replace(';', '')
        except:
            communi_address = None
        try:
            lib_address_pattern = re.compile(r'实验室地址(?:：|:);?(.*?);')
            lib_address = lib_address_pattern.findall(all_content_sep)[0].replace(';', '')
        except:
            lib_address = None

        office_address = None
        if communi_address and lib_address:
            office_address = communi_address + ';' + lib_address
        elif communi_address:
            office_address = communi_address
        else:
            office_address = lib_address
        # print(name, office_address)

        # 在职信息
        job_information = 1

        # 主要任职
        responsibilities = None
        item['name'] = name
        item['school_id'] = 2
        item['college_id'] = 1
        item['job_title'] = job_title
        item['directions'] = direction
        item['picture'] = picture
        item['phone'] = phone
        item['email'] = email
        item['education'] = education
        item['qualification'] = qualification
        item['job_information'] = job_information
        item['responsibilities'] = responsibilities
        item['abstracts'] = abstracts
        item['office_address'] = office_address

        yield item
