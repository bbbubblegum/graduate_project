# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 17:58:32 2019

@author: 蘇
"""

import jieba.analyse.tfidf as tfidf
import jieba
import imageio
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt
import pandas as pd
import re 


def fenci():
    stopwords=[]
    with open(r'D:\graduate\project\baidustopword_n.txt','r',encoding='utf-8') as fp:
        ln=fp.readlines()
        for j in ln:
            j=j.split('\n')
            stopwords.append(j[0])     
    excelFile=r'D:\graduate\project\lstm_comment_all.xlsx'
    text= pd.DataFrame(pd.read_excel(excelFile,sheet_name='n',header=0))    
#    text= pd.DataFrame(pd.read_excel(excelFile,sheet_name='p',header=0))
    comments=text['评论内容']
    cumment_lists=[]
    for comment in comments:
        if type(comment) ==int or type(comment)==float:
            pass
        else:
            cumment_lists.append(comment)
    print('开始分词')
    cut_cumment=''
    for comment in cumment_lists:
        words =jieba.cut(comment)
        for word in words:
            if word not in stopwords:
                word=re.sub('[^\\u4e00-\\u9fa5]','', word)
                cut_cumment+=word+' '
    keyword_tfidf={}
    count=0
    for keyword, weight in tfidf(cut_cumment,topK=50, withWeight=True):
        keyword_tfidf[keyword]=weight
        count+=1
        print(count)
    return cut_cumment,keyword_tfidf

cut_cumment,keyword_tfidf=fenci()
    
back_color = imageio.imread(r'D:\graduate\m.jpg')  # 解析该图片

wc = WordCloud(background_color='white',  # 背景颜色
#               collocations : bool, default=True //是否包括两个词的搭配
               collocations=False,
               max_words=300,  # 最大词数
               mask=back_color,  # 以该参数值作图绘制词云，这个参数不为空时，width和height会被忽略
               max_font_size=100,  # 显示字体的最大值
               font_path=r"C:\Windows\Fonts\Microsoft YaHei UI\msyhl.ttc",  # 解决显示口字型乱码问题，可进入C:/Windows/Fonts/目录更换字体
               random_state=26,  # 为每个词返回一个PIL颜色
               width=1000,  # 图片的宽
               height=860  #图片的长
               )


##wc.generate_from_frequencies(keyword_ctb8)
#wc.generate(cut_cumment)
## 基于彩色图像生成相应彩色
#image_colors = ImageColorGenerator(back_color)
## 显示图片
#plt.figure()
#plt.rcParams['savefig.dpi'] = 1000 #图片像素
#plt.rcParams['figure.dpi'] = 600 #分辨率
#plt.imshow(wc)
## 关闭坐标轴
#plt.axis('off')
## 绘制词云
## 保存图片
#wc.to_file('5.png')
