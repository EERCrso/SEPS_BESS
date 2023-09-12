from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import baterry
import functions


cum_times=[3,3,3,3,3,3,3,3,5,5,5,5,5,5,5,5,10,10,10,10,10,10,10,10,15,15,15,15,15,15,15,15]
MWinstal=[5,7.5,10,12.5,15,20,25,30,5,7.5,10,12.5,15,20,25,30,5,7.5,10,12.5,15,20,25,30,5,7.5,10,12.5,15,20,25,30]
MWHrated=[150,140,130,125,120,115,110,105,100,95,90,85,80,75,70,65,60,55,50,45,40,35,30,25,20]

cum_times=[10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10]
MWinstal=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
MWHrated=[40,35,30,25,20,15,10,5]


cum_time_list=list()
MW_list=list()
MWh_list=list()
mean1=list()
std1=list()
max1=list()
mean5=list()
std5=list()
max5=list()


#empty_dataframe = pd.DataFrame(columns=['cum_time', 'MW', 'MWH','mean1','std1','max1','mean5','std5','max5'])
result= pd.DataFrame()

for cum_index, cum_item in enumerate(cum_times):

    for MWh_index, MWh_item in enumerate(MWHrated):


        df=pd.read_csv('priebeh_t' + str(cum_item) + '_MW' + str(MWinstal[cum_index]) + '_MWh' + str(
            MWh_item) + '.csv',sep=";")
        #filter day
        is_day=is_2002 =  df['0']> 0.013
        df_day=df[is_day]

        #1 min diff
        df_day_1min=df_day.shift(periods=1)
        df_1min_diff=abs(df_day-df_day_1min)
        mean_1 = df_1min_diff['0'].mean()
        #median_1 = df_1min_diff['0'].median()
        std_1 = df_1min_diff['0'].std()
        maximum_1=df_1min_diff.max()


        #5 min diff
        df_day_5min=df_day.shift(periods=40)
        df_5min_diff=abs(df_day-df_day_5min)
        mean_5 = df_5min_diff['0'].mean()
        #median_5 = df_5min_diff['0'].median()
        std_5 = df_5min_diff['0'].std()
        maximum_5=df_5min_diff.max()

        cum_time_list.append(cum_item)
        MW_list.append(MWinstal[cum_index])
        MWh_list.append(MWh_item)
        mean1.append(mean_1)
        std1.append(std_1)
        max1.append(maximum_1[0])
        mean5.append(mean_5)
        std5.append(std_5)
        max5.append(maximum_5[0])


result['cum_time']=cum_time_list
result['MW']=MW_list
result['MWH']=MWh_list
result['mean1']=mean1
result['std1']=std1
result['max1']=max1
result['mean5']=mean5
result['std5']=std5
result['max5']=max5

result.to_csv('res_diff.csv', index = False, encoding='utf-8',sep=';')