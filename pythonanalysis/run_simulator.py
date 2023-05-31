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



    #[a, b] = [45.68826233  1.98380143].
    city = "hillsborough"
    
    F_KERNEL_A = 10.751
    F_KERNEL_B = 5.384
    
    # F_KERNEL_A = 45.68826233#10.751
    # F_KERNEL_B = 1.98380143#5.384
    
    # F_KERNEL_A = 10.751
    # F_KERNEL_B = 5.384
    INTERVENTION = 18 #----Intervention 18 inlcudes hillsborough specific interventions

    DAY_TILL_SIMUL=1400
    START_DAY=parameters["START_DAY"][i]
    NUM_DAYS = DAY_TILL_SIMUL-START_DAY

    # if(START_DAY>126):
    #     INTERVENTION=18
    MEAN_INCUBATION_PERIOD = 4.6
    MEAN_ASYMPTOMATIC_PERIOD = 0.5
    MEAN_SYMPTOMATIC_PERIOD = 5
    SYMPTOMATIC_FRACTION = 0.66
    MEAN_HOSPITAL_REGULAR_PERIOD = 8
    MEAN_HOSPITAL_CRITICAL_PERIOD = 8
    COMPLIANCE_PROBABILITY = 0.9


    HD_AREA_FACTOR = 2.0
    HD_AREA_EXPONENT = 0


    LAT_S = 27.646424685156582
    LAT_N = 28.173707571989837
    LON_E = -82.05401843866441
    LON_W = -82.65120691246932
    INIT_FIXED_NUMBER_INFECTED = parameters["INIT_FIXED_NUMBER_INFECTED"][i]
#    EXEC_DIR = "../calibration-mpi-protobuf/cpp-simulator/"
#    EXEC_DIR = "../calibration-mpi-protobuf_agetransfactor/cpp-simulator/"
#    EXEC_DIR = "../calibration-mpi-protobuf_new_individualfile/cpp-simulator/"
#    EXEC_DIR = "../calibration-mpi-protobuf_age_race_factor_hosp_death/cpp-simulator/"
#    EXEC_DIR = "../calibration-mpi-protobuf_age_race_factor_hosp_death_travelasymettry/cpp-simulator/"
#    EXEC_DIR = "../calibration-mpi-protobuf_age_race_factor_hosp_death_travelasymettry_writehistory/cpp-simulator/"
    EXEC_DIR = "../calibration-mpi-protobuf_age_race_factor_hosp_death_travelasymettry_writehistory_TestImmune/cpp-simulator/"

#    EXEC_DIR = "../calibration-mpi-protobuf_TravelTesting/cpp-simulator/"
#    EXEC_DIR = "../calibration-mpi-protobuf_MoreVariants/cpp-simulator/"
#    EXEC_DIR ="../calibration-mpi-protobuf_VoidGTrendsinBeta/cpp-simulator/"
#    EXEC_DIR = "../calibration-mpi-protobuf_deltaStrongBehaviour/cpp-simulator/"
#    EXEC_DIR = "../calibration-mpi-protobuf_delta_omicron_asymmetry/cpp-simulator/"

    # Set this to "--SEED_HD_AREA_POPULATION" to seed hd area population
    # as well.
    # SEED_HD_AREA_POPULATION="--SEED_HD_AREA_POPULATION"
    SEED_HD_AREA_POPULATION = " "
    # Set this to "--SEED_ONLY_NON_COMMUTER" to seed only those who do not
    # take public transit
    # SEED_ONLY_NON_COMMUTER="--SEED_ONLY_NON_COMMUTER"
    SEED_ONLY_NON_COMMUTER = " "
    # Set this to "--SEED_FIXED_NUMBER" to seed only a fixed number of
    # people. In this case, the value of INIT_FRAC_INFECTED will be
    # ignored in favour of the value of INIT_FIXED_NUMBER_INFECTED
    SEED_FIXED_NUMBER = "--SEED_FIXED_NUMBER"
    # SEED_FIXED_NUMBER=" "
    USE_AGE_DEPENDENT_MIXING = "false"
    IGNORE_ATTENDANCE_FILE = "true"

    # MEAN_INCUBATION_PERIOD=4.6
    # MEAN_ASYMPTOMATIC_PERIOD=0.5
    # MEAN_SYMPTOMATIC_PERIOD=5
    # SYMPTOMATIC_FRACTION=0.66
    # MEAN_HOSPITAL_REGULAR_PERIOD=8
    # MEAN_HOSPITAL_CRITICAL_PERIOD=8
    # COMPLIANCE_PROBABILITY=0.9    #---------------->These set of disease dynamics parameters can also be picked from a prior.
    
    INIT_FIXED_NUMBER_INFECTED = int(parameters['INIT_FIXED_NUMBER_INFECTED'][i])

    START_DAY=parameters["START_DAY"][i]
    TIME_ALPHA = int(parameters["TIME_ALPHA"][i])
    TIME_DELTA = int(parameters["TIME_DELTA"][i])
    TIME_OMICRON = int(parameters["TIME_OMICRON"][i])
    TIME_OMICRON_NEW = int(parameters["TIME_OMICRON_NEW"][i])

    INFECTIOUSNESS_ALPHA = parameters["INFECTIOUSNESS_ALPHA"][i]
    INFECTIOUSNESS_DELTA = parameters["INFECTIOUSNESS_DELTA"][i]
    INFECTIOUSNESS_OMICRON = parameters["INFECTIOUSNESS_OMICRON"][i]
    INFECTIOUSNESS_OMICRON_NEW = parameters["INFECTIOUSNESS_OMICRON_NEW"][i]

    VIRULENT_NEW_ALPHA = parameters["VIRULENT_NEW_ALPHA"][i]
    VIRULENT_NEW_DELTA = parameters["VIRULENT_NEW_DELTA"][i]
    VIRULENT_NEW_OMICRON = parameters["VIRULENT_NEW_OMICRON"][i]
    VIRULENT_NEW_OMICRON_NEW = parameters["VIRULENT_NEW_OMICRON_NEW"][i]

    REINFECTION_ALPHA = parameters["REINFECTION_ALPHA"][i]
    REINFECTION_DELTA = parameters["REINFECTION_DELTA"][i]
    REINFECTION_OMICRON = parameters["REINFECTION_OMICRON"][i]
    REINFECTION_OMICRON_NEW = parameters["REINFECTION_OMICRON_NEW"][i]

    FRACTION_NEW_ALPHA = parameters["FRACTION_NEW_ALPHA"][i]
    FRACTION_NEW_DELTA = parameters["FRACTION_NEW_DELTA"][i]
    FRACTION_NEW_OMICRON = parameters["FRACTION_NEW_OMICRON"][i]
    FRACTION_NEW_OMICRON_NEW = parameters["FRACTION_NEW_OMICRON_NEW"][i]

    FRACTION_SUSCEPTIBLE_ALPHA = parameters["FRACTION_SUSCEPTIBLE_ALPHA"][i]
    FRACTION_SUSCEPTIBLE_DELTA = parameters["FRACTION_SUSCEPTIBLE_DELTA"][i]
    FRACTION_SUSCEPTIBLE_OMICRON = parameters["FRACTION_SUSCEPTIBLE_OMICRON"][i]
    FRACTION_SUSCEPTIBLE_OMICRON_NEW = parameters["FRACTION_SUSCEPTIBLE_OMICRON_NEW"][i]

    BETA_SCALE = parameters["BETA_SCALE"][i]
    BETA_H = parameters["BETA_H"][i]
    BETA_PROJECT = parameters["BETA_PROJECT"][i]
    BETA_NBR_CELLS = parameters["BETA_NBR_CELLS"][i]
    BETA_CLASS = parameters["BETA_CLASS"][i]
    BETA_TRAVEL = parameters["BETA_TRAVEL"][i]

    CALIBRATION_DELAY = int(parameters['CALIBRATION_DELAY'][i])
    DAYS_BEFORE_LOCKDOWN = int(parameters['DAYS_BEFORE_LOCKDOWN'][i])
    
    VACCINATION_EFFECTIVENESS1=parameters['VACCINATION_EFFECTIVENESS1'][i]
    VACCINATION_EFFECTIVENESS2=parameters['VACCINATION_EFFECTIVENESS2'][i]
    VACCINATION_EFFECTIVENESS_WANING=parameters['VACCINATION_EFFECTIVENESS_WANING'][i]
    VACCINATION_EFFECTIVENESS_BOOSTED=parameters['VACCINATION_EFFECTIVENESS_BOOSTED'][i]
    

    BETA_RANDOM_COMMUNITY = parameters["BETA_RANDOM_COMMUNITY"][i]#BETA_NBR_CELLS
    BETA_W = parameters["BETA_W"][i]#BETA_PROJECT / BETA_SCALE
    BETA_S = parameters["BETA_S"][i]#BETA_CLASS / BETA_SCALE
    BETA_C = parameters["BETA_C"][i]#BETA_NBR_CELLS / BETA_SCALE
    
    PROVIDE_INITIAL_SEED=parameters["PROVIDE_INITIAL_SEED"][i]
    PROVIDE_INITIAL_SEED_GRAPH=parameters["PROVIDE_INITIAL_SEED_GRAPH"][i]
    MEAN_RECOVERED_TO_SUSCEPTIBLE_PERIOD=parameters['MEAN_RECOVERED_TO_SUSCEPTIBLE_PERIOD'][i]
    params = {
        "execDir": EXEC_DIR,
        # "SEED_HD_AREA_POPULATION": SEED_HD_AREA_POPULATION,
        # "SEED_ONLY_NON_COMMUTER": SEED_ONLY_NON_COMMUTER,
        "SEED_FIXED_NUMBER": SEED_FIXED_NUMBER,
        "NUM_DAYS": NUM_DAYS,
        "F_KERNEL_A": F_KERNEL_A,
        "F_KERNEL_B": F_KERNEL_B,

        # "HD_AREA_FACTOR": HD_AREA_FACTOR,
        # "HD_AREA_EXPONENT": HD_AREA_EXPONENT,
        
        "INTERVENTION": INTERVENTION,
        "input_directory": input_directory,
        
        #"INIT_FIXED_NUMBER_INFECTED": INIT_FIXED_NUMBER_INFECTED,

        # "TIME_ALPHA":TIME_ALPHA,
        # "TIME_DELTA":TIME_DELTA,
        # "TIME_OMICRON":TIME_OMICRON,
        # "TIME_OMICRON_NEW":TIME_OMICRON_NEW,
        
        # "INFECTIOUSNESS_ALPHA":INFECTIOUSNESS_ALPHA,
        # "INFECTIOUSNESS_DELTA":INFECTIOUSNESS_DELTA,
        # "INFECTIOUSNESS_OMICRON":INFECTIOUSNESS_OMICRON,
        # "INFECTIOUSNESS_OMICRON_NEW":INFECTIOUSNESS_OMICRON_NEW,
        
        # "VIRULENT_NEW_ALPHA":VIRULENT_NEW_ALPHA,
        # "VIRULENT_NEW_DELTA":VIRULENT_NEW_DELTA,
        # "VIRULENT_NEW_OMICRON":VIRULENT_NEW_OMICRON,
        # "VIRULENT_NEW_OMICRON_NEW":VIRULENT_NEW_OMICRON_NEW,
        
        # "REINFECTION_ALPHA":REINFECTION_ALPHA,
        # "REINFECTION_DELTA":REINFECTION_DELTA,
        # "REINFECTION_OMICRON":REINFECTION_OMICRON,
        # "REINFECTION_OMICRON_NEW":REINFECTION_OMICRON_NEW,
        
        # "FRACTION_NEW_ALPHA":FRACTION_NEW_ALPHA,
        # "FRACTION_NEW_DELTA":FRACTION_NEW_DELTA,
        # "FRACTION_NEW_OMICRON":FRACTION_NEW_OMICRON,
        # "FRACTION_NEW_OMICRON_NEW":FRACTION_NEW_OMICRON_NEW,
        
        # "FRACTION_SUSCEPTIBLE_ALPHA":FRACTION_SUSCEPTIBLE_ALPHA,
        # "FRACTION_SUSCEPTIBLE_DELTA":FRACTION_SUSCEPTIBLE_DELTA,
        # "FRACTION_SUSCEPTIBLE_OMICRON":FRACTION_SUSCEPTIBLE_OMICRON,
        # "FRACTION_SUSCEPTIBLE_OMICRON_NEW":FRACTION_SUSCEPTIBLE_OMICRON_NEW,
                
        # "BETA_H":BETA_H,
        # "BETA_PROJECT":BETA_PROJECT,
        # "BETA_NBR_CELLS":BETA_NBR_CELLS,
        # "BETA_CLASS":BETA_CLASS,
        #"BETA_TRAVEL":BETA_TRAVEL,
        
        # "BETA_RANDOM_COMMUNITY":BETA_RANDOM_COMMUNITY,
        # "BETA_W":BETA_W,
        # "BETA_S":BETA_S,
        # "BETA_C":BETA_C,
        
        # "VACCINATION_EFFECTIVENESS1":VACCINATION_EFFECTIVENESS1,
        # "VACCINATION_EFFECTIVENESS2":VACCINATION_EFFECTIVENESS2,
        # "VACCINATION_EFFECTIVENESS_WANING":VACCINATION_EFFECTIVENESS_WANING,
        # "VACCINATION_EFFECTIVENESS_BOOSTED":VACCINATION_EFFECTIVENESS_BOOSTED,
    
        "CALIBRATION_DELAY": CALIBRATION_DELAY,
        "DAYS_BEFORE_LOCKDOWN": DAYS_BEFORE_LOCKDOWN,
        "START_DAY": START_DAY
    }

    
    command=getcommand(params)
    print("waiting for command",command)

    params['output_directory']=output_directory_base

    output_directory =  output_directory_base +str(i)+"/"
    os.system("mkdir -p " + output_directory)
    
    #command += params["SEED_FIXED_NUMBER"]
    command+= " --output_directory " + str(output_directory)
    command+="  --PROVIDE_INITIAL_SEED " + " " + str(1)#str(int(PROVIDE_INITIAL_SEED))
    command+=" --PROVIDE_INITIAL_SEED_GRAPH " + " " + str(7)#str(int(PROVIDE_INITIAL_SEED_GRAPH))str(4123)
    #command+=" --ENABLE_NBR_CELLS " + " "
    #command+= " --mask_filename " + "maskwearing_November14_2022_plus4wgoogle_"+str(1)+".json"
    #command+= " --mask_folder " +"maskensembles_shifted"
    #command+=" --MEAN_RECOVERED_TO_SUSCEPTIBLE_PERIOD " + " " + str(int(MEAN_RECOVERED_TO_SUSCEPTIBLE_PERIOD))
    #command+=" --mask_filename " + " " + "maskwearing_Nov14_shifted_4weeks_"+str(22)+".json"
    #command+=" --MEASURES " + " " + str(4)#str(int(PROVIDE_INITIAL_SEED_GRAPH))str(4123)

    print(command)
    os.system(command)
