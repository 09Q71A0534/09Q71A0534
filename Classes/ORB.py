# Class ORB contains all the methods required for ORB bot
# This class contains methods required for applying and converting the ORB on the intraday data
# 
#
__author__ = "davidraj129@gmail.com"
__version__ = "1.0"


import pandas as pd
import math

class ORB:

    def __init__(self,data):
        #number of rows per day when 15min candle
        #this need to be automated based on candle frequency
       self.number_of_rows=26
       
       self.data=data
       self.ORB_parameters=pd.DataFrame(columns=['Date','ORB_High','ORB_Low','Buy_trigger','Short_trigger','Close_3pm','PnL','StopLoss_Hit'],index=range(round(len(data)/26)))
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
    def __get_ORB_parameters(self,intraday_data,index):
             
        try:

            intraday_data=intraday_data.iloc[:-3].copy()#Intraday drop last 3 rows in the dataframe i.e (3pm and above)
            
            ##not a efficient way to use copy method need to find alternatives
        
            #First row contains ORB High and ORB Low
        
            #ORB_parameters.iloc[index].Date    = intraday_data.index[0]
            #ORB_parameters.iloc[index].ORB_High= intraday_data.iloc[0].High
            #ORB_parameters.iloc[index].ORB_Low = intraday_data.iloc[0].Low
            #iloc doesn't work for assignments

            self.ORB_parameters.Date[index]      = intraday_data.index.date[0]
            self.ORB_parameters.ORB_High[index]  = intraday_data.iloc[0].High
            self.ORB_parameters.ORB_Low[index]   = intraday_data.iloc[0].Low
            self.ORB_parameters.Close_3pm[index] = intraday_data.iloc[-1].Close
            
            if len(intraday_data[intraday_data['Close'].gt(self.ORB_parameters.iloc[index].ORB_High)==True])> 0:
                
                self.ORB_parameters.Buy_trigger[index]=intraday_data[intraday_data['Close'].gt(self.ORB_parameters.iloc[index].ORB_High)==True].iloc[0]['Close']
                
            if len(intraday_data[intraday_data['Close'].lt(self.ORB_parameters.iloc[index].ORB_Low)==True])> 0:
                
                self.ORB_parameters.Short_trigger[index]=intraday_data[intraday_data['Close'].lt(self.ORB_parameters.iloc[index].ORB_Low)==True].iloc[0]['Close']
        
            #Profit or loss calculation
            if self.ORB_parameters.iloc[index].Buy_trigger ==0 and self.ORB_parameters.iloc[index].Short_trigger ==0:
                
                self.ORB_parameters.PnL[index]=0
                
            elif self.ORB_parameters.iloc[index].Buy_trigger !=0:
                
                self.ORB_parameters.PnL[index]=intraday_data.iloc[-1].Close-self.ORB_parameters.iloc[index].Buy_trigger
                
            elif self.ORB_parameters.iloc[index].Short_trigger !=0:
                
                self.ORB_parameters.PnL[index]=self.ORB_parameters.iloc[index].Short_trigger-intraday_data.iloc[-1].Close  
            
            #column stoploss triggered
            if self.ORB_parameters.iloc[index].Buy_trigger !=0 and self.ORB_parameters.iloc[index].Short_trigger !=0:
                
                self.ORB_parameters.StopLoss_Hit[index]='Yes'
                
            else:
                if self.ORB_parameters.iloc[index].Buy_trigger ==0 and self.ORB_parameters.iloc[index].Short_trigger ==0:
                    
                    self.ORB_parameters.StopLoss_Hit[index]='NA'
                    
                else:
                    
                    self.ORB_parameters.StopLoss_Hit[index]='No'
            
                
        except NameError:
            print ("This variable is not defined") 
    
    ##Public method
    def get_ORB_parameters(self):
        #make using of the method written with the slicing logic to get ORB_parameters df
        n = self.number_of_rows  #chunk row size
        [self.__get_ORB_parameters(self.data[i:i+n],math.floor(i/n)) for i in range(0,self.data.shape[0],n)]

        return self.ORB_parameters
      
  