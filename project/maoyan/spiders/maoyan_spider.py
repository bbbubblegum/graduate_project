# -*- coding: utf-8 -*-

"""
Created on Wed Nov 28 14:58:37 2018

@author: 蘇
"""

from scrapy import Request
from scrapy.spiders import Spider
from maoyan.items import MaoyanItem
from fake_useragent import UserAgent
import json
import datetime
import re
import time

class MaoyanSpider(Spider):

    name = 'maoyan' #设置爬虫名字为maoyan

    headers = {
    		"User-Agent": UserAgent(verify_ssl=False).random,
    		"Host": "m.maoyan.com",
    		"Referer": "http://m.maoyan.com/movie/1200486/comments?_v_=yes"
    	} 
#   设置请求头文件，模拟浏览器访问 
#   User Agent存放于Headers中，服务器就是通过查看Headers中的User Agent来判断是谁在访问。
#   在Python中，如果不设置User Agent，程序将使用默认的参数，那么这个User Agent就会有Python的字样，
#   如果服务器检查User Agent，那么没有设置User Agent的Python程序将无法正常访问网站。


    def start_requests(self):

        url = 'http://m.maoyan.com/mmdb/comments/movie/1200486.json?_v_=yes&offset=975&startTime=2018-07-06%2013%3A53%3A19'

        yield Request(url, headers=self.headers)
    
    def parse(self, response):

        datas = json.loads(response.body)#将Json格式数据处理为字典类型
        
        cmdatas=datas['cmts']
        
        item = MaoyanItem()
        
        endTime  =  datetime.date(2018,7,6)

        #获取url时间参数startTime=2018-08-11
        startTime = re.search(r'startTime=\d+\-\d+\-\d+',response.url).group()
        
        #分割url时间参数得到['startTime', '2018', '08', '11']
        startTime=re.split(r'[\=\-]',startTime)
        
        s_year = int(startTime[1])
        
        s_month = int(startTime[2])
        
        s_day = int(startTime[3])
        
        #转化url时间参数
        startTime = datetime.date(s_year,s_month,s_day)
        
        if startTime<endTime:
            
            next_url='0'
            
            print('爬取完毕')
            
        elif cmdatas:

            for data in cmdatas:
                item['cmdate']     = data['time'].split()[0]
                
                item['cmtime']     = data['time'].split()[1]
                 
                item['userId']     = data['userId']
                 
                item['cityName']   = data['cityName']
                 
                item['content']    = data['content']
                
                if "gender" in data:
                    item['gender']     = data['gender']
                else:
                    item['gender']     = '0'
    
                item['nickName']   = data['nickName']
                 
                item['userLevel']  = data['userLevel']
                 
                item['score']      = data['score']
            
                yield item

 

            # 如果cmdatas存在数据则对下一页进行采集

            page_num = re.search(r'offset=(\d+)', response.url).group(1)
            
            #获取当前offset参数
            
            #startTime = re.search(r'startTime=(\d\d\d\d-\d\d-\d\d)',response.url).group(1)
            
            #获取当前startTime参数

            offsetnum=(int(page_num)+15)
            
            #从2018-12-12 开始 offset=0---1005 后更换 日期为后一天
            #爬取存在以下问题： 
            #               （已解决）评论时间到达2018-07-06 后如何停止-->无参数[cmts]返回，erro报错，爬虫结束
            #               （已解决）翻页过程中，如数据库2018-11-06中存在的数据 与startTime=2018-11-06中存在的数据重复（excel去重）
            #               (已解决) 当前爬取资源url中的startTime与最后的评论时间相同时
            #                --> 判断当前Url中的startTime 与最后评论时间 若相同 则 最后评论时间减一天             
            #当前爬取资源<GET http://m.maoyan.com/mmdb/comments/movie/1200486.json?_v_=yes&offset=120&startTime=2018-08-05%2013%3A53%3A19> (referer: http://m.maoyan.com/movie/1200486/comments?_v_=yes)
            if offsetnum<990:
                
                page_num = 'offset=' + str(offsetnum)
    
                next_url = re.sub(r'offset=\d+', page_num, response.url)
                
            #当offset>990时，重置offset=15,startTime=当前评论的最后时间
            else:
                #最后的评论时间
                lastTime = item['cmdate'].split('-')

                cmt_year  = int(lastTime[0])
                
                cmt_month = int(lastTime[1])
                
                cmt_day   = int(lastTime[2])
                
                cmtime = datetime.date(cmt_year,cmt_month,cmt_day)
                
                #判断时间参数startTime 是否等于最后的评论时间cmtime 如果相等 startTime提前一天
                
                if cmtime == startTime:
                    
                    startTime = startTime-datetime.timedelta(days=1)
                else:
                    startTime=cmtime
                
                offsetnum=15
                
                #最后一条短评的cmtime -----评论时间转化成时间参数
                
                str_startTime='startTime='+str(startTime)
                
                page_num = 'offset=15'
                
                next_url = re.sub(r'offset=\d+', page_num, response.url)
                
                next_url = re.sub(r'startTime=\d+\-\d+\-\d+',str_startTime , next_url)
                
        #处理链接
            
            time.sleep(5)
            
            yield Request(next_url, headers=self.headers,dont_filter=True)
            
            
            #下一页