import sys
from gensim import corpora
import pandas as pd
from gensim import models
import lda
from .models import Problem
import jieba

def jiebafenci(problem_i, stoplist):
    seglist = [k for k in jieba.cut(problem_i) if k not in stoplist]
    return seglist

def lda_model(class_num):
    stoplist = [k.strip() for k in open("./server/data/stopword.txt", encoding = 'utf-8') if (k.strip() !='')]
    all_problems = Problem.objects.all()
    problems = [problem_i.prob for problem_i in all_problems]
    lines = [jiebafenci(problem_i, stoplist) for problem_i in problems]
    dictionary = corpora.Dictionary(lines)
    #for index,value in dictionary.items():
    #    print(index, "\t", value)
    corpus = [dictionary.doc2bow(line) for line in lines]
    #for i in range(10):
        #print(corpus[i])
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    lda = models.ldamodel.LdaModel(corpus = corpus_tfidf, id2word = dictionary, num_topics = class_num)
    corpus_lda = lda[corpus_tfidf]
    topics = lda.print_topics(num_topics = class_num, num_words = 5)

    result_list = []
    for item in list(corpus_lda):
        max_pair = (-1.000,-1.000)
        for a,b in item:
            if (b > max_pair[1]):
                max_pair = (a,b)
        result_list.append(max_pair)

    result_df = pd.DataFrame(result_list)
    lines_df = pd.DataFrame(problems)
    result = pd.concat([lines_df,result_df],axis = 1)
    result.columns= ["fenci","cluster","probability"]
    result["problem"]= problems
    for index, row in result.iterrows():
        print(row["fenci"], row["cluster"])
        print("---------")
    result_dic = {}
    for index, row in result.iterrows():
        result_dic[row["problem"]] = row["cluster"]
    for item in all_problems:
        item.lda_label = result_dic[item.prob]
        item.save()
    
