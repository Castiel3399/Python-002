# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql


class CatmoviePipeline:
    def process_item(self, item, spider):
        title = item['title']
        kind = item['kind']
        time = item['time']
        output = f'{title},{kind},{time}\n'
        self.run(title, kind, time)
        # self.run()

    def run(self, title, kind, time):
        conn = pymysql.connect(
            host='192.168.3.20',
            port=3306,
            user='root',
            password='lou-1987',
            db='spider'
        )
        # 游标建立的时候就开启了一个隐形的事物
        cur = conn.cursor()
        command = 'insert into maoyan(filmTitle, filmKind, filmTime) values(%s, %s, %s)'
        print(command)
        try:
            cur.execute(command, (title, kind, time))
            # 关闭游标
            cur.close()
            conn.commit()
        except:
            conn.rollback()
        # 关闭数据库连接
        conn.close()
