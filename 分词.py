# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 18:44:53 2019

@author: 蘇
"""



import jieba
import pandas as pd
import os
import re

def fenci():
    stopwords=[]
    with open(r'D:\graduate\project\hgdstopword.txt','r',encoding='utf-8') as fp:
        ln=fp.readlines()
        for j in ln:
            j=j.split('\n')
            stopwords.append(j[0])
    print('调用pkuseg')        
#    seg = pkuseg.pkuseg()
    text=pd.read_csv(r'D:\graduate\project\comment.csv')
    comments=text['comment']
    all_cut_cumment=[]
    print('开始分词')
    for comment in comments:
        cut_cumment=''
        if type(comment) ==int or type(comment)==float:
            pass
        else:
            words =jieba.cut(comment)
            for word in words:
                if word not in stopwords:
                    word=re.sub('[^\\u4e00-\\u9fa5]','', word)
                    cut_cumment+=word+' '
        all_cut_cumment.append(cut_cumment)
    print('分词结束')
    return all_cut_cumment
def write_fenci(all_cut_cumment):
    result_file=r'result_fenci.txt'
    if os.path.exists(result_file):
        os.remove(result_file)
    with open (result_file,'a+',encoding='utf-8') as f:
        for comment in all_cut_cumment:
            f.write(comment+'\n')
            
a=fenci()
write_fenci(a)

        