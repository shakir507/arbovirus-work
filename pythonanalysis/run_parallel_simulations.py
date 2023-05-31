#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 13:09:46 2022

@author: shakir
"""
import pandas as pd
from multiprocessing import Process, Queue, Manager
import multiprocessing as mp
from run_simulator import run_parameter_simulator


def run_parallel_sim(parameters):
    index=[x for x in range(len(parameters))]

    pool = mp.Pool(4)#processes=min((os.cpu_count() - 1), PROC_TO_RUN))

    for i in range(len(parameters)):
        pool.apply_async(run_parameter_simulator, (parameters,i))
    pool.close()
    pool.join()