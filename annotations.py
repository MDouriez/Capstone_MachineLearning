# Authors: Berengere Duverneuil, Marie Douriez
# coding: utf-8


import pandas as pd
import datetime
import numpy as np


def start_format(row):
    if isinstance(row['Start'],datetime.datetime):                 # if already Y-M-D HH:MM:SS
        return row['Start']                                        # return itself
    else:
        return datetime.datetime.combine(row['Day'],row['Start'])  # else convert

def end_format(row):
    if isinstance(row['End'],datetime.datetime):
        return row['End']
    else:
        return datetime.datetime.combine(row['Day'],row['End'])


fileIn = 'Annotations Capstone 2.xlsx'


### Preprocessing Bathroom
shower_time = 5 # time (in minutes to shower)

df_bath = pd.read_excel(fileIn,'Bathroom', 3, parse_cols='A:D')   # reading the excel file
df_bath.head()

df_bath['Day'] = df_bath['Day'].fillna(method='ffill')  # filling NaT day values with the current day
df_bath['Start'] = df_bath.apply(start_format,axis=1)   # converting to Y-M-D HH:MM:SS

df_bath.loc[df_bath.Activity == 'T','End'] = df_bath.loc[df_bath.Activity == 'T','Start']   # 1 min to flush
df_bath.loc[df_bath.Activity == 'S','End'] = df_bath.loc[df_bath.Activity == 'S','Start'] + datetime.timedelta(minutes=shower_time)

df_bath['End'] = pd.to_datetime(df_bath['End']) # converting to Y-M-D HH:MM:SS
df_bath = df_bath[['Start','End','Activity']]    # dropping the day
df_bath['Activity'] = df_bath['Activity'].replace(['T','S'],['Toilet','Shower'])

df_bath['Pres_bath'] = pd.Series(1., index=df_bath.index)


### Preprocessing Bedroom

df_bed = pd.read_excel(fileIn, 'Bedroom', 2, parse_cols='A:D')   # reading the excel file


df_bed['Day'] = df_bed['Day'].fillna(method='ffill')  # filling NaT day values with the current day
df_bed['Start'] = df_bed.apply(start_format,axis=1)   # converting to Y-M-D HH:MM:SS

df_bed.loc[df_bed.End.notnull(),'End'] = df_bed[df_bed.End.notnull()].apply(end_format,axis=1)

df_bed.loc[df_bed.Activity == 'C','End'] = df_bed.loc[df_bed.Activity == 'C','Start'] + datetime.timedelta(minutes=2)
df_bed['End'] = pd.to_datetime(df_bed['End'])         # converting to Y-M-D HH:MM:SS
df_bed = df_bed[['Start','End','Activity']]           # dropping the day
df_bed['Activity'] = df_bed['Activity'].replace(['C','B'],['Other','Sleep'])

df_bed['Pres_bed'] = pd.Series(1., index=df_bed.index)


### Preprocessing kitchen

df_kitch = pd.read_excel(fileIn,'Kitchen',3,parse_cols='A:D')   # reading the excel file


# filling NaT day values with the current day
df_kitch['Day'] = df_kitch['Day'].fillna(method='ffill')
df_kitch['Start'] = df_kitch.apply(start_format,axis=1)                              # converting to Y-M-D HH:MM:SS
df_kitch.loc[df_kitch.End.notnull(),'End'] = df_kitch[df_kitch.End.notnull()].apply(end_format,axis=1)
df_kitch['End'] = pd.to_datetime(df_kitch['End'])                                    # converting to Y-M-D HH:MM:SS
delta_cook = np.mean(df_kitch['End']-df_kitch['Start'])                              # average cooking time
# filling the missing end times
df_kitch.loc[df_kitch.End.isnull(),'End'] = df_kitch.loc[df_kitch.End.isnull(),'Start'] + delta_cook 
df_kitch = df_kitch[['Start','End','Activity']]                                        # dropping the day
df_kitch['Activity'] = 'Cook'


df_kitch2 = df_kitch.copy()                                     # add eating
df_kitch2.index = df_kitch.index + len(df_kitch.index)          # no overlapping of indices
df_kitch2['Start'] = df_kitch2['End']                           # eating starts at the end of cooking
df_kitch2['End'] = df_kitch2['Start'] + datetime.timedelta(minutes=15)   # eating takes an average of 15 min
df_kitch2['Activity'] = 'Eat'
df_kitch = pd.concat([df_kitch, df_kitch2])

df_kitch['Pres_kitch'] = pd.Series(1., index=df_kitch.index)


df_kitch.head()


### Final dataframe

#start_date = '20/02/2016 00:01:00'
#end_date = '2016-03-18 20:57:00'

start_date = min (min(df_kitch['Start']), min(df_bed['Start']), min(df_bath['Start'])) - datetime.timedelta(minutes=5)

max_bed = max(df_bed['End'])
max_kitch = max(df_kitch['End'])
max_bath = max(df_bath['End'])
end_date = max([max_bed, max_kitch, max_bath]) + datetime.timedelta(minutes=5)

print "start:", start_date, "end:", end_date


#days=14
#periods = days*24*60 # number of periods: 2 weeks with a frequency of 1 min
#rng = pd.date_range(start = start_date, periods=periods, freq='min')

rng = pd.date_range(start = start_date, end = end_date, freq='min')
df = pd.Series('Other', index=rng, name='Activity')    # default activity is 'Other'
df = pd.DataFrame(df)


df['Pres_bath'] = pd.Series(0, index=df.index)
df['Pres_bed'] = pd.Series(0, index=df.index)
df['Pres_kitch'] = pd.Series(0, index=df.index)
df.head()


## filling in the values in df



# Bathroom activities
for i in range(0,len(df_bath.index)):
    start = df_bath.loc[i,'Start']
    end = df_bath.loc[i,'End']
    time_index = (df.index >= start) & (df.index <= end)
    df.loc[time_index,'Activity'] = df_bath.loc[i,'Activity']

    # adding noise
    bf_S = 1
    af_S = 2
    bf_T = 1
    af_T = 1
    if df_bath.loc[i, 'Activity'] == 'Shower':
        time_index_noise = (df.index >= start - datetime.timedelta(minutes=bf_S)) & (df.index <= end + datetime.timedelta(minutes=af_S))
    if df_bath.loc[i, 'Activity'] == 'Toilet':
        time_index_noise = (df.index >= start - datetime.timedelta(minutes=bf_T)) & (df.index <= end + datetime.timedelta(minutes=af_T))
    df.loc[time_index_noise,'Pres_bath'] = 1

# Bedroom activities
for i in range(0,len(df_bed.index)):
    start = df_bed.loc[i, 'Start']
    end = df_bed.loc[i, 'End']
    time_index = (df.index >= start) & (df.index <= end)
    df.loc[time_index, 'Activity'] = df_bed.loc[i,'Activity']

    # adding noise
    bf_B = 5
    af_B = 1
    if df_bed.loc[i,'Activity'] == 'Sleep':
        time_index_noise = (df.index >= start - datetime.timedelta(minutes=bf_B)) & (df.index <= end + datetime.timedelta(minutes=af_B))
        df.loc[time_index_noise,'Pres_bed'] = 1
    else:
        df.loc[time_index,'Pres_bed'] = 1

# Kitchen activities
for i in range(0,len(df_kitch.index)):
    start = df_kitch.loc[i,'Start']
    end = df_kitch.loc[i,'End']
    time_index = (df.index >= start) & (df.index <= end)
    df.loc[time_index,'Activity'] = df_kitch.loc[i,'Activity']

    bf_cook = 2
    af_cook = 2
    if df_kitch.loc[i,'Activity'] == 'Cook':
        time_index_noise = (df.index >= start - datetime.timedelta(minutes=bf_cook)) & (df.index <= end + datetime.timedelta(minutes=af_cook))
        df.loc[time_index_noise,'Pres_kitch'] = 1
    if df_kitch.loc[i,'Activity'] == 'Eat':
        #print df.index[time_index]
        df.loc[time_index,'Pres_bed'] = 1 # eating in bedroom


y = df['Activity']
presence = df[['Pres_bath', 'Pres_kitch', 'Pres_bed']]

# export to csv files
presence.to_csv("presence_alldata.csv")
y.to_csv('y_alldata.csv')

print "Success"





