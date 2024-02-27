#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 16:12:23 2022

@author: shakir
"""

def getcommand(params):
    comms=[k for k in params]
    
    comms.pop(0)
    # comms.pop(0)
    # comms.pop(0)
    
    command = " "
    command += params["execDir"] + "drive_simulator" + " "
    # command += params["SEED_HD_AREA_POPULATION"] + " "
    # command += params["SEED_ONLY_NON_COMMUTER"] + " "
    
    for cm in comms:
        command+=" "+" --" + cm +" " + str(params[cm])
    
    return command

