# Class ORB contains all the methods required for ORB bot
# This class contains methods required for applying and converting the ORB on the intraday data
# 
#
__author__ = "davidraj129@gmail.com"
__version__ = "1.0"


import datetime
import pandas as pd
import numpy as np
import math

class ORB:

    def __init__(self,data):
        
        
        #number of rows per day when 15min candle
        #this need to be automated based on candle frequency
       #self.number_of_rows=26
       #self.number_of_rows=data[data.index.date[0].strftime("%m/%d/%Y")]['High'].count()
        
        u_dates=pd.Series([d.date() for d in data.index]).unique() 
        self.data=data
        self.ORB_parameters=pd.DataFrame(columns=['Date','ORB_High','ORB_Low','Buy_trigger','Short_trigger','Close_3pm','PnL','StopLoss_Hit'],index=range(u_dates.shape[0]))
       #filling the missing values with 0's
        self.ORB_parameters=self.ORB_parameters.fillna(0)
        
       #changing from int to float for more precise calculations
        
        self.ORB_parameters['ORB_High']      = self.ORB_parameters['ORB_High'].astype(float)
        self.ORB_parameters['ORB_Low']       = self.ORB_parameters['ORB_Low'].astype(float)
        self.ORB_parameters['Buy_trigger']   = self.ORB_parameters['Buy_trigger'].astype(float)
        self.ORB_parameters['Short_trigger'] = self.ORB_parameters['Short_trigger'].astype(float)
        self.ORB_parameters['PnL']           = self.ORB_parameters['PnL'].astype(float)
        self.ORB_parameters['Close_3pm']     = self.ORB_parameters['Close_3pm'].astype(float)

    
    ##Private method
    def __get_ORB_parameters(self,intraday_data,index,date):
             
        try:

            intraday_data=intraday_data[intraday_data.index.time<=datetime.time(15,00)].copy()
            
            if intraday_data.empty:
                
                self.ORB_parameters.Date[index]         = pd.to_datetime(date)
                self.ORB_parameters.PnL[index]          = np.nan
                self.ORB_parameters.StopLoss_Hit[index] = np.nan
                self.ORB_parameters.Buy_trigger[index]  = np.nan
                self.ORB_parameters.ORB_High[index]     = np.nan
                self.ORB_parameters.ORB_Low[index]      = np.nan
                self.ORB_parameters.Close_3pm[index]    = np.nan

            else:
                
                self.ORB_parameters.Date[index]      = pd.to_datetime(date)
                self.ORB_parameters.ORB_High[index]  = intraday_data.iloc[0].High
                self.ORB_parameters.ORB_Low[index]   = intraday_data.iloc[0].Low
                self.ORB_parameters.Close_3pm[index] = intraday_data.iloc[-1].Close
            
                if len(intraday_data[intraday_data['Close'].gt(self.ORB_parameters.iloc[index].ORB_High)==True])> 0:
                    self.ORB_parameters.Buy_trigger[index]=self.ORB_parameters.iloc[index].ORB_High               

                
                if len(intraday_data[intraday_data['Close'].lt(self.ORB_parameters.iloc[index].ORB_Low)==True])> 0:
                    self.ORB_parameters.Short_trigger[index]=self.ORB_parameters.iloc[index].ORB_Low                
        
                #Profit or loss calculation
                if self.ORB_parameters.iloc[index].Buy_trigger ==0 and self.ORB_parameters.iloc[index].Short_trigger ==0:
                    self.ORB_parameters.PnL[index]=0
                    self.ORB_parameters.StopLoss_Hit[index]='NA'
                
                elif self.ORB_parameters.iloc[index].Buy_trigger !=0 and self.ORB_parameters.iloc[index].Short_trigger ==0:
                    self.ORB_parameters.PnL[index]=intraday_data.iloc[-1].Close-self.ORB_parameters.iloc[index].Buy_trigger
                    self.ORB_parameters.StopLoss_Hit[index]='No'
                
                elif self.ORB_parameters.iloc[index].Short_trigger !=0 and self.ORB_parameters.iloc[index].Buy_trigger ==0:
                    self.ORB_parameters.PnL[index]=self.ORB_parameters.iloc[index].Short_trigger-intraday_data.iloc[-1].Close
                    self.ORB_parameters.StopLoss_Hit[index]='No'
                
                elif self.ORB_parameters.iloc[index].Buy_trigger !=0 and self.ORB_parameters.iloc[index].Short_trigger !=0:
                    self.ORB_parameters.StopLoss_Hit[index]='Yes'
                    self.ORB_parameters.PnL[index]=self.ORB_parameters.iloc[index].Short_trigger- self.ORB_parameters.iloc[index].Buy_trigger
                
        except NameError:
            print ("This variable is not defined") 
    
    ##Public method
    def get_ORB_parameters(self):
        #make using of the method written with the slicing logic to get ORB_parameters df
        u_dates=pd.Series([d.date() for d in self.data.index]).unique()
        #for i in u_dates:
             #n=self.data[i.strftime("%m/%d/%Y")]['High'].count()
             #[self.__get_ORB_parameters(self.data[i:i+n],math.floor(i/n)) for i in range(0,self.data.shape[0],n)]
        [self.__get_ORB_parameters(self.data[val.strftime("%m/%d/%Y")],idx,val) for idx, val in enumerate(u_dates)]
        return self.ORB_parameters

class resample:

    def __init__(self,timedelta):
        
        self.timedelta=timedelta
        
    def resample_stock_data(self,data): 
        # make a copy
        data1 = data.copy()
        # sort the index (evidently required by resample())
        data1 = data1.sort_index()
        aggregation_dict = {'High': 'max','Low': 'min'}


        return (data1.resample(self.timedelta).agg(aggregation_dict))  
  