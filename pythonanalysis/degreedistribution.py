import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import plotly.graph_objects as go

from plotly.subplots import make_subplots


output_directory_base0 =  "../../outputdir/"#"unshifted_revisedvaccine/"

cols1=["Symptomatic"]

networktypes=["kedah","random","scalefree","smallWorld"]

sets=['1']#,'1024']

AllLambda1={}
AllLambda2={}

for fn in networktypes:
    AllLambda1[fn]=0
    AllLambda2[fn]=0
for fn in networktypes:
    output_directory=output_directory_base0+str(fn)+"/"+"1"+"/"
    print(output_directory)
    modeldata=pd.read_csv(os.path.join(output_directory,"matrix.csv"))
    AllLambda1[fn]=modeldata
    AllLambda2[fn]= AllLambda1[fn].sum(axis=1)

    print(np.mean(AllLambda2[fn]))
    plt.plot(AllLambda2[fn])
    plt.legend(networktypes)
plt.show()