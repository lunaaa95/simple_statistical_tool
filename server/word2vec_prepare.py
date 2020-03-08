import sys
import jieba
from .models import Problem
from gensim.models import word2vec
import time
import pandas as pd
import numpy as np
from sklearn.cluster import k_means_
from sklearn.metrics.pairwise import cosine_similarity, pairwise_distances
from sklearn.preprocessing import StandardScaler

def getVector_v1(line, word2vec_model):
    count = 0
    line_vector = np.zeros( word2vec_model.layer1_size )
    for word in line:
        if word in word2vec_model:
            line_vector += word2vec_model[word]
            count += 1
    if count == 0:
        count =1
    return line_vector / count
def word_vector_to_csv(word2vec_model):
    f = open("./server/data/wordfile.txt","w")
    dic = {}
    for word in word2vec_model.wv.index2word:
        word_vector = word2vec_model[word]
        f.writelines(word + " ")
        for item in list(word_vector):
            f.writelines(str(item)+" ")
        f.writelines("\n")
    print("wordfile prepared")
    return

def fenci(prob, stoplist):
    seglist = [k for k in jieba.cut(prob) if k not in stoplist]
    return seglist

def prepare_vec():
    all_problems = Problem.objects.all()
    stoplist = [k.strip() for k in open('./server/data/stopword.txt', encoding ="utf-8") if k.strip() != '']
    name_list = [item.prob.strip() for item in all_problems]
    lines = [fenci(item, stoplist) for item in name_list]
    all_words = []
    for line in lines:
        all_words.extend(line)
    word2vec_model = word2vec.Word2Vec(lines, size=15, iter=20, min_count=10, window = 5, negative = 3)
    #合适最低计数值
    word_vector_to_csv(word2vec_model)
    #print(word2vec_model.wv.most_similar('为什么'))
    vector_list = []
    i = 0
    for line in lines[:]:
        vector_list.append( getVector_v1(line, word2vec_model) )
    df = pd.DataFrame(vector_list)
    df.to_csv("./server/data/w2v_embedding.csv", index = False)
    print("w2v_embedding.csv is prepared!")

def synthesize_vec():
    prepare_vec()

def main():
    synthesize_vec()

if __name__ == '__main__':
    main()
