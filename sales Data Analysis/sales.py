from __future__ import division
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
from numpy import nan as NA
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse
from pandas.tseries.offsets import Day, MonthEnd, Minute, Hour
import json

def path_c(path):
    "change path with \\ to /"
    pathC = ''
    for i in path:
        if i != '\\':
            pathC += i
        else:
            pathC += '/'
    return pathC

def sorting(data,column):
    sort = data.sort(columns=column)
    sort.index = list(range(len(sort)))

    return sort

def value_counts(data,number):
    df_info_keys = ['Transaction_date','Product','Price','Payment_Type',
                'State','Country']
    print data[df_info_keys[number]].value_counts()

df = pd.read_csv(path_c('SalesJan2009.csv'))

df_info_keys = ['Transaction_date','Product','Price','Payment_Type',
                'State','Country']
sales = DataFrame(df, columns = df_info_keys)

#sales = sales[:10]

ab =sorting(sales,df_info_keys[0])
#print ab['Product'].value_counts()
