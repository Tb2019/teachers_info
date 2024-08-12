# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TeacherItem(scrapy.Item):
    name = scrapy.Field()
    school_id = scrapy.Field()
    college_id = scrapy.Field()
    academy_id = scrapy.Field()  # 学院id
    job_title = scrapy.Field()  # 职称
    directions = scrapy.Field()  # 研究方向
    picture = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    education = scrapy.Field()  # 学历
    qualification = scrapy.Field()  # 学位
    job_information = scrapy.Field()  # 在职信息
    responsibilities = scrapy.Field()  # 主要任职
    abstracts = scrapy.Field()  # 个人简介
    office_address = scrapy.Field()  # 办公地点


class SchoolItem(scrapy.Item):
    name = scrapy.Field()


class AcademyItem(scrapy.Item):
    school_id = scrapy.Field()
    name = scrapy.Field()
