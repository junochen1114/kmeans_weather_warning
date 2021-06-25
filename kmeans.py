######################################
# analysis ###########################
######################################

import numpy as np
import pandas as pd
import weatherLearn
import random
from collections import defaultdict
import xlsxwriter
from pyecharts import options as opts
from pyecharts.charts import Geo
import matplotlib as mpl
import matplotlib.pyplot as plt


def distance(vec1, vec2):  # Euclidean distance
    return np.sqrt(np.sum(np.square(vec1 - vec2)))


# dataset: {地名: [0, 0, ...]} 对应的是warnColorlist
def loadDataSet():
    dataset = defaultdict(list)
    for place in wl.places:
        data = mp.read_mongo({'largeLocation': place}, False)['warnColor'].value_counts()
        dataset[place] = [0]*len(warnColorList)
        for warncolor, count in data.items():
            idx = warnColorList.index(warncolor)
            dataset[place][idx] = count
    return dataset


def initCentroids(dataSet, k):
    random_keys = random.sample(dataSet.keys(), k)
    return [np.array(dataSet[rkey]) for rkey in random_keys]


def minDistance(dataset, centroidList):
    # 对于每个dataset里的item，计算item和centroid的距离，把item放入相应的cluster中
    # centroidList = [vector]
    # clusterDict = { 0: {地名:[vector]}， 1:{地名:[vector]}}
    # dataset: {地名: [0, 0, ...]} 对应的是warnColorlist
    clusterDict = dict()
    for key, value in dataset.items():
        vec1 = np.array(value)
        cluster = 0
        minDis = float("inf")

        for i in range(len(centroidList)):
            vec2 = centroidList[i]
            dist = distance(vec1, vec2)

            if dist < minDis:
                minDis = dist
                cluster = i

        if cluster not in clusterDict.keys():
            clusterDict[cluster] = dict()

        clusterDict[cluster][key] = vec1
    return clusterDict


def getCentroids(clusterDict):
    # 得到k个质心
    centroidList = list()
    for rkey in clusterDict.keys():
        centroid = np.mean(list(clusterDict[rkey].values()), axis=0)
        # 计算每列的均值，即找到质心
        centroidList.append(centroid)

    return np.array(centroidList).tolist()


def getVar(clusterDict, centroidList):
    # 计算簇集合间的均方误差 sum()
    # 将簇类中各个向量与质心的距离进行累加求和
    # centroidList = [vector]
    # clusterDict = { 0: {地名:[vector]}， 1:{地名:[vector]}}

    var_sum = 0.0
    for key in clusterDict.keys():
        vec1 = np.array(centroidList[key])
        dist = 0.0
        for item in clusterDict[key].values():
            vec2 = np.array(item)
            dist += distance(vec1, vec2)**2
        var_sum += dist

    return var_sum


def kmeans(dataSet, k_cluster):
    centroidList = initCentroids(dataSet, k_cluster)
    clusterDict = minDistance(dataSet, centroidList)
    newVar = getVar(clusterDict, centroidList)  # 获得均方误差值，通过新旧均方误差来获得迭代终止条件
    oldVar = -0.0001  # 旧均方误差值初始化为-1
    # print('***** 第1次迭代 *****')
    # for key in clusterDict.keys():
    #     print(key, ' --> ', clusterDict[key])
    # print('均值向量: ', centroidList)
    # print('平均均方误差: ', newVar)
    # showCluster(centroidList, clusterDict)

    k = 2
    while abs(newVar - oldVar) >= 0.0001:  # 当连续两次聚类结果小于0.0001时，迭代结束
        centroidList = getCentroids(clusterDict)  # 获得新的质心
        clusterDict = minDistance(dataSet, centroidList)  # 新的聚类结果
        oldVar = newVar
        newVar = getVar(clusterDict, centroidList)
        # print('***** 第%d次迭代 *****' % k)
        # for key in clusterDict.keys():
        #     print(key, ' --> ', clusterDict[key])
        # print('均值向量: ', centroidList)
        # print('平均均方误差: ', newVar)
        # showCluster(centroidList, clusterDict)

        k += 1
    return centroidList, clusterDict


def write_dict(loc_dict, clusterDict,time):
    # clusterDict = { 0: {地名:[vector]}， 1:{地名:[vector]}}
    # loc_dict = {地名: [0, 0, 0, ...]}
    for cluster, dic in clusterDict.items():
        for location in dic.keys():
            loc_dict[location][time] = cluster
    return loc_dict


def write_excel(locDict, kmeans_dict, excel_path):
    workbook = xlsxwriter.Workbook(excel_path)
    worksheet = workbook.add_worksheet()

    row = 0

    for location,cluster in kmeans_dict.items():
        worksheet.write_string(row, 0, str(location))
        worksheet.write_number(row, 1, cluster)
        for idx in range(2, 12):
            worksheet.write_number(row, idx, locDict[location][idx-2])
        row += 1
    workbook.close()


if __name__ == '__main__':
    iter_times = 1
    k_cluster = 10

    wl = weatherLearn.weatherLearn()
    mp = wl.mp
    warnColorList = sorted(mp.count('warnColor'))
    dataset = loadDataSet()
    SSElist = [0]*(k_cluster-2)

    for time in range(2, k_cluster):
        centroidList, clusterDict = kmeans(dataset, time)
        SSE = getVar(clusterDict, centroidList)
        SSElist[time-2] = SSE

    x = range(2, k_cluster)
    y = SSElist
    plt.plot(x, y)
    plt.show()

    # locDict = {}  # record the 10 times of knn results of each location
    # initialization
    # for loc in dataset.keys():
    #     locDict[loc] = [0]*iter_times
    #
    # for i in range(iter_times):
    #     centroidList, clusterDict = kmeans(dataset, k_cluster)
    #     write_dict(locDict, clusterDict, i)

    # # show info
    # for location, value in locDict.items():
    #     print(location, ': ', value)

    # kmeans_dict = {}
    # for location, kmeans_lst in locDict.items():
    #     max_count = max(kmeans_lst, key=kmeans_lst.count)
    #     kmeans_dict[location] = max_count
    #     print(location, max_count)
    #
    # write_excel(locDict, kmeans_dict, 'kmeans_4.xlsx')


















