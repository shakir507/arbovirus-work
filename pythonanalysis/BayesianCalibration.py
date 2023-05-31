#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 01:19:15 2022

@author: shakir
"""

# This code is used to tune the parameters of the simulator so as to match the probability of getting an infection (i.e. lambda_home,
# lambda_workplace and lambda_community) to certain target value (default target value is 1/3 each) as well as to match the number
# of fatalities curve to actual data.



import os
import numpy as np
import pandas as pd
import time


from ParameterPriors import Priors
#from ParameterPrior_betas_Sequential_test import Priors_history
from run_parallel_simulations import run_parallel_sim
import scipy.stats as stats
# from calculate_DataModel_rmse import datamodel_Gap


output_directory_base0 =  "../outputdir/"#"unshifted_revisedvaccine/"

os.system('mkdir -p ' + output_directory_base0)

input_directory = "../InputFiles/Kedah/"#be sure to block this line for full population test


ChiCrit=stats.chi2.ppf(1-0.05, df=NUM_DAYS)

    
#---------Selecting priors sequentially-------------------------
#--------In the first piece of the simulation, the priors are selected from a fixed range as determined from literature/guess work.
#------- While the subsequent pieces the priors are informed from the best fitting parameters obtained in the previous step.
n_Params = 2
# if nsd>1:
#     posterior0,posterior_index,prior=Priors_history(n_Params,nsd,output_directory_base0)
parameters = Priors(n_Params)

    
 
parameters["START_DAY"]=0#nsd+(nsd-1)*NUM_DAYS
parameters["output_directory_base"]=output_directory_base
parameters["input_directory"]=input_directory

#parameters.to_csv(os.path.join(output_directory_base,"prior_parameters_sequential_"+str(nsd)+".csv"))

parameters.to_csv(os.path.join(output_directory_base,"prior_parameters_sequential_"+".csv"))

run_parallel_sim(parameters)
    

