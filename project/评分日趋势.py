# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 15:04:42 2019

@author: 蘇
"""

import csv
from pyecharts import Map, Geo
from pyecharts import Bar
import operator
import datetime
import pandas as pd


# 读数据
def read_csv():
	# 读取文件内容
    excelFile = r'DyingToSurvive.xlsx'
    df = pd.DataFrame(pd.read_excel(excelFile,sheet_name='Sheet1',header=0))  
    date = df['评论日期']
    nickName = df['评论者昵称']
    gender = df['性别']
    cityName = df['所在城市']
    userLevel = df['猫眼等级']
    score = df['评分']
    content=df['评论内容']
#    print(df)
    
    return date,nickName,gender,cityName,userLevel,score,content



# 每日评论总数可视化分析
def time_num_visualization(date):
    from pyecharts import Line
    date_list = list(date)
    set_date = sorted(list(set(date)))
    print(set_date)
    date_dict={}
    date_num = []
    for i in range(len(set_date)):
        date_dict[str(set_date[i]).split()[0]] = date_list.count(set_date[i])
	# 根据数量(字典的键值)排序
    date_name = []
    date_num = []
#    print(sort_dict)
    for i in date_dict:
        date_name.append(i)
        date_num.append(date_dict[i])
			
    line = Line("我不是药神--猫眼电影评论数量日期折线图")
    line.add(
		"日期-评论数",
		date_name,
		date_num,
		is_fill=False,
		area_color="#fff",
		area_opacity=0.2,
		is_smooth=True,
        is_more_utils = True,
        is_label_show=False,
        is_xaxislabel_align=True,
        xaxis_max='2018-12-18',
        lineSytle='polar',
        mark_point=[['max'],['min']],
        mark_line=["average"],
        tooltip_trigger="axis" , # 触发类型，item=数据项触发，默认，主要在散点图，饼图等无类目图中使用，xais=坐标轴触发，主要在柱状图，折线图等有类目的途中使用，none=什么都不触发
        tooltip_trigger_on="mousemove", # 触发条件, mousemove=鼠标移动的时候，click=电机的时候，mousemove|click=点击或移动的时候，none=不触发
        tooltip_axispointer_type="shadow", # 指示器类型，默认=line，直线，shadow=隐形，cross=十字准星
        tooltip_formatter= '{c}', # str类型，{a}=系列名称add第一个参数，{b}=对应的x轴值，{c}=x,y坐标
        tooltip_text_color= "red", # 提示框文本的颜色
        tooltip_font_size=20, # 提示框字体的大小
        tooltip_background_color="#fff", # 提示框背景色
        tooltip_border_color="#fff", # 提示框边框的颜色
        tooltip_border_width=1, # 边框的宽度
	)
    line.render("c_num_line.html")


# 4 评论数
time_num_visualization(date)