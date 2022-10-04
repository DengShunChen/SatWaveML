#!/usr/bin/env python
import os
import matplotlib.pyplot as plt
from netCDF4 import Dataset as netcdf_dataset
import numpy as np
import pandas as pd
from calendar import month_name
from cartopy import config, feature
import cartopy.crs as ccrs
from argparse import ArgumentParser,ArgumentDefaultsHelpFormatter
from datetime import datetime

class read_ccmp(object):
  def __init__(self,version):
    self.version = version
    self.hours=['00Z', '06Z', '12Z', '18Z']
      
  def get_data(self,var):
    self.fillvalue = getattr(self.dataset.variables[var],'_FillValue')
    self.units = getattr(self.dataset.variables[var],'units')
    self.long_name  = getattr(self.dataset.variables[var], 'long_name')
    self.lats = self.dataset.variables['latitude'][:]
    self.lons = self.dataset.variables['longitude'][:]

    data = self.dataset.variables[var][:,:,:]
    no_data = np.where(data == self.fillvalue)
    data[no_data] = np.nan
    return data

  def read_nc(self,strdate):
    year  = strdate[0:4]
    month = strdate[4:6]
    day   = strdate[6:8]
  
    fname = "v0%s.NRT/Y%s/M%s/CCMP_RT_Wind_Analysis_%s%s%s_V0%s_L3.0_RSS.nc" % (self.version,year,month,year,month,day,self.version)
    #fname = " http://data.remss.com/ccmp/v0%s.NRT/Y%s/M%s/CCMP_RT_Wind_Analysis_%s%s%s_V0%s_L3.0_RSS.nc" % (version,year,month,year,month,day,version)
    print(fname)
    self.file_exist = os.path.isfile(fname)  
    if not self.file_exist:
      return 
    
    self.dataset = netcdf_dataset(fname)
    
    self.uwnd = self.get_data('uwnd')
    self.vwnd = self.get_data('vwnd')

    self.data = np.sqrt(np.power(self.uwnd,2) + np.power(self.vwnd,2))  
    return self.data  


  def plot_map(self,strdate,hour,data,subfix=''):
    year  = strdate[0:4]
    month = strdate[4:6]
    day   = strdate[6:8]

    self.ihour = self.hours.index(hour)
    fig = plt.figure(facecolor='white')
    
    #ax = plt.axes(projection=ccrs.PlateCarree())
    ax = plt.axes(projection=ccrs.Orthographic(120, 23.5))
    #ax.add_feature(feature.OCEAN, zorder=0)
    #ax.add_feature(feature.LAND, zorder=0, edgecolor='black')
    
    ax.set_global()
    ax.gridlines()
    
    vmax=30
    vmin=0
    interval = 0.5
    cbarticks = np.arange(vmin,vmax+interval,interval)
    im = plt.contourf(self.lons, self.lats, data[self.ihour,:,:], cbarticks, cmap='coolwarm',transform=ccrs.PlateCarree(), vmin=-vmax, vmax=vmax)
    
    ax.coastlines()
    
    interval = interval*2
    cbar = plt.colorbar(im, ax=ax, ticks=np.arange(vmin,vmax+interval,interval))
    cbar.set_label(self.units)
    
    title = 'total wind speed at 10 meters' + ' for ' + month_name[int(month)] + ' ' + day + ', ' + year + ' at ' + hour
#    title = self.long_name + ' for ' + month_name[int(month)] + ' ' + day + ', ' + year + ' at ' + hour
    plt.title(title, fontsize='medium')
    
    filename='ccmp_L3_%s%s%s_%s%s.png' % (year,month,day,hour,subfix)
    fig.savefig(filename)
    plt.show()
    plt.close()

  def plot_map_diff(self,strdate,hour,data,subfix='',vmax=4,vmin=-4,interval=0.1):
    year  = strdate[0:4]
    month = strdate[4:6]
    day   = strdate[6:8]

    self.ihour = self.hours.index(hour)
    fig = plt.figure(facecolor='white')

    #ax = plt.axes(projection=ccrs.PlateCarree())
    ax = plt.axes(projection=ccrs.Orthographic(120, 23.5))
    #ax.add_feature(feature.OCEAN, zorder=0)
    #ax.add_feature(feature.LAND, zorder=0, edgecolor='black')

    ax.set_global()
    ax.gridlines()

    cbarticks = np.arange(vmin,vmax+interval,interval)
    im = plt.contourf(self.lons, self.lats, data[self.ihour,:,:], cbarticks, cmap='coolwarm',transform=ccrs.PlateCarree(), vmin=vmin, vmax=vmax)

    ax.coastlines()

    interval = interval*2
    cbar = plt.colorbar(im, ax=ax, ticks=np.arange(vmin,vmax+interval,interval))
    cbar.set_label(self.units)

    title = 'total wind speed at 10 meters' + ' for ' + month_name[int(month)] + ' ' + day + ', ' + year + ' at ' + hour
#    title = self.long_name + ' for ' + month_name[int(month)] + ' ' + day + ', ' + year + ' at ' + hour
    plt.title(title, fontsize='medium')

    filename='ccmp_L3_%s%s%s_%s%s.png' % (year,month,day,hour,subfix)
    fig.savefig(filename)
    plt.show()
    plt.close()

  def plot_H10(self,strdate,hour,data,subfix='',cmap='coolwarm',vmax=10,vmin=0,interval=0.25):
    year  = strdate[0:4]
    month = strdate[4:6]
    day   = strdate[6:8]

    self.ihour = self.hours.index(hour)
    fig = plt.figure(figsize=(16,8),dpi=200,facecolor='white')

    ax = plt.axes(projection=ccrs.PlateCarree())
    #ax = plt.axes(projection=ccrs.Orthographic(120, 23.5))
    #ax.add_feature(feature.OCEAN, zorder=0)
    ax.add_feature(feature.LAND, zorder=1, edgecolor='black', facecolor='black')

    #ax.set_global()
    ax.set_extent([116.0, 125.5, 20.5, 27.0], ccrs.PlateCarree())

    ax.gridlines()

    cbarticks = np.arange(vmin,vmax+interval,interval)
    im = plt.contourf(self.lons, self.lats, data[self.ihour,:,:], cbarticks, cmap=cmap,transform=ccrs.PlateCarree(), vmin=vmin, vmax=vmax)

    ax.coastlines()

    interval = interval*2
    cbar = plt.colorbar(im, ax=ax, ticks=np.arange(vmin,vmax+interval,interval))
    cbar.set_label('meters')

    title = 'Retrieved Significant Wave Height' + ' for ' + month_name[int(month)] + ' ' + day + ', ' + year + ' at ' + hour
#    title = self.long_name + ' for ' + month_name[int(month)] + ' ' + day + ', ' + year + ' at ' + hour
    plt.title(title, fontsize='medium')

    filename='ccmp_L3_H_%s%s%s_%s%s.png' % (year,month,day,hour,subfix)
    fig.savefig(filename,dpi=200)
    plt.show()
    plt.close()

  def plot_Vmsat(self,strdate,hour,data,subfix='',cmap='coolwarm'):
    year  = strdate[0:4]
    month = strdate[4:6]
    day   = strdate[6:8]

    self.ihour = self.hours.index(hour)
    fig = plt.figure(figsize=(16,8),dpi=200,facecolor='white')

    ax = plt.axes(projection=ccrs.PlateCarree())
    #ax = plt.axes(projection=ccrs.Orthographic(120, 23.5))
    #ax.add_feature(feature.OCEAN, zorder=0)
    ax.add_feature(feature.LAND, zorder=1, edgecolor='black', facecolor='black')

    #ax.set_global()
    ax.set_extent([116.0, 125.5, 20.5, 27.0], ccrs.PlateCarree())

    ax.gridlines()

    vmax=25
    vmin=0
    interval = 0.5
    cbarticks = np.arange(vmin,vmax+interval,interval)
    im = plt.contourf(self.lons, self.lats, data[self.ihour,:,:], cbarticks, cmap=cmap,transform=ccrs.PlateCarree(), vmin=vmin, vmax=vmax)

    ax.coastlines()

    interval = interval*2
    cbar = plt.colorbar(im, ax=ax, ticks=np.arange(vmin,vmax+interval,interval))
    cbar.set_label(self.units)

    title = 'total wind speed at 10 meters' + ' for ' + month_name[int(month)] + ' ' + day + ', ' + year + ' at ' + hour
#    title = self.long_name + ' for ' + month_name[int(month)] + ' ' + day + ', ' + year + ' at ' + hour
    plt.title(title, fontsize='medium')

    filename='ccmp_L3_Vmsat_%s%s%s_%s%s.png' % (year,month,day,hour,subfix)
    fig.savefig(filename,dpi=200)
    plt.show()
    plt.close()

if __name__ == '__main__':

  parser = ArgumentParser(description = 'Plot CCMP wind maps',formatter_class=ArgumentDefaultsHelpFormatter)
  parser.add_argument('-b','--begin_date',help='beginning date',type=str,metavar='YYYYMMDD',required=True)
  parser.add_argument('-e','--end_date',help='ending date',type=str,metavar='YYYYMMDD',default=None,required=False)
  parser.add_argument('-v','--version',help='version',type=str,default='2.1',required=False)

  args = parser.parse_args()
  bdate = datetime.strptime(args.begin_date,'%Y%m%d')
  edate = bdate if args.end_date is None else datetime.strptime(args.end_date,'%Y%m%d')
  version=args.version

  ccmp = read_ccmp(version)
  
  for adate in pd.date_range(bdate,edate,freq='24H'):
    sdate = adate.strftime('%Y%m%d')
    data = ccmp.read_nc(sdate)
    for hour in ccmp.hours:
      print(sdate,' ',hour) 
      ccmp.plot_map(sdate,hour,data)

