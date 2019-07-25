# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.conf import settings

class MaoyanPipeline(object):
    def process_item(self, item, spider):
        host = settings['MYSQL_HOSTS']
        user = settings['MYSQL_USER']
        psd = settings['MYSQL_PASSWD']
        db = settings['MYSQL_DBNAME']
        char=settings['CHARSET']
        port=settings['MYSQL_PORT']
#数据库连接
        connet=pymysql.connect(host=host,user=user,passwd=psd,db=db,charset=char,port=port)
        #数据库游标
        youbiao=connet.cursor()
        print("mysql connect succes")#测试语句，这在程序执行时非常有效的理解程序是否执行到这一步
        	 	#sql="insert into gamerank (rank,g_name,g_type,g_status,g_hot) values(%s,%s,%s,%s,%s)" % (item['rank'],item['game'],item['type'],item['status'],item['hot'])
        try:
            sql="insert into DyingToSurvive (评论日期,评论时间,用户ID,评论者昵称,性别,所在城市,猫眼等级,评分,评论内容)\
                    VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (item['cmdate'],item['cmtime'],item['userId'],item['nickName'],item['gender'],item['cityName'],item['userLevel'],item['score'],item['content'])
            youbiao.execute(sql)
        except Exception as reason:
        	 return('Insert error:',reason)
        	 connet.rollback()
        else:
        	 connet.commit()
        	 connet.close()
        	 return item
