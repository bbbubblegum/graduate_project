
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 15:13:15 2019

@author: 蘇
"""
import os
# gensim用来加载预训练word vector
import warnings
warnings.filterwarnings("ignore")

# 使用tensorflow的keras接口来建模
import tensorflow_LSTM as tf_lstm

words_list=[]

with open ('big_num.txt','r',encoding='utf-8')as f:
    big_text=f.readlines()
    for text in big_text:
        text=text.split('\n')
        words_list.append(text[0])
result_file='情感分析结果_new.txt'
if os.path.exists(result_file):
    os.remove(result_file)
for text in words_list:
    result=tf_lstm.predict_sentiment(text)
    if type(result)==str:
        with open (result_file,'a+',encoding='utf-8')as rf:
            rf.write(text+' '+result+'\n')


