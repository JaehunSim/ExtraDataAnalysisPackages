# -*- coding: cp949 -*-
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
from numpy import nan as NA
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.patches as mpatches

def path_c(path):
    "change path with \\ to /"
    pathC = ''
    for i in path:
        if i != '\\':
            pathC += i
        else:
            pathC += '/'
    return pathC

def drop_index(df):
    "drop index which has 0, change columns into int type"  
    list1=[]
    for i in range(len(df.index)):
        try:
            if pd.value_counts(df.values[i])[0]> 0:
                list1.append(i)
        except:
            pass
        
    for i in list1:
        df = df.drop(df.index[i])
        for j in range(len(list1)):
            list1[j]= list1[j]-1


    
    return df

def line_graph(data,xslot,yslot,ylimit_low,ylimit_high):
    "draw line graph"
    fig, axes = plt.subplots(5,5)
    count = 0
    for i in range(xslot):
        for j in range(yslot):
            try:
                x=data.columns
                y=data.ix[count]
                axes[i,j].plot(x,y,color='k',marker='o')
                axes[i,j].set(ylim=[ylimit_low,ylimit_high])
                axes[i,j].set_title(data.index[count], size=10)
                #axes[i,j].set_xlabel(data.index[count:count+2])
                count+=1          
            except:
                pass
    return axes

def single_graph(data,number,ylimit_low=70.,ylimit_high=130.):
    fig, axes = plt.subplots(1,1)
    x=data.columns
    y=data.ix[number]
    axes.plot(x,y,color='k',marker='o')
    ticks = axes.set_xticks(elementary1.columns)
    axes.set(ylim=[ylimit_low,ylimit_high])
    try:
        axes.set_title(data.index[number], size=10)
    except:
        axes.set_title(number, size=10)
    for xy in zip(tuplify(data.ix[number].index),
                  tuplify(data.ix[number].values)):
        axes.annotate(xy[1], xy=xy, xytext=(xy[0],xy[1]+1))
    return axes

def multi_graph(number,ylimit_low=80.,ylimit_high=140.,*data):
    color_list=['b','g','r','c','m','y','k','w']
    label_list=['Elementary','Middle','High']
    color_count=0
    fig, axes = plt.subplots(1,1)
    #axes.set(ylim=[ylimit_low,ylimit_high]) #Error raised...
    for i in data:
        x=i.columns
        y=i.ix[number]
        axes.plot(x,y,color=color_list[color_count],marker='o')
        ticks = axes.set_xticks(elementary1.columns)
        color_count+=1
        #if color_count >8:
            #color_count=0
        """
        try:
            axes.set_title(i.index[number], size=10)
        except:
            axes.set_title(number, size=10)
        """
        
        for xy in zip(tuplify(i.ix[number].index),
                          tuplify(i.ix[number].values)):
                axes.annotate(xy[1], xy=xy, xytext=(xy[0],xy[1]+1))

        
                
    return axes

def tuplify(thing):
    ex=[]
    for i in thing:
        ex.append(i)
    ex2=[]
    for i in ex:
        ex2.append(int(i))
    result = tuple(ex2)
    return result

def increase_rate(data):
    "change data to increase_rate"
    for j in range(len(data.index)):
        temp1 = pd.Series(data.ix[j].values.copy(),
                         index=data.ix[j].index.copy(),
                         name=data.ix[j].name)

        data.ix[j][0] = 100.0
        for i in range(len(data.ix[0].index)-1):
            data.ix[j][i+1] = (float(data.ix[j][i+1])/temp1[i])*100

    return data

def change_to_int(data):
    ex=[]
    for i in data.columns:
        ex.append(int(i))
    data.columns = ex
    return data

def draw_by_single(data,number):
    single_graph(data,number,80.,140.)
    plt.grid()
    plt.axhline(y=100., linewidth=2,color='k')
    plt.show()

def draw_by_multi(number,*data):
    #Num 0 : Kore,a #Num 1: Israel, #Num 2: Japan...
    axes =multi_graph(number,80.,140.,*data)
    axes.set(ylim=[80.,140.])
    legendList = []
    for i in data:
        legendList.append(i.index.name)
    plt.legend(tuple(legendList))
    plt.title((elementary1.ix[number].name) +"'s Education Expenditure Increase Rate (%)")
    plt.grid()
    plt.axhline(y=100., linewidth=2,color='k')
    plt.show()
    
def fill_missing_data(data):
    list1 = []
    count=0
    for i in data.values:
        if i==0:
            list1.append(count)
        count+=1
    count=0
    while count<len(list1):
        for i in list1:
            data.values[i] = data.values[i+1]*1/float(pow(data.values[len(data)-1]/float(data.values[i+1]),1/float(len(data)-i-2)))
        count+=1
            
"""
count = 0
x=df1.columns
y=df1.ix[count]
axes[0,0].plot(x,y,'ko-',label='one')
axes[0,0].set(ylim=[0.,13000.])
count+=1
y=df1.ix[count]
axes[0,0].plot(x,y,'ko-',label=df1.index[count])
count+=1
y=df1.ix[count]
axes[0,0].plot(x,y,'ko-',label='three')

plt.show()
"""

elementary = pd.read_csv('newData_elementary.csv',index_col='Nation') #original data
elementary1 = drop_index(elementary) #dropped data that lacks
#line_graph(df1,5,5,0.,13000.)
elementary1 = increase_rate(elementary1) #change data to increased format
#line_graph(df2,5,5,70.,130.) #draw line graph
change_to_int(elementary1)

middle = pd.read_csv(path_c('newData_middle.csv'),index_col='Nation')
a=middle.ix['Poland']
fill_missing_data(a)
middle1 = drop_index(middle)
middle1 = increase_rate(middle1)
change_to_int(middle1)

high = pd.read_csv(path_c('newData_high.csv'),index_col='Nation')
b=high.ix['Denmark']
fill_missing_data(b)
high1 = drop_index(high)
high1 = increase_rate(high1)
change_to_int(high1)

elementary1.index.name = "Elementary"
middle1.index.name = "Middle"
high1.index.name = "High"

draw_by_multi(2,elementary1,middle1,high1)




    
