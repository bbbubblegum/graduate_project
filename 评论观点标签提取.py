# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 13:38:58 2019

@author: 蘇
"""

from pyhanlp import HanLP
import re
import os
# # 依存句法分析
# result_file = 'comment_tags.txt'
# if os.path.exists(result_file):
#     os.remove(result_file)
# with open(r'D:\graduate\project\comment.txt','r',encoding='utf-8')as f:
#     comments=f.readlines()
# for comment in comments:
#     if len(comment)>30:
#         pass
#     else:
#         comment=HanLP.parseDependency(comment)
#         word_DEPREL=[]
#         words={}
#         for i,word in enumerate(comment.iterator()):  # 通过dir()可以查看comment的方法
#            # print("%s --(%s)--> %s" % (word.LEMMA, word.DEPREL, word.HEAD.LEMMA))
#            # with open('a.txt','w',encoding='utf-8') as f:
#            #     print((comment), file=f)
#            word_DEPREL.append(word.DEPREL)
#            words[i]=word
#
#         comment_tags=[]
#         word_tag=""
#         for i in range(len(words)):
#             word = words[i]
#             if "主谓关系" not in  word_DEPREL:
#                 if "动宾关系" not in  word_DEPREL:#处理只有核心关系的情况
#                         if word.DEPREL=="核心关系":
#                             word_tag += word.LEMMA
#                 else:                           #没有谓语，只有动宾关系
#                         if word.DEPREL=="核心关系" or word.DEPREL=="动宾关系":
#                             word_tag += word.LEMMA
#             elif "动宾关系" in word_DEPREL: #主谓宾关系
#                     if word.DEPREL=="主谓关系" or word.DEPREL=="核心关系" \
#                         or word.DEPREL=="动宾关系":
#                         word_tag += word.LEMMA
#
#         word_tag=re.sub('[^\\u4e00-\\u9fa5]','', word_tag)
#         if len(word_tag) !=0:
#             comment_tags.append(word_tag)
#
#         with open(result_file,'a+',encoding='utf-8') as f_tags :
#             for comment_tag in comment_tags:
#                 f_tags.write(comment_tag+'\n')


word='很好很好很好'

comment=HanLP.parseDependency(word)
for i,word in enumerate(comment.iterator()):  # 通过dir()可以查看comment的方法
    print("%s --(%s)--> %s" % (word.LEMMA, word.DEPREL, word.HEAD.LEMMA))
with open('b.txt','w',encoding='utf-8') as f_result:
    print((comment),file=f_result)

print(comment)


