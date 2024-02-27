#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 21:52:13 2022

@author: shakir
"""

#Run this code to plot confidence intervals using simulator output data based on best RMSE values.  
#It takes the indices for best rmse values from a table, reads outputs from folders according to indices and resturns a confidence interval.
#This is helpful in looking at the trends shown by the simulator across all the parameters in the prior distribution

import os
import numpy as np
import pandas as pd
import time

def get_95CI_posterior(posterior_index,output_directory_base,lendata):

    n_params=len(posterior_index)

    simdata=np.zeros(lendata)
    allmodels=pd.DataFrame()
    for i in posterior_index:
        output_directory =  output_directory_base +"piece_1/"+str(int(i))+"/"

        if(os.path.exists(os.path.join(output_directory,"infections_from_new_strain0_973.csv"))):
            modeldata=pd.read_csv(os.path.join(output_directory,"infections_from_new_strain0_973.csv"),index_col=False)
            
           
            # modeldata=modeldata['num_infected']
            # N = 4#number of simulations per-day
            # modeldata=modeldata.groupby(modeldata.index // N).sum()
            
                       
            modeldata=modeldata['total_new_infections']
            N = 4#number of simulations per-day
            # modeldata=modeldata.groupby(modeldata.index // N).sum()
            
            modeldata=modeldata.iloc[0::N]
            
            modeldata=modeldata.to_list()
            
            modeldata=np.array(modeldata)
            modeldata=modeldata[:lendata]
            allmodels[str(i)]=modeldata
            simdata=np.add(modeldata,simdata)
        
    mean=simdata/len(posterior_index)
    stdev=np.std(allmodels,axis=1)
    print(len(stdev),len(mean),len(allmodels))
    CI95=pd.DataFrame({"Mean":mean,"LL":mean-1.96*stdev/np.sqrt(len(mean)),"UL":mean+1.96*stdev/np.sqrt(len(mean))})
    return mean,stdev,allmodels,CI95


