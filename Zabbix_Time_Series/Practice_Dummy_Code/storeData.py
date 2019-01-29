import CommonFunctions as cf
import pandas as pd
import os
import seaborn as sns

os.listdir()


######### LOADING EXCEL DATA ########
data = pd.read_excel('Sample - Superstore.xls')
#####################################

######## INSPECTING DATA ##########
data.head()
data.shape
data.iloc[:,0:8].head()
data.iloc[:,8:15].head()
data.iloc[:,15:].head()
##################################


####### WORKING ONLY ON Furniture CATEGORY DATA #########
data['Category'].value_counts()

furnData = data[data['Category'] == 'Furniture']

furnData.iloc[:,0:8].head()
furnData.iloc[:,8:15].head()
furnData.iloc[:,15:].head()
#########################################################

######## CHECK FOR MISSING VALUES ##########
cf.draw_null_values_table(furnData)
##NO MISSING VALUES FOUND
############################################


######## CREATING NEW DATE VARIABLES #############
furnData['Order Date'].min()
furnData['Order Date'].max()

furnData['Order Date Year'] = furnData['Order Date'].dt.year
furnData['Order Date Month'] = furnData['Order Date'].dt.month
furnData['Order Date Day'] = furnData['Order Date'].dt.day


furnData.drop(columns=['Category'],inplace=True)
##################################################


########### LESS IMP COLUMNS ARE REMOVED ################
# =============================================================================
# Order ID
# Customer Name
# Country
# City
# State
# Region
# Product Name
# =============================================================================

cols = ['Row ID','Quantity','Profit','Discount','Ship Date','Ship Mode','Order ID','Customer Name','Country','City','State','Region','Product Name']
furnData.drop(columns=cols,axis=1,inplace=True)
########################################################


############ GROUPING SALES DATA BASED ON ORDER DATE ######
furnData['Order Date'].value_counts()
furnGrouped = furnData.groupby('Order Date')['Sales'].sum().reset_index()
furnGrouped.index

furnGrouped = furnGrouped.set_index('Order Date')
##########################################################

#################### RESAMPLING ######################
furnSampled = furnGrouped['Sales'].resample('MS').mean()

furnSampled['2016':]
######################################################

furnSampled.plot(figsize=(14,3))

################## VISUALIZING TREND & SEASONALITY #######






















