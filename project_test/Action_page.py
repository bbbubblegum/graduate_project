

# 猫眼电影介绍url
# http://maoyan.com/films/1217236

import requests, time
from fake_useragent import UserAgent
import json, csv, os
import pandas as pd
import datetime


class Spidermaoyan():
    headers = {
    		"User-Agent": UserAgent(verify_ssl=False).random,
    		"Host": "m.maoyan.com",
    		"Referer": "http://m.maoyan.com/movie/1200486/comments?_v_=yes"
    	}
    def __init__(self, url):
    		self.url = url
    	
    	# 发送get请求
    def get_json(self):
    		# 发送get请求
    		response_comment = requests.get(self.url, headers=self.headers)
    		json_comment = response_comment.text
    		json_comment = json.loads(json_comment)
    		# print(json_comment)
    		return json_comment
    	
    	# 获取数据并存储
    def get_data(self, json_comment):
            json_response = json_comment["cmts"]  # 列表
            #print(len(json_response))
            list_info = []
            for data in json_response:
                cmtime = data["time"]
                userId = data["userId"]
                cityName = data["cityName"]
                content = data["content"]
                if "gender" in data:
                    gender = data["gender"]
                else:
                    gender = 0
                nickName = data["nickName"]
                userLevel = data["userLevel"]
                score = data["score"]
                list_one = [cmtime, userId, nickName, gender, cityName, userLevel, score, content]
                list_info.append(list_one)
            self.file_do(list_info)
    	
    	# 存储文件
    def file_do(self, list_info):
    		# 获取文件大小
            file_size = os.path.getsize(r'D:/graduate/DyingToSurvive.csv')
            if file_size == 0:
    			# 表头
                name = ['评论日期','用户ID','评论者昵称', '性别', '所在城市', '猫眼等级', '评分', '评论内容']
    			# 建立DataFrame对象
                file_test = pd.DataFrame(columns=name, data=list_info)
    			# 数据写入
                file_test.to_csv(r"D:/graduate/DyingToSurvive.csv", encoding="utf_8_sig", index=False)
            else:
                with open(r"D:/graduate/DyingToSurvive.csv","a+", encoding="utf_8_sig", newline='') as file_test:
    				# 追加到文件后面
                    writer = csv.writer(file_test)
    				# 写入文件
                    writer.writerows(list_info)

# 猫眼电影短评接口
offset =15
# 电影是2018.9.21上映的
startTime=datetime.date(2018,7,6)
str_startTime=str(startTime)
count=0
try:
    while startTime<datetime.date(2018,12,3):
        comment_api ='http://m.maoyan.com/mmdb/comments/movie/1200486.json?_v_=yes&offset={0}&startTime={1}%2022%3A13%3A52'.format(
                offset,str_startTime)
        s0 = Spidermaoyan(comment_api)
        json_comment = s0.get_json()
        if json_comment["total"] == 0:  # 当前时间内评论爬取完成  
            offset=15
            startTime=startTime+datetime.timedelta(days=1)
            str_startTime=str(startTime)
            continue
        s0.get_data(json_comment)
        offset +=15
        count+=1
        print(count)
except:
    count=count*15
    print('当前可取数据：%d条爬取完成'%count*15)
#time.sleep()

