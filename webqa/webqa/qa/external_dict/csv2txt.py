# encoding=utf-8
"""
@desc：将csv文件按jieba外部词典的格式转为txt文件
nz代表地名
"""
import pandas as pd

df = pd.read_csv('./location.csv', sep='\n')
title = df['location_name'].values

with open('./location.txt', 'a') as f:
    for t in title[1:]:
        f.write(t + '@@' + 'ns' + '\n')