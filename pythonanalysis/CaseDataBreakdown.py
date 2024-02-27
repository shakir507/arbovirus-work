#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 10:35:30 2022

@author: shakir
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import os

input_directory = "../../InputFiles/Senegal/"#be sure to block this line for full population test


datainput=pd.read_csv(os.path.join(input_directory,'InputCasesData.csv'),parse_dates=['date'])

output_directory_base0 =  "../outputdir/SequentialFitting/"#"unshifted_revisedvaccine/"

for nsd in range(1,41):
    
    output_directory_base =  output_directory_base0 +"piece_"+str(nsd)+"/"
    os.system("mkdir -p " + output_directory_base)
    
tl=1
for nsd in range(1,29):
    
    output_directory_base =  output_directory_base0 +"piece_"+str(nsd)+"/"
    
    tu=tl+30
    timerange=list(np.arange(tl,tu,1))
    data1=datainput.loc[datainput.time_step.isin(timerange)].reset_index()
    data1=data1.drop(['index'],axis=1)
    data1.to_csv(os.path.join(output_directory_base,'casesfile_'+str(nsd)+'.csv'),index=False)
    tl+=30