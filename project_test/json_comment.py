# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 14:58:37 2018

@author: 蘇
"""

'''
data : 2018.10.06
author : 极简XksA
goal : 爬取猫眼《悲伤逆流成河》影评，词云可视化
'''

# 猫眼电影介绍url
# http://maoyan.com/films/1217236

import requests
from fake_useragent import UserAgent
import json
headers = {
        "User-Agent": UserAgent(verify_ssl=False).random,
        "Host":"m.maoyan.com",
        "Referer":"http://m.maoyan.com/movie/1200486/comments?_v_=yes"
    }
# 猫眼电影短评接口
offset = 15
#offset=995 to the end 
# 电影是2018.9.21上映的
startTime = '2018-07-06'
#http://m.maoyan.com/mmdb/comments/movie/1200486.json?_v_=yes&offset=15&startTime=2018-11-28%2014%3A56%3A57
comment_api ='http://m.maoyan.com/mmdb/comments/movie/1200486.json?_v_=yes&offset=995&startTime=2018-07-26%2022%3A13%3A52'
# 发送get请求
response_comment = requests.get(comment_api,headers = headers)
json_comment = response_comment.text
json_comment = json.loads(json_comment)
print(json_comment)
