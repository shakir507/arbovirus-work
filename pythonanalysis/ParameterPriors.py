#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 10:21:04 2022

@author: shakir
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 15:26:02 2022

@author: shakir
"""

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

from scipy import stats
from pyDOE import *

import os

def Priors(nParams):
#-----------------------------------------------------------------------------#
    minValues={}
    maxValues={}

#------------------Beta: home, school, work, community------------------------#
    minValues['BETA_SCALE']=1;
    maxValues['BETA_SCALE']=9;
    
    minValues['BETA_H']=0.0001;
    maxValues['BETA_H']=1;#9
    
    minValues["BETA_RANDOM_COMMUNITY"]=0.0001;#BETA_NBR_CELLS
    maxValues["BETA_RANDOM_COMMUNITY"]=1;#BETA_NBR_CELLS
    
    minValues["BETA_W"]=0.0001
    maxValues["BETA_W"]=1
    
    minValues["BETA_S"]=0.001;
    maxValues["BETA_S"]=1.5
    
    minValues["BETA_C"]=0.001
    maxValues["BETA_C"]=1


#-----------------------------------------------------------------------------#
    rangeParam={};
    for ld in minValues:
        rangeParam[ld]=maxValues[ld]-minValues[ld]
    
    
    
#-----------------------------------------------------------------------------#
    np.random.seed(2)#fixing  
    

    paraLHS=lhs(len(minValues), samples=nParams, criterion='corr');#to use the correlation feature, the dimension of the matrix should be more than 1.
    
    print(len(minValues))
    
#-----------------------------------------------------------------------------#
    
    
    i=0;
    VarParamsLHS=pd.DataFrame()
    for ld in minValues:
        VarParamsLHS[ld]=minValues[ld]+rangeParam[ld]*paraLHS[:,i]
        i=i+1
    VarParamsLHS['PROVIDE_INITIAL_SEED_GRAPH']=random.sample(range(1, nParams+1), nParams)
    VarParamsLHS['PROVIDE_INITIAL_SEED']=random.sample(range(1, nParams+1), nParams)

    return VarParamsLHS
#-----------------------------------------------------------------------------#