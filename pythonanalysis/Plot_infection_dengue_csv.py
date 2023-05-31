#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 15:12:00 2023

@author: shakir
"""
import os
import numpy as np
import pandas as pd
import time
import datetime as dt
import matplotlib.dates as mdates

import matplotlib.pyplot as plt

import plotly.graph_objects as go

from plotly.subplots import make_subplots


output_directory_base0 =  "../outputdir/"#"unshifted_revisedvaccine/"

cols1=["Symptomatic"]

NetworkTypes=["SmallWorld"]


sets=['1']#,'1024']

AllLambda1={}
AllLambda2={}

for fn in sets:
    AllLambda1[fn]=0
    AllLambda2[fn]=0
    
startdate1=dt.date(2020,3,1)
output_directory=output_directory_base0+str(fn)+"/"

modeldata=pd.read_csv(os.path.join(output_directory,"csvContent"+NetworkTypes[0]+".csv"),index_col=False)

Nodes=list(modeldata.Nodes.unique())

Allnodes={}
for nd in Nodes:
    Allnodes[nd]=modeldata.loc[modeldata.Nodes.isin([nd])].reset_index().drop(['index'],axis=1)['Symptomatic']
AllnodeDF=pd.DataFrame(Allnodes)




DataDates1=[startdate1 + dt.timedelta(days=int(x)) for x in range(1,len(modeldata.loc[modeldata.Nodes.isin([1])])+1)]

#----Matplotlib plotting--//

# plt.figure(figsize=(10,6))
# for cl in sets:
#     plt.plot(DataDates1,Alldata1[cl])

# plt.title("Infected")
# ax=plt.gca()
# ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
# plt.gcf().autofmt_xdate()
# plt.show()


#----Plotly for ploting----

colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink','grey','magenta','orchid','darkgreen']
colors1=['red','blue','green']
fig = make_subplots(rows=1, cols=1, shared_xaxes=True, vertical_spacing=0.1)

# line=dict(color='black')
i=1
x1=0.5
for cl in Nodes:

    fig.add_trace(
        go.Scatter(x=DataDates1, y=AllnodeDF[cl],name=str(cl),line=dict(color=colors[i-1]),legendgroup=str(i)),
        row=1, col=1)

    i+=1
# Set y-axes titles
fig.update_yaxes(title_text="Cases by Nodes",title_font=dict(size=20), row=1, col=1,tickfont = dict(size=20))
fig.update_xaxes(visible=True, row=1, col=1)

# Set x-axis title for the third row

fig.update_xaxes(title_text="Date",title_font=dict(size=20), row=1, col=1,tickfont = dict(size=20))
fig.update_traces(showlegend=True)
fig.update_layout(
    legend=dict(
        orientation="v",
        yanchor="top",
        y=1,
        xanchor="right",
        x=1.1
    )
)

file_path = os.getcwd()
file_name = 'figureplotly.png'

fig.update_layout(height=700, width=1000,legend_tracegroupgap = 10)
fig.update_layout(xaxis=dict({'range': [dt.date(2020,3,1), dt.date(2020,7,1)]},tickmode='array',dtick='M4', tickformat='%b %Y'))


import plotly.io as pio

# Create a sample plotly figure

# Define the file path and file name
file_path = os.getcwd()
file_name = 'figure.png'

# Set the output format to png
pio.kaleido.scope.default_format = 'png'

# Write the figure to a file
pio.write_image(fig, file_path+'/'+file_name)
fig.show()
