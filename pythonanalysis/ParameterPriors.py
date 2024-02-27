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
    minValues['bet1']=0.
    maxValues['bet1']=0.01
    
    minValues['bet2']=0.
    maxValues['bet2']=0.02#9


    minValues['muV']=0.06
    maxValues['muV']=0.07#9

    minValues["Exposed"]=50
    maxValues["Exposed"]=100

    minValues["InitialInfections"]=50
    maxValues["InitialInfections"]=100

    minValues["Recovered"]=50
    maxValues["Recovered"]=100
    print(minValues)
#-----------------------------------------------------------------------------#
    rangeParam={}
    for ld in minValues:
        rangeParam[ld]=maxValues[ld]-minValues[ld]
    
    
    
#-----------------------------------------------------------------------------#
    np.random.seed(2)#fixing  
    
    paraLHS=lhs(len(minValues), samples=nParams, criterion='corr');#to use the correlation feature, the dimension of the matrix should be more than 1.
    # paraLHS=lhs(2, samples=2, criterion='corr');#to use the correlation feature, the dimension of the matrix should be more than 1.
    
#-----------------------------------------------------------------------------#
    
    
    i=0
    VarParamsLHS=pd.DataFrame()
    for ld in minValues:
        VarParamsLHS[ld]=minValues[ld]+rangeParam[ld]*paraLHS[:,i]
        i=i+1

    return VarParamsLHS
#-----------------------------------------------------------------------------#