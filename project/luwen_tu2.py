# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 15:36:51 2019

@author: 蘇
"""

from pyecharts import Map, Geo
from pyecharts import Bar
import operator
import datetime
import pandas as pd


class Read_excel(object):
    def read_csv(self):
    	# 读取文件内容
        excelFile = r'lstm_comment_all.xlsx'
        df = pd.DataFrame(pd.read_excel(excelFile,sheet_name='lstm',header=0,encoding='utf-8'))  
        return df


#date = df['评论日期']
#nickName = df['评论者昵称']
#gender = df['性别']
#cityName = df['所在城市']
#userLevel = df['猫眼等级']
#score = df['评分']
#content=df['评论内容']
#sentiment=df['情感极性']  
#return date,nickName,gender,cityName,userLevel,score,content,sentiment

class Make_pic(Read_excel): 
    def sex_distribution(self):
        df=self.read_csv()
        v1 = []
        v2 = []
        
        boy_df_p=df[(df['情感极性']=='正面评价') & (df['性别']==1)]
        print(boy_df_p)
        boy_con_p=len(boy_df_p['性别'])

        girl_df_p=df[(df['情感极性']=='正面评价')&(df['性别']==2)]
        girl_con_p=len(girl_df_p['性别'])
        
        
        boy_df_n=df[(df['情感极性']=='负面评价')&(df['性别']==1)]
        boy_con_n=len(boy_df_n['性别'])

        girl_df_n=df[(df['情感极性']=='负面评价')&(df['性别']==2)]
        girl_con_n=len(girl_df_n['性别'])
  
        attr = ['男性','女性']
        
        boy_p=boy_con_p/(boy_con_p+boy_con_n)
        girl_p=girl_con_p/(girl_con_p+girl_con_n)
        boy_n=boy_con_n/(boy_con_p+boy_con_n)
        girl_n=girl_con_n/(girl_con_p+girl_con_n)
    
        v1.append(boy_p)
        v1.append(girl_p)
        v2.append(boy_n)
        v2.append(girl_n)   

        bar = Bar('《我不是药神》观影用户性别情感倾向图')
        bar.add('好评',attr,
                v1,
                is_stack = True,
                legend_orient="vertical",
                legend_pos="left",
        		rosetype="area",
        		is_legend_show=True,
        		is_label_show=True,
                xaxis_name='性别',
                yaxis_name='人数',
                label_pos="inside"
                )  #is_stack = True才表示堆叠在一起
        bar.add('差评',
                attr,
                v2,
                is_stack = True,
                is_convert = True,
                is_label_show=True,
                label_pos="inside",
                is_legend_show=True)#is_convert 交换 XY 轴
        bar.render('sentimen_sex.html')   
        
    def city_distribution(self):
        df=self.read_csv()

        cityName=df['所在城市']
        
        #获取所有城市名称
        city_list = list(set(cityName))
        city_list=['北京','天津','上海','重庆','河北','山西','辽宁',\
                   '吉林','黑龙江','江苏','浙江','安徽','福建','江西',\
                   '山东','河南','湖北','湖南','广东','海南','四川',\
                   '贵州','云南','陕西','甘肃','青海','台湾','内蒙古自治区',\
                   '广西壮族自治区','西藏自治区','宁夏回族自治区','新疆维吾尔自治区',\
                   '香港特别行政区','澳门特别行政区']
        city_list_1=['北京','上海','广州','深圳',\
                   '成都','杭州','武汉','重庆','南京',\
                   '天津','苏州','西安','长沙','沈阳',\
                   '青岛','郑州','大连','东莞','宁波']
        
        city_list_2=['昆明','大连','厦门','合肥','佛山','福州',\
                   '哈尔滨','济南','温州','长春','石家庄','常州',\
                   '泉州','南宁','贵阳','南昌','南通','金华','徐州','太原',\
                   '嘉兴','烟台','惠州','保定','台州','中山','绍兴',\
                   '乌鲁木齐','潍坊','兰州']
        city_list=city_list_1+city_list_2
        
        city_dict = {city_list[i]:0 for i in range(len(city_list))}

        for i in range(len(city_list)):
            city_p=df[(df['情感极性']=='正面评价') & (df['所在城市']==city_list[i])]
            city_n=df[(df['情感极性']=='负面评价') & (df['所在城市']==city_list[i])]
            num=len(city_p['所在城市'])+len(city_n['所在城市'])
            if num!=0:
                city_count_p=len(city_p['所在城市'])/num
                if city_count_p!=1:
                    city_dict[city_list[i]] = city_count_p
            
            
        
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
    

a=Make_pic()
a.city_distribution()