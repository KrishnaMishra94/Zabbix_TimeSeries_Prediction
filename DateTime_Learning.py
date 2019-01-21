import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


######### CREATING A DATE RANGE #############
date_rng = pd.date_range(start='1/1/2018',end='1/5/2018',freq='H')

type(date_rng[0])
##########################################

########## CREATING A BASIC DATAFRAME ############
df         = pd.DataFrame(date_rng,columns=['date'])
df['data'] =  np.random.randint(low=0,high=100,size=len(date_rng))

df['date time'] = pd.to_datetime(df['date'])
##################################################

########## CONVERITNG A STRING INTO DATETIME ########## 
import datetime as dt

dt.datetime.strptime('June-01-2018','%B-%d-%Y')
#####################################################


########## SETTING DATETIME INDEX FOR TIME SERIES DATA ##########

df.set_index('date time',inplace=True)
df[df.index.day == 2]
######################################################


######### RESAMPLING OF TIME SERIES DATA ###########
df.resample('D').mean() ## DOWNSAMPLING ON DAILY BASIS
df.resample('W').mean() ## DOWNSAMPLING ON WEEKLY BASIS
#####################################################



######### CREATING A ROLLING WINDOW ###########
df.drop(columns=['date'],axis=1,inplace=True)

df['rolling_sum'] = df.rolling(3).sum()
###############################################

######### CONVERING EPOCH INTO TIMEDATA ##########

epochT = 1548069776
realT = pd.to_datetime(epochT,unit='s')
#################################################
    
