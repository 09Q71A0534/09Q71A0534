#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 22:42:41 2021

@author: david
"""

import requests
import pandas as pd
from datetime import timedelta

class IntradayDownloader:
    
     def __init__(self,**kwargs):
         
         self.user  = kwargs['user']
         self.token = kwargs['token']
         self.timeframe =kwargs['timeframe']
         self.authtoken =kwargs['authtoken'] 
    
     def __get_intraday_data(self,from_date,to_date):
         headers={'Authorization': self.authtoken}    
         url=f'https://kite.zerodha.com/oms/instruments/historical/{self.token}/{self.timeframe}?user_id={self.user}&oi=1&from={from_date}&to={to_date}'
         resJson=requests.get(url,headers=headers).json()
         candleinfo=resJson['data']['candles']
         columns=['timestamp','Open','High','Low','Close','V','OI']
         df=pd.DataFrame(candleinfo,columns=columns)
         return df
    
     def get_intraday_data(self,start_date,end_date):
         
         columns=['timestamp','Open','High','Low','Close','V','OI']
         year_data=pd.DataFrame(columns=columns)

         from_date=start_date
         while from_date< end_date:
             to_date=from_date+timedelta(days=30)
             #print(from_date,to_date)
             month_data=self.__get_intraday_data(from_date,to_date)
             year_data=year_data.append(month_data)
             from_date=from_date+timedelta(days=31)
         return year_data   

