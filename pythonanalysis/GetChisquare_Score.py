#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 19:28:36 2022

@author: shakir
"""

import numpy as np

def chisquare(data,modeldata):
        chi_square_test_statistic1 = 0
        for i in range(len(data)):
            print(len(modeldata))
            chi_square_test_statistic1 = chi_square_test_statistic1 + (np.square(data[i]-modeldata[i]-0.1))/(modeldata[i]+0.1)
        return chi_square_test_statistic1