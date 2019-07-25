# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 15:08:42 2019

@author: 蘇
"""


import csv
from pyecharts import Map, Geo
from pyecharts import Bar
import operator
import datetime
import pandas as pd



numDimensions = 300

maxSeqLength = 250 #最大序列长度

batchSize = 24 #批处理大小

lstmUnits = 64 #LSTM单元数

numClasses = 2 #输出类别数

iterations = 100000 #训练次数



import numpy as np

wordsList = np.load('.\wordsList.npy').tolist()

wordsList = [word.decode('UTF-8') for word in wordsList] #Encode words as UTF-8

wordVectors = np.load('.\wordVectors.npy')

import tensorflow as tf

tf.reset_default_graph()

labels = tf.placeholder(tf.float32, [batchSize, numClasses])

input_data = tf.placeholder(tf.int32, [batchSize, maxSeqLength])



data = tf.Variable(tf.zeros([batchSize, maxSeqLength, numDimensions]),dtype=tf.float32)

data = tf.nn.embedding_lookup(wordVectors,input_data)



lstmCell = tf.contrib.rnn.BasicLSTMCell(lstmUnits)

lstmCell = tf.contrib.rnn.DropoutWrapper(cell=lstmCell, output_keep_prob=0.25)

value, _ = tf.nn.dynamic_rnn(lstmCell, data, dtype=tf.float32)



weight = tf.Variable(tf.truncated_normal([lstmUnits, numClasses]))

bias = tf.Variable(tf.constant(0.1, shape=[numClasses]))

value = tf.transpose(value, [1, 0, 2])

last = tf.gather(value, int(value.get_shape()[0]) - 1)

prediction = (tf.matmul(last, weight) + bias)



correctPred = tf.equal(tf.argmax(prediction,1), tf.argmax(labels,1))

accuracy = tf.reduce_mean(tf.cast(correctPred, tf.float32))



sess = tf.InteractiveSession()

saver = tf.train.Saver()

saver.restore(sess, tf.train.latest_checkpoint('.\models'))



import re

strip_special_chars = re.compile("[^A-Za-z0-9 ]+")



def cleanSentences(string):

    string = string.lower().replace("<br />", " ")

    return re.sub(strip_special_chars, "", string.lower())



def getSentenceMatrix(sentence):

    arr = np.zeros([batchSize, maxSeqLength])

    sentenceMatrix = np.zeros([batchSize,maxSeqLength], dtype='int32')

    cleanedSentence = cleanSentences(sentence)

    split = cleanedSentence.split()

    for indexCounter,word in enumerate(split):

        try:

            sentenceMatrix[0,indexCounter] = wordsList.index(word)

        except ValueError:

            sentenceMatrix[0,indexCounter] = 399999 #Vector for unkown words

    return sentenceMatrix



inputText = "That movie was terrible."

inputMatrix = getSentenceMatrix(inputText)



predictedSentiment = sess.run(prediction, {input_data: inputMatrix})[0]



if (predictedSentiment[0] > predictedSentiment[1]):

    print ("Positive Sentiment")

else:

    print ("Negative Sentiment")