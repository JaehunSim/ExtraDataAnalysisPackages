from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pandas.tseries.offsets import Day, MonthEnd, Minute, Hour

def cstrtod(date):
    "change_str_into_datetime_form"
    datetime1 = datetime(int(date[0:4]),int(date[4:6]),int(date[6:8]))
    return datetime1

def cdtostr(datetime_form):
    "change_datetime_into_str_form"
    year = str(datetime_form.year)
    if len(str(datetime_form.month)) == 1:
        month = "0"+str(datetime_form.month)
    else:
        month = str(datetime_form.month)
    if len(str(datetime_form.day)) == 1:
        day = "0"+str(datetime_form.day)
    else:
        day = str(datetime_form.day)
    return year+month+day

def create_holiday(year):
    year = str(year)
    "2016~2020 create holidays"
    holiday_list = []
    korean_holiday_in_solar = ["0101","0301","0505","0606","0815","1003","1009","1225"]
    korean_holiday_in_lunar = {"2016": ["0208","0514","0915"],
                               "2017": ["0128","0503","1004"],
                               "2018": ["0216","0522","0924"],
                               "2019": ["0205","0512","0913"],
                               "2020": ["0125","0430","1001"]}        
    for i in korean_holiday_in_solar:
        if i == korean_holiday_in_solar[2]:
            date = cstrtod(year+i).isoweekday()
            if date == 0:
                holiday_list.append(cdtostr(cstrtod(year+i)+Day(1)))
            if date == 6:
                holiday_list.append(cdtostr(cstrtod(year+i)+Day(2)))
            else:
                holiday_list.append(year+i)
            continue
        holiday_list.append(year+i)

    for i in korean_holiday_in_lunar[year]:
        if i == korean_holiday_in_lunar[year][1]:
            holiday_list.append(year+i)
            continue
        date = cstrtod(year+i).isoweekday()
        if date in [0,1,6]:
            for j in [-1,0,1,2]:
                holiday_list.append(cdtostr(cstrtod(year+i)+Day(j)))
        else:
            for j in [-1,0,1]:
                holiday_list.append(cdtostr(cstrtod(year+i)+Day(j)))
   
    holiday_list.sort()
    
    output = []
    for x in holiday_list:
        if x not in output:
            output.append(x)
        else:
            if cstrtod(str(int(x)+1)).isoweekday() == 0:
                output.append(str(int(x)+2))    
            else:
                output.append(str(int(x)+1))    
    return output

def main(date1):
    "input as year+month...ex). 201603"
    month_days = [31,29,31,30,31,30,31,31,30,31,30,31]
    if(int(str(date1)[:4]) % 4 == 0):
        month_days[1] = 28
    today = datetime.today()

    empty = [["" for i in range(7)] for i in range(7)]


    "SUN to SAT for days list"
    date = []
    for i in range(15):
        date.append((today+Day(i)).strftime("%m/%d %a").upper())
    days = []
    for i in range(len(date)):
            days.append(date[i][-3:])
    days = days[days.index("SUN"):days.index("SUN")+7]

    empty[0] = days
    empty = np.array(empty)
    empty = empty.flatten()    

    date1 = str(date1) + "01"
    ex = cstrtod(date1)
    holidays = create_holiday(ex.year)
    
    startday = 7+ex.isoweekday()
    empty[startday] = str(1)
    for i in range(month_days[ex.month-1]):
        empty[startday+i] = str(1+i)

    empty = empty.reshape((7,7))
    "Figure intial setting"
    nrows, ncols = 7, 7     #7rows, 7columns 
    hcell, wcell= 0.2, 1.   #height 0.2, width 1.0
    hpad, wpad = 0,0
    fig = plt.figure(figsize=(ncols*wcell+wpad, nrows*hcell+hpad))
    ax = fig.add_subplot(111)
    plt.axis('off')         #make all the axis invisible

    "Table Setting"
    the_table = ax.table(cellText=empty,loc='center', cellLoc='center')
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(15)

    cells = the_table.properties()["celld"]

    #for i in range(nrows):
        #for j in range(ncols):
            #cells[i,j].set_verticalalignment("top") 

    "Title of the calendar"
    ax.text(0.42,1.07,str(ex.strftime("%b").upper())+" "+str(ex.year),fontsize=35, )

    "setting colors of the cells"
    for i in range(7):
        the_table._cells[i,0]._text.set_color('r')
        the_table._cells[i,6]._text.set_color('b')

    "holiday dates"
    holiday_dates_in_the_month = []
    for i in holidays:
        if int(i[4:6]) == ex.month:
            holiday_dates_in_the_month.append(str(int(i[6:8])))
    "set color of holidays in red"
    for i in holiday_dates_in_the_month:
        index1 = np.where(empty==i)
        the_table._cells[index1[0][0],index1[1][0]]._text.set_color('r')
        
    "figure layout when printing"
    fig.subplots_adjust(left=0.04, bottom=0.06, right=0.96, top=0.86)        
    plt.show()


main(201712)
