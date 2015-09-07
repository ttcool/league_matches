# -*- coding: utf8 -*-
import json
from pandas import DataFrame
import pandas as pd

#数据保存为csv文件
def save_csv(filename):
    match = json.load(open(filename+'.json'))
    matches = []
    for i in match:
        j = []
        for k in i:
            if i[k] == None:
                j.append(i[k])
            else:
                j.append((i[k]).encode('utf8'))
        matches.append(j)
    data = pd.DataFrame(matches,columns=['序号','客队半场得分','客队球衣颜色','赢球平均欧指数','客队名称','本场比赛序号','主队盘路名称','客队盘路名称','盘路','status','平球平均欧指','主队ID','比赛时间','澳门盘口','输球平均欧指','主队本轮排名','主队名称','客队得分','主队得分','主队半场得分','轮次','客队本轮排名'])
    data.to_csv(filename+'.csv')

#意甲数据
print '保存意甲数据'
save_csv('Italian_Serie_A')
 
