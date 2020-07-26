# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CatmoviePipeline:
    def process_item(self, item, spider):
        title = item['title']
        kind = item['kind']
        time = item['time']
        output = f'|{title}|\t|{kind}|\t|{time}|\n\n'
        with open('./catmovie.txt', 'a+', encoding='utf-8') as article:
            article.write(output)
        return item
