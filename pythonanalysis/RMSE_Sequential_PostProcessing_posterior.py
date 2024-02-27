#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 00:35:31 2022

@author: shakir
"""

import os
import numpy as np
import pandas as pd
import time
#from calculate_DataModel_rmse import datamodel_Gap
import scipy.stats as stats

from GetChisquare_Score import chisquare
def rmse_save_posterior(parameters,output_directory_base,nsd):

    #parameters=pd.read_csv(os.path.join(output_directory_base,'prior_parameters.csv'))
    n_params=len(parameters)
    RMSE_df=pd.DataFrame({"index":[0.0]*n_params,"RMSE":[0.0]*n_params,"p_value":[0.0]*n_params})
    RMSE_df=RMSE_df[:]*0.0
    
    data=pd.read_csv(os.path.join(output_directory_base,"casesfile_"+str(nsd)+".csv"),parse_dates=['date'])
    cols=['total cases']#'time_step',
    data=data[cols]
    data=data['total cases'].to_list()
    i1=0
    print("i am in rmse\n")
    for i in range(len(parameters)):
        output_directory =  output_directory_base +str(int(i))+"/"
        if(os.path.exists(os.path.join(output_directory,"new_infections.csv"))):
            modeldata=pd.read_csv(os.path.join(output_directory,"new_infections.csv"))
           
            modeldata=modeldata['total_new_infections']
            N = 4#number of simulations per-day
            # modeldata=modeldata.groupby(modeldata.index // N).sum()
            
            modeldata=modeldata
            modeldata=modeldata.to_list()
            
            #print(i,len(data),len(modeldata))
            #chi_square_test_statistic, p_value = stats.chisquare(data, modeldata)
            chi_square_test_statistic=chisquare(data,modeldata)
            RMSE_df['RMSE'][i]= chi_square_test_statistic
            RMSE_df['p_value'][i]=500000
            #print(i,len(data),len(modeldata),chi_square_test_statistic)

            #RMSE_df['RMSE'][i], RMSE_df['Correlation'][i]=datamodel_Gap(modeldata,data)
        #print(rmse_df,corr)
        #    if rmse_df <100:
            RMSE_df['index'][i]=i
            i1+=1
        # RMSE_df['RMSE'][i]=rmse_df
        # RMSE_df['Correlation'][i]=corr
    #print(result)
    
    RMSE_df.to_csv(os.path.join(output_directory_base, "rmse_priors_"+str(nsd)+".csv"),index=False)
    print("i am done with rmse\n")

    