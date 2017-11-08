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
#from collections import Counter
#import json

today = datetime.today()
time = ["","9:30~10:30","10:30~11:30","11:30~13:00",
"13:00~1400","14:00~15:00","15:00~16:00","16:00~17:00"]
date = []
for i in range(20):
    if (today+Day(i)).isoweekday() not in [6,7]:
        date.append((today+Day(i)).strftime("%m/%d %a").upper())
days = []
for i in range(len(date)):
	days.append(date[i][-3:])
date = date[days.index("MON"):]
days = days[days.index("MON"):]
date = date[:days.index("FRI")+6]

empty = [["" for i in range(8)] for i in range(10)]
for i in range(len(date)):
	empty[i][0] = date[i]
for i in range(len(empty)):
	empty[i][3] = "Lunch Time"
timetable = DataFrame(empty, index=date, columns=time)
timetable.ix[:,2] = "Lunch Time"

nrows, ncols = len(date)+1, len(time)
hcell, wcell= 0.3, 1.
hpad, wpad = 0,0
fig = plt.figure(figsize=(ncols*wcell+wpad, nrows*hcell+hpad))
ax = fig.add_subplot(111)
"""
"Hiding x,y labels"
for xlabel_i in ax.axes.get_xticklabels():
    xlabel_i.set_visible(False)
    xlabel_i.set_fontsize(0.0)
for xlabel_i in ax.axes.get_yticklabels():
    xlabel_i.set_fontsize(0.0)
    xlabel_i.set_visible(False)
"""
ax.xaxis.set_major_formatter(plt.NullFormatter())
ax.yaxis.set_major_formatter(plt.NullFormatter())
for sp in ax.spines.itervalues():
	sp.set_color("w")
	sp.set_zorder(0)

the_table = ax.table(cellText=empty,colLabels=time,
		     loc='center')
the_table.auto_set_font_size(False)
the_table.set_fontsize(15)
the_table.set_zorder(10)

ax.text(0.25,0.9,"Jaehun Sim",fontsize=45)
ax.text(0.60,0.075,"Not here: ", fontsize=25)
ax.text(0.74, 0.075,"Highlighted", fontsize=25)
ax.grid(b=False)
plt.show()

