from __future__ import division
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
from numpy import nan as NA
import matplotlib.pyplot as plt
from datetime import datetime
#from datetime import timedelta
from dateutil.parser import parse
#from pandas.tseries.offsets import Day, MonthEnd, Minute, Hour
#from collections import Counter
#import json
from operator import methodcaller


def path_c(path):
    "change path with \\ to /"
    pathC = ''
    for i in path:
        if i != '\\':
            pathC += i
        else:
            pathC += '/'
    return pathC
"""
def drop_comma_in_string(series):
    result = []
    for i in series:
        if ',' in i:
            temp = i.split(",")
            temp2 = ""
            for i in temp:
                    temp2 += i
        result.append(temp2)
    result = Series(result, dtype='object', name=series.name)
    result.index = series.index
    return result

def swap_to_noncomma_data(series):
    result = drop_comma_in_string(series)
    result.name = series.name
    return result
"""
def change_date_to_datetime(series):
    "series or DataFrame index changing to datetime"
    temp = series.index
    ex1 = []
    for i in range(len(temp)):
        ex1.append(parse(temp[i]))
    series.index = ex1
    series = series.sort_index()
    return series

data = pd.read_csv(path_c("C:\Users\Home\Desktop\python\Data\stock\stock_data2.csv"),
                   index_col=0)
change_date_to_datetime(data)
data.index = data.sort_index().index
list1 = list(data.columns)
list1.append("")
list1 = [list1[-1]]+list1[:-1]

dict1 = {list1[0]: "YDM",
         list1[1]: "CI",
         list1[2]: "C",
         list1[3]: "FR%",
         list1[4]: "MI",
         list1[5]: "HI",
         list1[6]: "LI",
         list1[7]: "V(Fx)",
         list1[8]: "V(Fo)",
         list1[9]: "TV(W)(Fx)",
         list1[10]: "TV(W)(Fo)",
         list1[11]: "IPOMC(W)(Fx)",
         list1[12]: "IPOMC(W)(Fo)"}

str2 = ""
for i in range(len(data.columns)):
	str2 += (dict1[data.columns[i]]+",")
list2 = str2.split(",")
list2 = list2[0:-1]
data.columns = list2

change = data.ix[:,:6]
fig, axes = plt.subplots(1,1)
change.CI.plot()
axes.set_title('KOSPI labeling TOP5% up&down')

"annotating top, down values"
top = change.C[change.C>change.C.quantile(0.95)]
down = change.C[change.C<change.C.quantile(0.05)]
top_index = top.index.map(lambda x: x.strftime('%m-%d'))
down_index = down.index.map(lambda x: x.strftime('%m-%d'))
for i in range(len(top)):
    axes.annotate((top_index[i],float(top.values[i])),
                  xy=(top.index[i], change.CI[top.index[i]]+5),
                  xytext=(top.index[i], change.CI[top.index[i]]+5))
for i in range(len(down)):
    axes.annotate((down_index[i],float(down.values[i])),
                  xy=(down.index[i], change.CI[down.index[i]]+5),
                  xytext=(down.index[i], change.CI[down.index[i]]+5))
plt.grid()
plt.show()


