import CommonFunctions as cf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import itertools
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf ## FOR ACF & PACF PLOTS
import statsmodels.api as sm ## FOR SARIMAX MODEL
from statsmodels.tsa.arima_model import ARMA ## FOR ARMA MODEL
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import MySQLdb

os.listdir()
######## LOADING ZABBIX DATA ##############

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


############## GRID SEARCH FOR ARIMA MODEL ###############

p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

for param in pdq:
    for seasonal_param in seasonal_pdq:
        try:
            model = sm.tsa.statespace.SARIMAX(trends_march,
                                              order = param,
                                              seasonal_order = seasonal_param,
                                              enforce_stationarity=False,
                                              enforce_invertibility=False)
           
            results = model.fit()
               
            print('ARIMA {}x{} - AIC:{}'.format(param,seasonal_param,results.aic))
        except:
            print('------------------ ISSUE ------------------')


# (1, 0, 0)x(0, 0, 0, 12) - AIC:-483.9370490284733
############################################################
            
############## SARIMAX MODEL IMPLMEMENTATION ################            

model = sm.tsa.statespace.SARIMAX(trends_march,
                                  order = (1, 1, 1),
                                  seasonal_order = (1, 1, 0, 12),
                                  enforce_stationarity=False,
                                  enforce_invertibility=False)
           
results = model.fit()

pred = results.get_prediction(start=pd.to_datetime('2018-04-01'),end=pd.to_datetime('2018-04-30'), dynamic=False)
pred_ci = pred.conf_int()

ax = trends_march.plot(label='observed')
  
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)
plt.show()
##############################################################






