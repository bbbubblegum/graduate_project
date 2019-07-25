
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 13:24:48 2019

@author: 蘇
"""

# 首先加载必用的库
#%matplotlib inline
import numpy as np
#import matplotlib.pyplot as plt
import re
import jieba # 结巴分词
# gensim用来加载预训练word vector
from gensim.models import KeyedVectors
import warnings
warnings.filterwarnings("ignore")

# 我们使用tensorflow的keras接口来建模
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, GRU, Embedding, LSTM, Bidirectional
from tensorflow.python.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.optimizers import RMSprop
from tensorflow.python.keras.optimizers import Adam
from tensorflow.python.keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard, ReduceLROnPlateau

from sklearn.model_selection import train_test_split

# 使用gensim加载预训练中文分词embedding
cn_model = KeyedVectors.load_word2vec_format(r'sgns.zhihu.bigram-char',binary=False)

train_texts_orig= []
with open('train_text.txt','r',encoding='utf-8')as f:
    text=f.readlines()
    for j in text:
        j=j.split('\n')
        train_texts_orig.append(j[0])
        
# 进行分词和tokenize
# train_tokens是一个长长的list，其中含有4000个小list，对应每一条评价
train_tokens = []
for text in train_texts_orig:
    # 去掉标点
    text = re.sub("[^\\u4e00-\\u9fa5]", "",text)
    # 结巴分词
    if len(text)==0:
        pass
    else:
        cut = jieba.cut(text)
        # 结巴分词的输出结果为一个生成器
        # 把生成器转换为list
        cut_list = [ i for i in cut ]
        for i, word in enumerate(cut_list):
            try:
                # 将词转换为索引index
                cut_list[i] = cn_model.vocab[word].index
            except KeyError:
                # 如果词不在字典中，则输出0
                cut_list[i] = 0
        train_tokens.append(cut_list)
# 获得所有tokens的长度
num_tokens = [ len(tokens) for tokens in train_tokens ]
num_tokens = np.array(num_tokens)

# 最长的评价tokens的长度
max_tokens=np.max(num_tokens)
# 平均tokens的长度
mean_tokens=np.mean(num_tokens)

# 平均tokens的长度
print('# 平均tokens的长度:%s',mean_tokens)
      
print('最长的评价tokens的长度:%s',max_tokens)

# 取tokens平均值并加上两个tokens的标准差，
# 假设tokens长度的分布为正态分布，则max_tokens这个值可以涵盖95%左右的样本
#max_tokens = np.mean(num_tokens) + 2 * np.std(num_tokens)
max_tokens = int(max_tokens)
print('修改后最长的评价tokens的长度:%s',max_tokens)
# 取tokens的长度为27时，大约95%的样本被涵盖
# 我们对长度不足的进行padding，超长的进行修剪
np.sum( num_tokens < max_tokens ) / len(num_tokens)

#反向tokenize
#我们定义一个function，用来把索引转换成可阅读的文本，这对于debug很重要。

# 用来将tokens转换为文本
def reverse_tokens(tokens):
    text = ''
    for i in tokens:
        if i != 0:
            text = text + cn_model.index2word[i]
        else:
            text = text + ' '
    return text
reverse = reverse_tokens(train_tokens[0])
# 原始文本
origain_text=train_texts_orig[0]

# =============================================================================
# 准备Embedding Matrix
# 现在我们来为模型准备embedding matrix（词向量矩阵），
# 根据keras的要求，我们需要准备一个维度为$(numwords, embeddingdim)$的矩阵，
# num words代表我们使用的词汇的数量，
# emdedding dimension在我们现在使用的预训练词向量模型中是300，
# 每一个词汇都用一个长度为300的向量表示。
# 注意我们只选择使用前50k个使用频率最高的词，
# 在这个预训练词向量模型中，一共有260万词汇量，
# 如果全部使用在分类问题上会很浪费计算资源，
# 因为我们的训练样本很小，一共只有4k，
# 如果我们有100k，200k甚至更多的训练样本时，
# 在分类问题上可以考虑减少使用的词汇量。
# 
# =============================================================================
# 只使用前20000个词
num_words = 50000
# 初始化embedding_matrix，之后在keras上进行应用
embedding_dim=300
embedding_matrix = np.zeros((num_words, embedding_dim))
# embedding_matrix为一个 [num_words，embedding_dim] 的矩阵
# 维度为 50000 * 300
print('开始embedding_matrix')
for i in range(num_words):
    embedding_matrix[i,:] = cn_model[cn_model.index2word[i]]
embedding_matrix = embedding_matrix.astype('float32')

train_pad = pad_sequences(train_tokens, maxlen=max_tokens,
                            padding='pre', truncating='pre')
# =============================================================================
# 为了实现的简便，keras只能接受长度相同的序列输入。因此如果目前序列长度参差不齐，
# 这时需要使用pad_sequences()。
# 该函数是将序列转化为经过填充以后的一个长度相同的新序列新序列。
# 序列预处理pad_sequences()序列填充
# keras.preprocessing.sequence.pad_sequences(sequences, 
# 	maxlen=None,
# 	dtype='int32',
# 	padding='pre',
# 	truncating='pre', 
# 	value=0.)
# 
# sequences：浮点数或整数构成的两层嵌套列表
# maxlen：None或整数，为序列的最大长度。大于此长度的序列将被截短，小于此长度的序列将在后部填0.
# dtype：返回的numpy array的数据类型
# padding：‘pre’或‘post’，确定当需要补0时，在序列的起始还是结尾补`
# truncating：‘pre’或‘post’，确定当需要截断序列时，从起始还是结尾截断
# value：浮点数，此值将在填充时代替默认的填充值0
# =============================================================================

print('embedding_matrix结束')
train_pad[ train_pad>=num_words ] = 0
print('训练目标向量，样本标注，前1443个为n，后19443为p')
train_target = np.concatenate( (np.zeros(1443),np.ones(19202)) )

# 90%的样本用来训练，剩余10%用来测试
#X表示评论文本内容，Y表示评论文本的情感极性
X_train, X_test, y_train, y_test = train_test_split(train_pad,
                                                    train_target,
                                                    test_size=0.1,
                                                    random_state=12)
# 查看训练样本，确认无误
print(reverse_tokens(X_train[35]))
print('class: ',y_train[35])



# 用LSTM对样本进行分类
model = Sequential()
# 模型第一层为embedding
model.add(Embedding(num_words,
                    embedding_dim,
                    weights=[embedding_matrix],
                    input_length=max_tokens,
                    trainable=False))
model.add(Bidirectional(LSTM(units=32, return_sequences=True)))
model.add(LSTM(units=16, return_sequences=False))
model.add(Dense(1, activation='sigmoid'))
# 我们使用adam以0.001的learning rate进行优化
optimizer = Adam(lr=1e-3)

# =============================================================================
# 优化器optimizer：该参数可指定为已预定义的优化器名，如rmsprop、adagrad，
# 或一个Optimizer类的对象，详情见optimizers
# 
# 损失函数loss：该参数为模型试图最小化的目标函数，它可为预定义的损失函数名，
# 如categorical_crossentropy、mse，也可以为一个损失函数。详情见losses
# 
# 指标列表metrics：对分类问题，我们一般将该列表设置为metrics=['accuracy']。
# 指标可以是一个预定义指标的名字,也可以是一个用户定制的函数.指标函数应该返回单个张量,
# 或一个完成metric_name - > metric_value映射的字典.请参考性能评估
## For a binary classification problem
#model.compile(optimizer='rmsprop',
#              loss='binary_crossentropy',
#              metrics=['accuracy'])
# =============================================================================

model.compile(loss='binary_crossentropy',
              optimizer=optimizer,
              metrics=['accuracy'])
# 我们来看一下模型的结构，一共90k左右可训练的变量
model.summary()


# 建立一个权重的存储点
path_checkpoint = 'sentiment_checkpoint.keras'
checkpoint = ModelCheckpoint(filepath=path_checkpoint, monitor='val_loss',
                                      verbose=1, save_weights_only=True,
                                      save_best_only=True)

# 定义early stoping如果3个epoch内validation loss没有改善则停止训练
earlystopping = EarlyStopping(monitor='val_loss', patience=3, verbose=1)
# 自动降低learning rate
lr_reduction = ReduceLROnPlateau(monitor='val_loss',
                                       factor=0.1, min_lr=1e-5, patience=0,
                                       verbose=1)
# 定义callback函数
callbacks = [
    earlystopping, 
    checkpoint,
    lr_reduction
]
# 开始训练
model.fit(X_train, y_train,
          validation_split=0.1, 
          epochs=20,
          batch_size=128,
          callbacks=callbacks)
result = model.evaluate(X_test, y_test)

print('Accuracy:{0:.2%}'.format(result[1]))

# 尝试加载已训练模型
try:
    model.load_weights(path_checkpoint)
except Exception as e:
    print(e)

def predict_sentiment(text):
    try:
        print(text)
        # 去标点
        text = re.sub("[^\\u4e00-\\u9fa5]", "",text)
        # 分词
        if len(text)==0:
            pass
        else:
            cut = jieba.cut(text)
            cut_list = [ i for i in cut ]
            # tokenize
            for i, word in enumerate(cut_list):
                try:
                    cut_list[i] = cn_model.vocab[word].index
                except KeyError:
                    cut_list[i] = 0
            # padding
            tokens_pad = pad_sequences([cut_list], maxlen=max_tokens,
                                   padding='pre', truncating='pre')
            # 预测
            result = model.predict(x=tokens_pad)
            coef = result[0][0]
            if coef >= 0.5:
                return '正面评价'+' '+'output=%.2f'%coef
            else:
                return '负面评价'+' '+'output=%.2f'%coef
    except:
        return 'erro'
