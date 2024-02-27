import numpy as np
import pandas as pd
import os
import networkx as nx
import json
import matplotlib.pyplot as plt

def SetinitialConditions(nt,centrality,degree,node_names,Nodes):
    I=[0]*Nodes
    np.random.seed(2)
    Ir=list(np.random.randint(1,100,Nodes))
    Ir=sorted(Ir)
    nodecentrality={}
    nodedegree={}
    for nd in node_names:
        nodecentrality[nd]=centrality[nt][nd]
        nodedegree[nd]=degree[nt][nd]
    sorted_node_by_degree=(sorted(nodedegree.items(), key=lambda x:x[1]))
    for i in range(Nodes):
        I[sorted_node_by_degree[i][0]]=Ir[i]
    return I

input_path="../InputFiles/Senegal/"
output_path="../OutputFiles/Senegal/"

os.system('mkdir -p ' + input_path)
os.system('mkdir -p ' + output_path)

NetworkTypes=["SmallWorld","Random","ScaleFree","ScaleFreeConfigurationModel"]

#-----Network generator------//
Nodes=47
k=4# average degree
psm=0.1
prn=0.3
m = 2
seed=2
degree={}
centrality={}
np.random.seed(seed)#fixing  seed
for nt in NetworkTypes:
    if nt==NetworkTypes[0]:

        G=nx.watts_strogatz_graph(Nodes, k, psm,seed)
        degree[nt]=G.degree()
        centrality[nt]=nx.betweenness_centrality(G)
    if nt==NetworkTypes[1]:

        G = nx.erdos_renyi_graph(Nodes, prn,seed)
        degree[nt]=G.degree()
        centrality[nt]=nx.betweenness_centrality(G)

    if nt==NetworkTypes[2]:

        G = nx.barabasi_albert_graph(Nodes, m,seed=seed)
        degree[nt]=G.degree()
        centrality[nt]=nx.betweenness_centrality(G)

    if nt==NetworkTypes[3]:
        degree_sequence = [k] * Nodes
        G = nx.configuration_model(degree_sequence,seed=seed)
        G = nx.Graph(G)
        degree[nt]=G.degree()
        centrality[nt]=nx.betweenness_centrality(G)

    
    # Convert the graph to an adjacency matrix
    adj_matrix = nx.to_numpy_array(G, dtype=int)

    # Convert int64 elements to regular Python integers
    adj_matrix = adj_matrix.astype(int)

    # Retrieve the list of node names
    node_names = list(G.nodes())

    # Create a list of dictionaries with keys as node names
    adj_list_dict = []
    for i in range(len(adj_matrix)):
        dict1 = {}
        dict1["node"] = node_names[i]
        for j in range(len(adj_matrix)):
            dict1[str(j)] = int(adj_matrix[i][j])
        adj_list_dict.append(dict1)

    # Write the adjacency list dictionary to a JSON file
    with open(os.path.join(input_path, "NetworkFileHuman"+nt+".json"), "w") as file:
        json.dump(adj_list_dict, file)
    # print(adj_list_dict)

I=SetinitialConditions(nt,centrality,degree,node_names,Nodes)

print(I)


#Seeding infection on nodes
# I=[0]*Nodes
# I[0]=15;
# I[1]=16;
# I[2]=18;
# I[3]=28;
# I[4]=10;
# I[5]=34;
# I[6]=31;
# I[7]=25;
# I[8]=30;
# I[9]=57;
# I[10]=14;


PIH=[0]*Nodes
# PIH[0]=0.157089967;
# PIH[1]=0.118807849;
# PIH[2]=0.059977786;
# PIH[3]=0.774676046;
# PIH[4]=0.449722325;
# PIH[5]=1.532543502;
# PIH[6]=0.823954091;
# PIH[7]=0.109589041;
# PIH[8]=0.601369863;
# PIH[9]=0.987819326;
# PIH[10]=0.104961126;

muM=[0]*Nodes
R0=[0]*Nodes
np.random.seed(seed)
R0=[4+np.random.random() for i in range(Nodes)]#Reproduction number to reverse engineer mosquito birth rate and hence population
muM=[1/16.0 for i in range(Nodes)]#---------vector death rate
np.random.seed(seed)
PIH=[2*np.random.random() for i in range(Nodes)]        
infec=pd.DataFrame({"Infected":I,"birthrate":PIH,"MosquitoDeathRate":muM,"R0":R0})

infec.to_json(os.path.join(input_path,"NetworkSeeding.json"),orient='records')
# print(nt,degree[nt],Nodes)
# for nd in node_names:
#     print(nd,degree[nt][nd])
# nt=NetworkTypes[0]
# print(centrality[nt])

# for nd in node_names:
#     plt.plot(degree[nt][nd],I[nd],"-*")
# plt.show()