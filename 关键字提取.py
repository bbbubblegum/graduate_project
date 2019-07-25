# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 14:56:55 2019

@author: 蘇
"""
#提取关键词
import jieba
import jieba.analyse.tfidf as tfidf
import jieba.analyse.textrank as textank
import jieba.analyse.analyzer as analyzer

import jieba.posseg as pseg


#path=r'D:\graduate\comment_tags.txt'
#
#data=[]
#with open(path,'r',encoding='utf-8') as f:
#    fword=f.readlines
#    for i in range(10):
#        data.append(f.readline())
##cutData = jieba.cut(data, cut_all=True)
##word_jieba = " ".join(cutData)
#cut_result={}
#cixing={}
#
#seg = pkuseg.pkuseg()#以默认配置加载模型
#for line in data:
#    text = seg.cut(line)
#    cut_result[line]=text#进行分词
#    word_pkuseg = " ".join(text)
#    words =pseg.cut(line)
#    for word, flag in words:
#        print('%s %s' % (word, flag))

keyword_tfidf={}
data='开始 人民'
for keyword, weight in tfidf(data,topK=50, withWeight=True):
    print('%s %s' % (keyword, weight))
    keyword_tfidf[keyword]=weight


# =============================================================================
# jieba.analyse.extract_tags(sentence, topK=20, withWeight=False, allowPOS=())
#                             sentence 为待提取的文本
#                             topK 为返回几个 TF/IDF 权重最大的关键词，默认值为 20
#                             withWeight 为是否一并返回关键词权重值，默认值为 False
#                             allowPOS 仅包括指定词性的词，默认值为空，即不筛选
# =============================================================================



