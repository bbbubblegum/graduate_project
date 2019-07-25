# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 17:58:32 2019

@author: 蘇
"""
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


# 评论者性别分布可视化
def sex_distribution(gender):
	# print(gender)
	from pyecharts import Pie
	list_num = []
	list_num.append(gender.count('0')) # 未知
	list_num.append(gender.count('1')) # 男
	list_num.append(gender.count('2')) # 女
	attr = ["其他","男","女"]
	pie = Pie("我不是药神--观影用户性别饼图")
	pie.add("", attr, list_num, is_label_show=True, is_more_utils = True)
	pie.render("sex_pie.html")

# 评论者所在城市分布可视化
def city_distribution(cityName):
    city_list = list(set(cityName))
    city_dict = {city_list[i]:0 for i in range(len(city_list))}
    for i in range(len(city_list)):
        city_dict[city_list[i]] = cityName.count(city_list[i])
	# 根据数量(字典的键值)排序
    L = sorted(city_dict.items(),key=lambda item:item[1],reverse=True)
    
    n=20
 
    L = L[:n]
     
    dictdata = {}
    for l in L:
        dictdata[l[0]] = l[1]

    sort_dict = sorted(dictdata.items(), key=lambda d: d[1], reverse=True)
    city_name = []
    city_num = []
    for i in range(len(sort_dict)):
        city_name.append(sort_dict[i][0])
        city_num.append(sort_dict[i][1])


    bar = Bar("我不是药神--猫眼电影评论者城市分布")
    bar.use_theme('macarons')
    bar.add("", city_name, city_num, \
            mark_line = ['average'],\
            bar_category_gap = '50%',\
            is_label_show=True, \
            is_datazoom_show=True, \
            is_more_utils = True\
            )
    bar.render("city_bar.html")
    
	
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
			
    line = Line("我不是药神--电影评论数量日期折线图")
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
        is_xaxislabel_align=False,
        xaxis_max='2018-12-18',
        mark_point=[['max'],['min']],
        mark_line=["average"],
        tooltip_trigger="axis" , # 触发类型，item=数据项触发，默认，主要在散点图，饼图等无类目图中使用，xais=坐标轴触发，主要在柱状图，折线图等有类目的途中使用，none=什么都不触发
        tooltip_trigger_on="mousemove", # 触发条件, mousemove=鼠标移动的时候，click=电机的时候，mousemove|click=点击或移动的时候，none=不触发
        tooltip_axispointer_type="shadow", # 指示器类型，默认=line，直线，shadow=隐形，cross=十字准星
        tooltip_formatter= '{c}', # str类型，{a}=系列名称add第一个参数，{b}=对应的x轴值，{c}=x,y坐标
        tooltip_text_color= "#000", # 提示框文本的颜色
        tooltip_font_size=20, # 提示框字体的大小
        tooltip_background_color="#fff", # 提示框背景色
        tooltip_border_color="#fff", # 提示框边框的颜色
        tooltip_border_width=1, # 边框的宽度
	)
    line.render("c_num_line.html")

	
# 评论者猫眼等级、评分可视化
def level_score_visualization(userLevel,score):
    from pyecharts import Pie
    userLevel_list = list(set(userLevel))
    userLevel_list = sorted(userLevel_list)
    userLevel_num = []
    for i in range(len(userLevel_list)):
        userLevel_num.append(userLevel.count(userLevel_list[i]))
#    
#    score_list = list(set(score))
#    score_list = sorted(score_list)
#    score_num = []
#    for i in range(len(score_list)):
#        score_num.append(score.count(score_list[i]))
#    
#    pie01 = Pie("我不是药神--观影用户等级环状饼图", title_pos='center', width=900)
#    pie01.add(
#		"等级",
#		userLevel_list,
#		userLevel_num,
#		radius=[40, 75],
#		label_text_color=None,
#		is_label_show=True,
#		legend_orient="vertical",
#		legend_pos="left",
#        is_more_utils = True
#	)
#    pie01.render("level_pie.html")
#    pie02 = Pie("我不是药神--观影用户评分玫瑰饼图", title_pos='center', width=900)
#    pie02.add(
#		"评分",
#		score_list,
#		score_num,
#		center=[50, 50],
#		is_random=True,
#		radius=[30, 75],
#        legend_orient="vertical",
#        legend_pos="left",
#		rosetype="area",
#		is_legend_show=True,
#		is_label_show=True,
#	)
#    pie02.render("score_pie.html")

date,nickName,gender,cityName,userLevel,score,content = read_csv()



# 2 性别分布
#sex_distribution(gender)
# 3 城市分布
#city_distribution(cityName)
# 4 评论数
#time_num_visualization(date)
# 5 等级，评分
level_score_visualization(userLevel,score)
