# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import redis,re

# 初始化redis连接池,当成功的添加到数据库,就把url的code保存到数据库
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)  



class ThtPipeline:
    def __init__(self):
        self.db = pymysql.connect(host="127.0.0.1", user="root", password="root", database="tht", charset='utf8' )
    def process_item(self, item, spider):
        data=dict(item)#将传来的item字段转为字典
        cursor=self.db.cursor()
        #这里临时输出看一下
        # print(data['securities']+"---"+data['job_category']+"---"+data['source_url'])
        sql="INSERT INTO `jobs_test` (`id`, `securities`, `title`, `content`, `job_addr`, `job_category`, `publish_time`, `department`, `job_number`, `job_education`, `end_time`, `others`, `source_url`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cursor.execute(sql,[data['securities'],data['title'],data['content'],data['job_addr'],data['job_category'],data['publish_time'],data['department'],data['job_number'],data['job_education'],data['end_time'],data['others'],data['source_url']])
            self.db.commit()
        except:
            self.db.rollback()
            print(sql)
            print("sql错误------------------------------------------")
        cursor.close()
        #添加的url的最后id
        r.sadd(spider.name,re.findall(r'jobId=(\d+)',data['source_url'])[0])
        return item
    def close_spider(self,spider):
        self.db.close()
