#!/usr/bin/env python
import sqlite3
import os
import pandas as pd
import numpy as np
import re
from datetime import datetime
import json

class Buoy_Data(object):
  def __init__(self,datapath):
    self.datapath = datapath

  def read_sql(self,filename):
    conn = sqlite3.connect(filename, timeout=10)
    df = pd.read_sql("SELECT * FROM status",con=conn)
    conn.close()
    return df

  def get_data(self,filename='buoy_data.sqlite.db'):
    
    df = self.read_sql('%s/%s' % (self.datapath, filename))

    df['DATETIME'] = pd.to_datetime(df['DATETIME'])

    df['H']        = df['H'].astype('float')/100.
    df['T']        = df['T'].astype('float')
    df['Tmean']    = df['Tmean'].astype('float')

    df['Temp']     = df['Temp'].astype('float')
    df['Zt']       = df['Zt'].astype('float')

    df['Vm']       = df['Vm'].astype('float')
    df['Dm']       = df['Dm'].astype('float')
    df['Vg']       = df['Vg'].astype('float')
    df['Vms']      = df['Vms'].astype('float')
    df['Vgs']      = df['Vgs'].astype('float')
    df['Zv']       = df['Zv'].astype('float')
   
    df['P']        = df['P'].astype('float')
 
    df['Vmsat']    = df['Vmsat'].astype('float')

    
    with open('%s/%s' % (self.datapath,'buoy_station_name.json'),'r') as outfile:
      name = json.load(outfile)

    # add STN station name variable 
    def label_stname (row):
      if row['ST'] in name:
         return name[row['ST']]['STN']

    df['STN'] = df.apply (lambda row: label_stname(row), axis=1)

    return df

if __name__ == '__main__':
  bd = Buoy_Data('../../') 

  df = bd.get_data()

  # ### filter out bad data
  pdf = df[(~np.isnan(df['Vm'])) & (~np.isnan(df['H']))]

  # ### select target buoy
  stnlist=['新竹浮標','龜山島浮標','臺東外洋浮標','龍洞浮標','小琉球浮標','花蓮浮標','東沙島浮標','馬祖浮標']

  adf = pdf[pdf['STN'].isin(stnlist)]
 
  print(adf)





