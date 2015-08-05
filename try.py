# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 23:09:36 2015

@author: chunyaoyang
"""

import pandas as pd
import matplotlib.pyplot as plt

filepath = "/Users/chunyaoyang/GitHub/py-gsboxplot/"
site = 'Trout'
year1 = '2001'
year2 = '2014'
output_eps = '%s.eps' % (site)
pc_csv1 = '%s_summary_%s.csv' % (site, year1)
pc_csv2 = '%s_summary_%s.csv' % (site, year2)

thalweg_csv = '%s_LP_Thalweg.csv' % (site)
thalweg_data = pd.read_csv(thalweg_csv)

csv_list = [pc_csv1, pc_csv2]


def read_csv(pc_df):
    pc_data = pd.read_csv(pc_df)    
    pc_data = pc_data.rename(columns = {"Unnamed: 0": 'xs_id'})
    return pc_data

def merge_dataframe(pc_csv):
    pc_df = read_csv(pc_csv)
    left = pc_df
    right = thalweg_data
    result = pd.merge(left, right, on = 'xs_id')
    result = result.loc[:,['xs_id','dmin','d16','d50','d84','d100','distance']]
    return result


##
def make_dict(f_list):   
    x ={}
    for f in f_list:
        df = merge_dataframe(f)     
        x[f] = [df]
    return x

    

def plot_gs_vs_lg(dfs):
    plt.figure(figsize=(20,8),dpi=50, facecolor='white')
    plt.xlabel('Distance(m)')
    plt.yscale('log')
    plt.ylim(0.0001,500)

    colors = ['black', 'green', 'red']
        
    for idx, df in enumerate(dfs):
                       
        y1 = df['dmin']
        y2 = df['d16']
        y3 = df['d50']
        y4 = df['d84']
        y5 = df['d100']
        x = df['distance']

        dmin, = plt.plot(x, y1, '+', color= colors[idx],markersize=5.5)
        d16, = plt.plot(x, y2,'D', color= colors[idx],markersize=5.5)
        d50, = plt.plot(x, y3,'o', color= colors[idx],markersize=8.5)
        d84, = plt.plot(x, y4,'D', color= colors[idx],markersize=5.5)
        d100, = plt.plot(x, y5,'+', color= colors[idx],markersize=5.5)
    #plt.savefig(output_eps,format='eps',dpi=200)

def plot(datalist):
    f_list = make_dict(datalist)
    for key, value in f_list.iteritems():
        plot_gs_vs_lg(value)
    

plot(csv_list)


#==============================================================================
# for j in range(len(df)):
#     df2 = df.iloc[j]
#     for i in range(len(df2)):
#         if i > 0 and i < len(df2)-1:
#             a = np.array([df2[i],df2[len(df2)-1]])
# print a
# df4 = pd.DataFrame(columns = ['a','b'])
# 
# for i in range(10):
#     data = np.random.randint(15, size=(2))
#     df4.loc[i] = data
# 
# data = pd.DataFrame.as_matrix(df4)
# print data
#==============================================================================



#plt.figure(2)
#plt.plot([1,2,3], [1,2,3], 'go-', label='line 1', linewidth=2)





