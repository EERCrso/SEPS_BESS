import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import seaborn as sns


hourlist=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
pd.set_option('display.max_columns', 100)  # or 1000
pd.set_option('display.max_rows', 50)  # or 1000
pd.set_option('display.max_colwidth', -1)  # or 199



#inicializacia data
df=pd.read_csv("FVE_2021_1MIN_FULL_NO_DIFF.csv",sep=";")
print(df)




print('.....')
#month grouping
print('.....')
# df_month = df.groupby('month').sum()
# df_month=df_month/60
# df_month.to_csv('FVE_2021_groupped_month.csv', index = False, encoding='utf-8',sep=';')
print('.....')
#day grouping
print('.....')
# df_day = df.groupby('day').sum()
# df_day=df_day/60
# df_day.to_csv('FVE_2021_groupped_day.csv', index = False, encoding='utf-8',sep=';')
print('.....')
#HOur grouping
print('.....')
df["hour_month_day"] = df["hour"].astype(str) +'_'+ df["month"].astype(str) + '_' + df["day"].astype(str)
print(df)
df_hour = df.groupby(["month","day",'hour']).agg('max')
jan= [1]*24*31
feb= [2]*24*28
mac= [3]*24*31
aprl= [4]*24*30
maj= [5]*24*31
jun= [6]*24*30
jul= [7]*24*31
au= [8]*24*31
sept= [9]*24*30
oct= [10]*24*31
nov= [11]*24*30
dec= [12]*24*31

janh= hourlist*31
febh= hourlist*28
mach= hourlist*31
aprlh= hourlist*30
majh= hourlist*31
junh= hourlist*30
julh= hourlist*31
auh= hourlist*31
septh= hourlist*30
octh= hourlist*31
novh= hourlist*30
dech= hourlist*31

#df_hour=df_hour/60
mesiac =  jan + feb + mac+aprl+maj+jun+jul+au+sept+oct+nov+dec
hodina = janh + febh + mach+aprlh+majh+junh+julh+auh+septh+octh+novh+dech

print(mesiac)
df_hour["mesiac"] = mesiac
df_hour["hodina"] = hodina

data = pd.DataFrame(data={'x':df_hour["mesiac"], 'y':df_hour["hodina"], 'z':df_hour["SR"]})
data = data.pivot(index='x', columns='y', values='z')
sns.heatmap(data)
plt.show()

#df_hour.to_csv('FVE_2021_groupped_hour_max.csv', index = False, encoding='utf-8',sep=';')
