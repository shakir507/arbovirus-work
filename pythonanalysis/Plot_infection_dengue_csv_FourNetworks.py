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

networktypes=["SmallWorld","Random","ScaleFree"]
Node_to_city={1:"Ah",2:"Malau",3:"Limbong",4:"Kuala Kedah",5:"Padang Kerbau",6:"Sik",7:"Semeling",8:"Kota",9:"Pinang Tunggal",10:"Lunas",11:"Mahang"}

# 1 		Ah              4243                 3
# 2 		Malau           3209                 4
# 3 		Limbong 1       620                  4
# 4		    Kuala Kedah     20924                3

# 5		    Padang Kerbau   12147                3
# 6 		Sik             41394                2

# 7 		Semeling        22255                4
# 8 		Kota            2960                 3
# 9 		Pinang Tunggal  16243                3

# 10 		Lunas           26681                4
# 11 		Mahang          2835                 1

sets=['1']#,'1024']

startdate1=dt.date(2020,3,1)



AllnodeDF={}
for nt in networktypes:
    AllnodeDF[nt]=0
for nt in networktypes:
    output_directory=output_directory_base0+"1"+"/"
    modeldata=pd.read_csv(os.path.join(output_directory,"csvContent"+nt+".csv"))
    Nodes=list(modeldata.Nodes.unique())
    Allnodes={}
    for nd in Nodes:
        Allnodes[nd]=modeldata.loc[modeldata.Nodes.isin([nd])].reset_index().drop(['index'],axis=1)['Symptomatic']
    AllnodeDF[nt]=pd.DataFrame(Allnodes)    




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

# colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink','grey','magenta','orchid','darkgreen']
# colors1=['red','blue','green']
# fig = make_subplots(rows=1, cols=1, shared_xaxes=True, vertical_spacing=0.1)

# # line=dict(color='black')
# i=1
# x1=0.5
# for cl in Nodes:

#     fig.add_trace(
#         go.Scatter(x=DataDates1, y=AllnodeDF[cl],name=str(cl),line=dict(color=colors[i-1]),legendgroup=str(i)),
#         row=1, col=1)

#     i+=1
# # Set y-axes titles
# fig.update_yaxes(title_text="Cases by Nodes",title_font=dict(size=20), row=1, col=1,tickfont = dict(size=20))
# fig.update_xaxes(visible=True, row=1, col=1)

# # Set x-axis title for the third row

# fig.update_xaxes(title_text="Date",title_font=dict(size=20), row=1, col=1,tickfont = dict(size=20))
# fig.update_traces(showlegend=True)
# fig.update_layout(
#     legend=dict(
#         orientation="v",
#         yanchor="top",
#         y=1,
#         xanchor="right",
#         x=1.1
#     )
# )

# file_path = os.getcwd()
# file_name = 'figureplotly.png'

# fig.update_layout(height=700, width=1000,legend_tracegroupgap = 10)
# fig.update_layout(xaxis=dict({'range': [dt.date(2020,3,1), dt.date(2020,7,1)]},tickmode='array',dtick='M4', tickformat='%b %Y'))


# import plotly.io as pio

# # Create a sample plotly figure

# # Define the file path and file name
# file_path = os.getcwd()
# file_name = 'figure.png'

# # Set the output format to png
# pio.kaleido.scope.default_format = 'png'

# # Write the figure to a file
# pio.write_image(fig, file_path+'/'+file_name)
# fig.show()


colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink','grey','magenta','orchid','darkgreen']
colors1=['red','blue','green']
fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.05)

# line=dict(color='black')
i=1
x1=0.5
for dv in networktypes:
    kl=0
    for cl in Nodes:
        
        fig.add_trace(
            go.Scatter(x=DataDates1, y=AllnodeDF[dv][cl],name=Node_to_city[cl],line=dict(color=colors[kl]),legendgroup=str(i)),
            row=i, col=1)
        kl+=1
    x1=x1+0.6*(i-1)    
#     fig.update_layout(
#     legend=dict(x=x1, y=-0.2, orientation='h'),
#     legend_tracegroupgap=50,
#     legend_title_text='Subplot'+str(i-1),
#     legend_title_font_size=16,
#     legend_title_font_color=colors1[i-1],
#     legend_title_side='top',
#     legend_bgcolor='rgba(255, 255, 255, 0.5)',
#     legend_bordercolor='black',
#     legend_borderwidth=2,
#     legend_itemsizing='constant')
        #ax[i].legend(diversity[dv][str(kl)],loc='upper right')

    i+=1
# Set y-axes titles
fig.update_yaxes(title_text="Cases Small World",title_font=dict(size=20), row=1, col=1,tickfont = dict(size=18))
fig.update_yaxes(title_text="Cases Random Network",title_font=dict(size=20), row=2, col=1,tickfont = dict(size=18))
fig.update_yaxes(title_text="Cases Scale Free",title_font=dict(size=20), row=3, col=1,tickfont = dict(size=18))
# fig.update_yaxes(title_text="Cases Kedah",title_font=dict(size=20), row=4, col=1,tickfont = dict(size=18))

fig.update_xaxes(visible=True, row=1, col=1)

fig.update_xaxes(visible=True, row=2, col=1)


# Set x-axis title for the third row


fig.update_xaxes({'range': [dt.date(2020,3,1), dt.date(2020,7,1)],
                      'tickmode': 'array',
                      'dtick': 'M4',
                      'tickformat': '%b %Y'},
                      row=3, col=1)
fig.update_xaxes(title_text="Date",title_font=dict(size=20),tickfont = dict(size=18), row=4, col=1,tickangle= -45)

fig.update_layout(height=1200, width=800,legend_tracegroupgap = 50)
fig.update_layout(xaxis=dict({'range': [dt.date(2020,3,1), dt.date(2020,7,1)]},tickmode='array',dtick='M4', tickformat='%b %Y',tickangle= -45))

output_file = os.path.join(os.getcwd(), "NetworkPlots.png")

# write the plot to the output file
fig.write_image(output_file)
#fig.show()



        