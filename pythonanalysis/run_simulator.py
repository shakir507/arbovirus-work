#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 17:05:15 2022

@author: shakir
"""
import os
import numpy as np
import pandas as pd

from get_command import getcommand


def run_parameter_simulator(parameters,i):
    input_directory = parameters["input_directory"][i]
    #"../../staticInst/data/synthpops/hills-1p45M/"
    output_directory_base =  parameters["output_directory_base"][i]

    DAY_TILL_SIMUL=30
    START_DAY=parameters["START_DAY"][i]
    NUM_DAYS = DAY_TILL_SIMUL-START_DAY


    EXEC_DIR = "../cpp-ArboSim/"

    START_DAY=parameters["START_DAY"][i]
    print(parameters)

    bet1 = parameters["bet1"][i]#BETA_PROJECT / BETA_SCALE
    bet2 = parameters["bet2"][i]#BETA_CLASS / BETA_SCALE
    muV  = parameters["muV"][i]
    nodes= parameters["Nodes"][i]
    Networktype=parameters["NetworkName"][i]
    NetworkFile=parameters["NetworkFileHuman"][i]
    exposed=parameters["Exposed"][i]
    InitialInfections=parameters["InitialInfections"][i]
    recovered=parameters["Recovered"][i]
    params = {
        "execDir": EXEC_DIR,
        "NUM_DAYS": NUM_DAYS,        
        "input_directory": input_directory,
        "Exposed": exposed,
        "InitialInfections": InitialInfections,
        "Recovered": recovered,
        "bet1":bet1,
        "bet2":bet2,
        "muV":muV,
        "NetworkName":Networktype,#"Scalefree","Random","SmallWorld"
        "NetworkFileHuman":NetworkFile,#"NetworkFileHumanRandom.json","NetworkFileHumanSmallWorld.json"
        "Nodes":nodes
    }
    print(params)

    command=getcommand(params)
    print("waiting for command",command)

    params['output_directory']=output_directory_base

    output_directory =  output_directory_base +str(i)+"/"
    os.system("mkdir -p " + output_directory)
    
    #command += params["SEED_FIXED_NUMBER"]
    command+= " --output_directory " + str(output_directory)

    print(command)
    os.system(command)
