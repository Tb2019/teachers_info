# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class ShiheziUniversityPipeline:

    def open_spider(self, spider):
        self.local_conn = pymysql.connect(
            host='localhost', user='root', password='123456', database='alpha_search', port=3306, charset='utf8'
        )
        self.cursor = self.local_conn.cursor()
        self.table = 'search_teacher'
        # print('连接上了数据库')

    def process_item(self, item, spider):
        # print(item)
        keys = ','.join(item.keys())
        values = ','.join(['%s'] * len(item))
        sql = """
            insert into {table} ({keys}) values({values})
        """.format(table=self.table, keys=keys, values=values)
        try:
            if self.cursor.execute(sql, tuple(item.values())):
                print('insert successful')
                self.local_conn.commit()
        except:
            print('insert failed')
            self.local_conn.rollback()
        return item

    def close_spider(self, spider):
        self.local_conn.close()
        print('爬取结束')