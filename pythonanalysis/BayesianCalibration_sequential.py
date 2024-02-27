#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 01:19:15 2022

@author: shakir
"""

# This code is used to tune the parameters of the simulator sequentially so as to match the probability of getting an infection (i.e. lambda_home,
# lambda_workplace and lambda_community) to certain target value (default target value is 1/3 each) as well as to match the number
# of fatalities curve to actual data.



import os
import numpy as np
import pandas as pd
import time


from ParameterPriors import Priors
from ParameterPrior_sequential import Priors_history
from run_parallel_simulations import run_parallel_sim
import scipy.stats as stats
# from calculate_DataModel_rmse import datamodel_Gap


output_directory_base0 =  "../outputdir/SequentialFitting/"#"unshifted_revisedvaccine/"

os.system('mkdir -p ' + output_directory_base0)

input_directory = "../../InputFiles/Senegal/"#be sure to block this line for full population test

    
ChiCrit=50
for nsd in range(1,41):
    output_directory_base =  output_directory_base0 +"piece_"+str(nsd)+"/"
    
#---------Selecting priors sequentially-------------------------
#--------In the first piece of the simulation, the priors are selected from a fixed range as determined from literature/guess work.
#------- While the subsequent pieces the priors are informed from the best fitting parameters obtained in the previous step.
    n_Params = 10
    # if nsd>1:
    #     posterior0,posterior_index,prior=Priors_history(n_Params,nsd,output_directory_base0)
    if nsd==1:
        parameters = Priors(n_Params)
    else:
        par1=Priors(int(n_Params/2))
        par2=Priors_history(int(n_Params/2), nsd, output_directory_base0,ChiCrit)
        parameters = pd.concat([par1,par2],ignore_index=True)#this function uses the information on current simulation piece, 
        #and based on that it digs up the previous simulation results, calcuated best fitting parameters, 
        #checks their range and then generates a new prior based on this new range.
        
 
    parameters["START_DAY"]=nsd-1+(nsd-1)*30

    parameters["output_directory_base"]=output_directory_base
    parameters["input_directory"]=input_directory
    #Location profile includs number of cities, network formed between cities and the filename that store the adjacency matrix
    parameters["Nodes"]=47#there are 47 cities in Senegal
    parameters["NetworkName"]="Random"#"Scalefree","Random","SmallWorld"
    parameters["NetworkFileHuman"]="NetworkFileHumanRandom.json"#"NetworkFileHumanScaleFree.json","NetworkFileHumanRandom.json","NetworkFileHumanSmallWorld.json"
    #parameters.to_csv(os.path.join(output_directory_base,"prior_parameters_sequential_"+str(nsd)+".csv"))

    parameters.to_csv(os.path.join(output_directory_base,"prior_parameters_sequential_"+str(nsd)+".csv"))

    run_parallel_sim(parameters)
    

