import CommonFunctions as cf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
import statsmodels.api as sm

os.listdir()
######### LOADING ZABBIX DATA ##############

trends = pd.read_csv('ZABBIX_TRENDS.csv')
trends_orig = trends.copy()
########################################


######### EXPLORATORY DATA ANALYSIS ############

## CHECK FOR MISSING VALUES
cf.draw_null_values_table(trends)

## CONVERTING EPOCH TO DATETIME
trends['DateTime'] = pd.to_datetime(trends['clock'],unit='s')

## SETTING INDEX TO DATETIME
trends = trends.set_index(trends['DateTime'])

## SELECTING MARCH MONTH'S DATA
trends_march = trends.loc['2018-03-01':'2018-03-31']

## SELECTING NECESSARY COLUMNS
trends_march = trends_march.loc[:,['value_avg']]

## RE-SAMPLING BASED ON DAY
trends_march = trends_march.resample('D').mean()
####################################################


############## DATA VISUALIZATION ####################

## PLOT THE ORIGINAL DATA
trends_march.plot(figsize=(15,9),legend=True)
plt.legend(['ITEM VALUES'])
plt.savefig('Items_Plot.png')

## PLOTTING SMOOTHED VERSION OF DATA  
plt.figure(figsize=(15,9))
trends_rolling = trends_march['value_avg'].rolling('3D').mean()
trends_march.plot(legend=True)
trends_rolling.plot(legend=True)
plt.legend(['Original Data','Smoothed Data'])
plt.savefig('Original_Vs_Smoothed.png')


## PLOTTING ACF & PACF PLOTS
plot_acf(trends_march['value_avg'],lags=30,title="ACF Plot For Zabbix Item Value For March")
plt.savefig('ACF_PLOT.png')

plot_pacf(trends_march['value_avg'],lags=30,title="PACF Plot Zabbix Item Value For March")
plt.savefig('PACF_PLOT.png')

## PLOTTING TRENDS, SEASONALITY, RESIDUAL
decomposed_trends = sm.tsa.seasonal_decompose(trends_march['value_avg'],freq=10)
decomposed_trends.plot()
plt.savefig('Decomposed_Series.png')

#######################################################












