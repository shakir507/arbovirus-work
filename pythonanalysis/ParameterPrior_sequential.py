import pandas as pd
import numpy as np
import datetime as dt
import random
import matplotlib.pyplot as plt
import scipy.sparse as sparse
import scipy.sparse.linalg as linalg
import scipy.integrate as integrate
import math
from scipy.stats.distributions import norm
from scipy.stats import gamma
from RMSE_Sequential_PostProcessing_posterior import rmse_save_posterior
from scipy import stats
from pyDOE import *

import os

def Priors_history(nParams,nsd,output_directory_base0,ChiCrit):
    
    #Rmse-criterion
    
    output_directory_base =  output_directory_base0 +"piece_"+str(nsd-1)+"/"

    data=pd.read_csv(os.path.join(output_directory_base,"casesfile_"+str(nsd-1)+".csv"),parse_dates=['date'])

    prior=pd.read_csv(os.path.join(output_directory_base,"prior_parameters_sequential_"+str(nsd-1)+".csv"))

    parameters_ran=[0]*nParams*2#parameters.head(6853)

    rmse_save_posterior(parameters_ran,output_directory_base,nsd-1)
    
    rmse_table=pd.read_csv(os.path.join(output_directory_base,"rmse_priors_"+str(nsd-1)+".csv"))

    posterior_index=[]
    # while(len(list(set(posterior_index)))<20 and r_th<20):
    #     for i in rmse_table['index']:
    #         if rmse_table['RMSE'][i]<r_th and rmse_table['RMSE'][i]>0:
    #             posterior_index.append(i)
    #     r_th+=1
    #while(len(list(set(posterior_index)))<20):
    for i in rmse_table['index']:
        if rmse_table['RMSE'][i]<100*ChiCrit and rmse_table['RMSE'][i]>0:
            posterior_index.append(i)
    posterior_index=list(set(posterior_index))
    print(posterior_index)
    posterior0=prior.iloc[posterior_index]
    infectedcases=[]
    exposed=[]
    recovered=[]
    for jk in posterior_index:
        output_directory =  output_directory_base +str(int(jk))+"/"
        if(os.path.exists(os.path.join(output_directory,"new_infections.csv"))):
            inf=pd.read_csv(os.path.join(output_directory,""))
            infectedcases.append(inf["Infected"][len(inf)-1])
            exposed.appendappend(inf["Exposed"][len(inf)-1])
            recovered.append(inf["Recovered"][len(inf)-1])
    #return posterior0,posterior_index,prior
#     #get-max-and-min
#-----------------------------------------------------------------------------#

    minValues={}
    maxValues={}
    minValues['bet1']=min(posterior0['bet1']);
    maxValues['bet1']=max(posterior0['bet1']);
    
    minValues['bet2']=min(posterior0['bet2']);
    maxValues['bet2']=max(posterior0['bet2']);
    

    minValues['muV']=min(posterior0["muV"])
    maxValues['muV']=max(posterior0["muV"])#9

    minValues["Exposed"]=min(exposed+[1])
    maxValues["Exposed"]=max(exposed+[1])

    minValues["InitialInfections"]=min(infectedcases+[1])
    maxValues["InitialInfections"]=max(infectedcases+[1])

    minValues["Recovered"]=min(recovered+[1])
    maxValues["Recovered"]=max(recovered+[1])

#-----------------------------------------------------------------------------#
    #priors(nParams)
    rangeParam={}
    for ld in minValues:
        rangeParam[ld]=maxValues[ld]-minValues[ld]
#-----------------------------------------------------------------------------#

    paraLHS=lhs(len(minValues), samples=nParams, criterion='corr');#to use the correlation feature, the dimension of the matrix should be more than 1.
    
#-----------------------------------------------------------------------------#
    i=0
    VarParamsLHS=pd.DataFrame()
    for ld in minValues:
        VarParamsLHS[ld]=minValues[ld]+rangeParam[ld]*paraLHS[:,i]
        i=i+1


    return VarParamsLHS