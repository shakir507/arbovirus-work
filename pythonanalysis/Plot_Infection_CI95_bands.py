#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 15:56:52 2022

@author: shakir
"""
import os
import numpy as np
import pandas as pd
import time
import datetime as dt
import matplotlib.dates as mdates

import matplotlib.pyplot as plt


output_directory_base0 =  "../outputdir/"#"unshifted_revisedvaccine/"
NetworkType="Scalefree"
cols1=["Symptomatic"]



sets=["0"]#,'1024']

AllLambda1={}
AllLambda2={}

for fn in sets:
    AllLambda1[fn]=0
    AllLambda2[fn]=0
    
startdate1=dt.date(2020,3,1)

output_directory=output_directory_base0+str(fn)+"/"

modeldata=pd.read_csv(os.path.join(output_directory,"csvContent"+NetworkType+".csv"),index_col=False)

Nodes=list(modeldata.Nodes.unique())

Allnodes={}
for nd in Nodes:
    Allnodes[nd]=modeldata.loc[modeldata.Nodes.isin([nd])].reset_index().drop(['index'],axis=1)['Symptomatic']
AllnodeDF=pd.DataFrame(Allnodes)




DataDates1=[startdate1 + dt.timedelta(days=int(x)) for x in range(1,len(modeldata.loc[modeldata.Nodes.isin([1])])+1)]




plt.figure(figsize=(10,6))
for nd in Nodes:
    plt.plot(DataDates1,AllnodeDF[nd])

plt.title("Newly Infected")
ax=plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
plt.gcf().autofmt_xdate()
plt.show()