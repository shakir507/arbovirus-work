#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 21:40:12 2022

@author: shakir
"""

import os
import numpy as np
import pandas as pd
import time
import datetime as dt
import matplotlib.dates as mdates

import matplotlib.pyplot as plt
import warnings as wr
from get_ConfidenceInterval_rmse_fit import get_95CI_posterior

wr.filterwarnings("ignore")
#---input_directory:Directory where observed data is locate

#---path: the main apth where all output folders are created

#---synthpopDir: Where wardNo_to_zipcode.csv file is located

input_directory = "../calibration-mpi-protobuf_MoreVariants/staticInst/data/synthpops/hills-1p45M/"


path = "../temp6/OneRun_MPI_protobuffOut/"#This is whwere rmse is saved and alsoe the folders where model output is save

path = "../temp6/OneRun_MPI_protobuffOut/output-mpi-1117-50sims_origmask-973days/"


synthpopDir="../calibration-mpi-protobuf/staticInst"

data=pd.read_csv(os.path.join(input_directory,"HillsCases_deaths_hospitals_March1_November10.csv"),parse_dates=['date'])



FIRST_PERIOD = 21
SECOND_PERIOD = 21
THIRD_PERIOD = 42
FOURTH_PERIOD = 42
OE_SECOND_PERIOD = 30



rmse_table=pd.read_csv(os.path.join(path,"param_index_rmse.csv"),index_col=False)
posterior_index=[]
lendata=973

#print(rmse_table)
CI95_full=pd.DataFrame()

r_th=1000

k=0
for i in rmse_table['Index']:
    if rmse_table['RMSE'][k]<r_th and rmse_table['RMSE'][k]>0:
            posterior_index.append(str(rmse_table['Index'][k]))
    k+=1
posterior_index=list(set(posterior_index))
print(len(posterior_index))
if(len(posterior_index)>0):# and r_th<200):
    mn,sd,modl,CI95=get_95CI_posterior(posterior_index,path,lendata) 
    startdate1=data['date'][0]
    CI95['dates']=[startdate1 + dt.timedelta(days=int(x)) for x in range(1,len(CI95)+1)]
    CI95_full=pd.concat([CI95_full,CI95],ignore_index=True)



plt.figure(figsize=(10,6))

plt.plot(CI95_full['dates'],CI95_full['Mean'])
plt.plot(CI95_full['dates'],CI95_full['LL'])
plt.plot(CI95_full['dates'],CI95_full['UL'])
plt.plot(data['date'],data['total cases'])
plt.title("New_Infections_per_day")
ax=plt.gca()

plt.axvline(x = startdate1+dt.timedelta(days=24), color = 'b', label = 'axvline - full height')
plt.axvline(x = startdate1+dt.timedelta(days=24+FIRST_PERIOD), color = 'b', label = 'axvline - full height')
plt.axvline(x = startdate1+dt.timedelta(days=24+FIRST_PERIOD+SECOND_PERIOD), color = 'b', label = 'axvline - full height')
plt.axvline(x = startdate1+dt.timedelta(days=24+FIRST_PERIOD+SECOND_PERIOD+THIRD_PERIOD), color = 'b', label = 'axvline - full height')
plt.axvline(x = startdate1+dt.timedelta(days=24+FIRST_PERIOD+SECOND_PERIOD+THIRD_PERIOD+FOURTH_PERIOD), color = 'b', label = 'axvline - full height')

ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
#plt.xlim(dt.date(2020,3,1), dt.date(2020,10,1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
#plt.ylim(0,100)
#plt.xlim(dt.date(2020,3,1), dt.date(2020,5,1))
plt.gcf().autofmt_xdate()