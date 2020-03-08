import sys
import pandas as pd
from . import word2vec_prepare as wp
import numpy as np
from .models import Problem
from sklearn.cluster import k_means_
from sklearn.metrics.pairwise import cosine_similarity, pairwise_distances
from sklearn.preprocessing import StandardScaler
import jieba

def give_label(cluster_num):
    wp.synthesize_vec()
    data = pd.read_csv("./server/data/w2v_embedding.csv")
    df = pd.DataFrame(data)
    all_problems = Problem.objects.all()
    name_list = [item.prob.rstrip() for item in all_problems]
    stoplist = [k.strip() for k in open('./server/data/stopword.txt',encoding ="utf-8") if k.strip()!='']
    lines = [wp.fenci(item,stoplist) for item in name_list]

    scaler = StandardScaler(with_mean = False)
    arry = np.array(df)
    arry = scaler.fit_transform(arry)
    df = pd.DataFrame(arry)

    estimator = k_means_.KMeans(n_clusters= cluster_num, n_init=15).fit(df)
    df["name"] = name_list
    df["fenci"] = lines

    centroids = estimator.cluster_centers_

    r1=pd.Series(estimator.labels_).value_counts()
    r2=pd.DataFrame(centroids)
    r=pd.concat([r2,r1],axis=1)
    r = pd.concat([df, pd.Series(estimator.labels_)], axis = 1)  #详细
    r.columns = list(df.columns) + [u'聚类类别']
    result_dict = {}
    for index, row in r.iterrows():
        result_dict[row['name']] = row['聚类类别']
    print("w2v_complete!")
    for item in all_problems:
        item.w2v_label = result_dict[item.prob]
        item.save()

