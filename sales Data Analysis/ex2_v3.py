# -*- coding: utf-8 -*-
import matplotlib
import pandas as pd
import numpy as np
from pandas import DataFrame, Series
import datetime
from matplotlib import pyplot as plt
import math

##matplotlib settings##
matplotlib.rc('font', family='Arial')

##Data Gathering##
rawData = pd.read_csv("SalesJan2009.csv")

##Data Store/Manage##
#changing format of columns
rawData.Price = rawData.Price.astype("float64")
rawData.Transaction_date = Series(map(pd.to_datetime,rawData.Transaction_date.values))
rawData.Account_Created = Series(map(pd.to_datetime,rawData.Account_Created.values))
#Product Standard Cost
productCost = {"Product1":1200, "Product2":3600, "Product3":7500}
#Get index that doesn't match standard cost
indexToDumpTemp = []
temp = rawData.ix[:,1:3]
for i in range(len(productCost)):
    temp2 = temp[temp.Product =="Product"+str(i+1)]
    indexToDumpTemp.append(temp2.Price[temp2.Price != productCost["Product"+str(i+1)]].index.values)
indexToDump = np.array([], dtype="int64")
for i in range(len(indexToDumpTemp)):
    indexToDump = np.concatenate((indexToDump, indexToDumpTemp[i]))
#Drop index that doesn't match
rawData = rawData.drop(indexToDump)
#replace space with empty in City Column"
for i in range(len(rawData.City.values)):
    rawData.City.values[i] = rawData.City.values[i].replace(" ","")

##Data Analysis##
#Making new DataFrame
Data = DataFrame(rawData.ix[:,0])
Data["Customer_info"] = rawData.Name + " " + rawData.City
Data["Country"] = rawData.Country
Data["Product"] = rawData.Product
Data["Td_sub_A"] = rawData.Transaction_date - rawData.Account_Created #Transaction_date-Account_Created
Data["Td_sub_A"] = Data["Td_sub_A"].values.view('<i8')/((10**9)*60)
def country_to_product():
    #1.Split by Product and Map(groupby) Country
    cp = Data[["Country","Product"]]
    cp1 = cp[cp["Product"]=="Product1"]
    Product1_graph = cp1.groupby("Country").count()["Product"].copy()
    Product1_graph.sort()
    Product1_graph = Product1_graph[Product1_graph>=Product1_graph.quantile(0.8)] #Product1 bigger than 5
    cp2 = cp[cp["Product"]=="Product2"]
    Product2_graph = cp2.groupby("Country").count()["Product"].copy()
    Product2_graph.sort()
    Product2_graph = Product2_graph[Product2_graph>=Product2_graph.quantile(0.6)]
    cp3 = cp[cp["Product"]=="Product3"]
    Product3_graph = cp3.groupby("Country").count()["Product"].copy()
    Product3_graph.sort()
    #2.plotting
    fig= plt.figure()
    ax1 = plt.subplot(1,3,1)
    ax2 = plt.subplot(1,3,2)
    ax3 = plt.subplot(1,3,3)
    #2)ax1
    plt.axes(ax1)
    Product1_graph.plot(kind="bar")
    plt.title("Product1")
    ##for tick in ax1.get_xticklabels():
      ##  tick.set_rotation("horizontal")
    #2)ax2
    plt.axes(ax2)
    Product2_graph.plot(kind="bar")
    plt.title("Product2")
    #2)ax3
    plt.axes(ax3)
    Product3_graph.plot(kind="bar")
    plt.title("Product3")
    #3.save fig
    plt.savefig(r"Country_to_Product.png", bbox_inches='tight')

def product_to_AcTd():        
    pat = Data[["Product","Td_sub_A"]]
    timecut = [0,60*24,1440*10,1440*90,1440*3000]#[0,60,60*3,60*24,1440*3,1440*10,1440*90,1440*3000]
    #1.Discretization & Ordering by cut level
    pat1 = pat[pat["Product"]=="Product1"]
    pat1_data = pd.cut(pat1.Td_sub_A,timecut)
    temp = pd.value_counts(pat1_data)
    temp2 = temp.copy()
    for i in range(len(temp2)):
        temp2[i] = temp[pat1_data.levels[i]]
    temp2.index = pat1_data.levels
    pat1_data = temp2
    pat2 = pat[pat["Product"]=="Product2"]
    pat2_data = pd.cut(pat2.Td_sub_A,timecut)
    temp = pd.value_counts(pat2_data)
    temp2 = temp.copy()
    for i in range(len(temp2)):
        temp2[i] = temp[pat2_data.levels[i]]
    temp2.index = pat2_data.levels
    pat2_data = temp2
    pat3 = pat[pat["Product"]=="Product3"]
    pat3_data = pd.cut(pat3.Td_sub_A,timecut)
    temp = pd.value_counts(pat3_data)
    temp2 = temp.copy()
    for i in range(len(temp2)):
        temp2[i] = temp[pat3_data.levels[i]]
    temp2.index = pat3_data.levels
    pat3_data = temp2
    #2.plotting
    fig= plt.figure()
    ax1_1 = plt.subplot(1,3,1)
    ax2_1 = plt.subplot(1,3,2)
    ax3_1 = plt.subplot(1,3,3)
    #2)ax1
    plt.axes(ax1_1)
    pat1_data.plot(kind="bar")
    plt.title("Product1")
    pat1xticks = ax1_1.set_xticklabels(["~1day","1~10days","10~90days","90days~"], rotation='horizontal',size=7)
    #2)ax2
    plt.axes(ax2_1)
    pat2_data.plot(kind="bar")
    plt.title("Product2")
    pat2xticks = ax2_1.set_xticklabels(["~1day","1~10days","10~90days","90days~"], rotation='horizontal',size=7)
    #2)ax3
    plt.axes(ax3_1)
    pat3_data.plot(kind="bar")
    plt.title("Product3")
    pat3xticks = ax3_1.set_xticklabels(["~1day","1~10days","10~90days","90days~"], rotation='horizontal',size=7)
    #3.save fig
    plt.savefig(r"Product_to_AcTd.png", bbox_inches='tight')

def country_to_AcTd():
    cat = Data[["Country","Td_sub_A"]]
    cat1 = cat.groupby("Country").count()["Td_sub_A"].copy()
    cat1.sort()
    cat1 = cat1[-9:]
    timecut = [0,60*24,1440*10,1440*90,1440*3000]#[0,60,60*3,60*24,1440*3,1440*10,1440*90,1440*3000]
    #1.Discretization & Ordering by cut level
    def popS(name,series,bigger):
        "return specific name Series from bigger"
        return series[series[bigger]==name]
    cat1_1 = popS(cat1.index[-1],cat,"Country")
    cat1_2 = popS(cat1.index[-2],cat,"Country")
    cat1_3 = popS(cat1.index[-3],cat,"Country")
    cat1_4 = popS(cat1.index[-4],cat,"Country")
    cat1_5 = popS(cat1.index[-5],cat,"Country")
    cat1_6 = popS(cat1.index[-6],cat,"Country")
    cat1_7 = popS(cat1.index[-7],cat,"Country")
    cat1_8 = popS(cat1.index[-8],cat,"Country")
    cat1_9 = popS(cat1.index[-9],cat,"Country")
    def dataInTimecut(data,timeColumn,timecut):
        "reorganizing data into timecut by timeColumn number"
        data = pd.cut(data.ix[:,timeColumn],timecut)
        temp = pd.value_counts(data)
        temp2 = temp.copy()
        for i in range(len(temp2)):
            temp2[i] = temp[data.levels[i]]
        temp2.index = data.levels
        data = temp2
        return data
    cat1_1_data = dataInTimecut(cat1_1,1,timecut)
    cat1_2_data = dataInTimecut(cat1_2,1,timecut)
    cat1_3_data = dataInTimecut(cat1_3,1,timecut)
    cat1_4_data = dataInTimecut(cat1_4,1,timecut)
    cat1_5_data = dataInTimecut(cat1_5,1,timecut)
    cat1_6_data = dataInTimecut(cat1_6,1,timecut)
    cat1_7_data = dataInTimecut(cat1_7,1,timecut)
    cat1_8_data = dataInTimecut(cat1_8,1,timecut)
    cat1_9_data = dataInTimecut(cat1_9,1,timecut)
    #2.plotting
    fig= plt.figure()
    ax1 = plt.subplot(3,3,1)
    ax2 = plt.subplot(3,3,2)
    ax3 = plt.subplot(3,3,3)
    ax4 = plt.subplot(3,3,4)
    ax5 = plt.subplot(3,3,5)
    ax6 = plt.subplot(3,3,6)
    ax7 = plt.subplot(3,3,7)
    ax8 = plt.subplot(3,3,8)
    ax9 = plt.subplot(3,3,9)
    #ax1)
    plt.axes(ax1)
    cat1_1_data.plot(kind="bar")
    plt.title(cat1_1.Country.values[0])
    ax1.set_xticklabels(["~1day","1~10days","10~90days","90days~"], rotation='horizontal',size=8)
    #ax2)
    plt.axes(ax2)
    cat1_2_data.plot(kind="bar")
    plt.title(cat1_2.Country.values[0])
    ax2.set_xticklabels(["~1day","1~10days","10~90days","90days~"], rotation='horizontal',size=8)
    #ax3)
    plt.axes(ax3)
    cat1_3_data.plot(kind="bar")
    plt.title(cat1_3.Country.values[0])
    ax3.set_xticklabels(["~1day","1~10days","10~90days","90days~"], rotation='horizontal',size=8)
    #ax4)
    plt.axes(ax4)
    cat1_4_data.plot(kind="bar")
    plt.title(cat1_4.Country.values[0])
    ax4.set_xticklabels(["~1day","1~10days","10~90days","90days~"], rotation='horizontal',size=8)
    #ax5)
    plt.axes(ax5)
    cat1_5_data.plot(kind="bar")
    plt.title(cat1_5.Country.values[0])
    ax5.set_xticklabels(["~1day","1~10days","10~90days","90days~"], rotation='horizontal',size=8)
    #ax6)
    plt.axes(ax6)
    cat1_6_data.plot(kind="bar")
    plt.title(cat1_6.Country.values[0])
    ax6.set_xticklabels(["~1day","1~10days","10~90days","90days~"], rotation='horizontal',size=8)
    #ax7)
    plt.axes(ax7)
    cat1_7_data.plot(kind="bar")
    plt.title(cat1_7.Country.values[0])
    ax7.set_xticklabels(["~1day","1~10days","10~90days","90days~"], rotation='horizontal',size=8)
    #ax8)
    plt.axes(ax8)
    cat1_8_data.plot(kind="bar")
    plt.title(cat1_8.Country.values[0])
    ax8.set_xticklabels(["~1day","1~10days","10~90days","90days~"], rotation='horizontal',size=8)
    #ax9)
    plt.axes(ax9)
    cat1_9_data.plot(kind="bar")
    plt.title(cat1_9.Country.values[0])
    ax9.set_xticklabels(["~1day","1~10days","10~90days","90days~"], rotation='horizontal',size=8)
    #3.save fig
    plt.tight_layout()
    plt.savefig(r"Country_to_AcTd.png", bbox_inches='tight')

def duplicated_buy():
    "how many customers have bought again?"
    customer = Data.Customer_info
    customer2 = customer.drop_duplicates()
    return customer.count() - customer2.count()
def transdate_to_Product():
    tp = Data[["Transaction_date","Product"]]
    tp = tp.sort(columns="Transaction_date")
    #1.ata managing
    tp1 = tp[tp["Product"]=="Product1"]
    tp1_data = tp1.groupby(tp1["Transaction_date"].map(lambda t: t.day)).count()["Product"]
    tp2 = tp[tp["Product"]=="Product2"]
    tp2_data = tp2.groupby(tp2["Transaction_date"].map(lambda t: t.day)).count()["Product"]
    tp3 = tp[tp["Product"]=="Product3"]
    tp3_data = tp3.groupby(tp3["Transaction_date"].map(lambda t: t.day)).count()["Product"]
    #2.plotting
    fig= plt.figure()
    ax1 = plt.subplot(1,1,1)
    graph1 = ax1.plot(tp1_data,"ko--", label="Product1")
    graph2 = ax1.plot(tp2_data,"bo--", label="Product2")
    graph3 = ax1.plot(tp3_data,"go--",label="Product3")
    plt.title("Transdate to Product")
    plt.legend(loc="best")
    plt.grid()
    plt.xlim(0,30)
    #2.axhline)mean
    plt.axhline(y=tp1_data.mean(),linewidth=1,color='k')
    plt.axhline(y=tp2_data.mean(),linewidth=1,color='b')
    #2.trend line
    x = range(1,32)
    z = np.polyfit(x,tp1_data.values,1)
    p = np.poly1d(z)
    ax1.plot(x,p(x),'k--')
    z2 = np.polyfit(x,tp2_data.values,1)
    p2 = np.poly1d(z2)
    ax1.plot(x,p2(x),'b--')
    #3.save fig
    plt.tight_layout()
    plt.savefig(r"Transdate_to_Product.png", bbox_inches='tight')


