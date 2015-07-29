# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 08:29:53 2015

Get D16, D50, D84, Geometric Mean Size, Geometric Standard Deviation and Plot the Grain Size Distribution
based on pebble count result.

Require: csv files of pebble count result
Desired format:  
filename: <siteName>_PebbleCount_XS<no.>.csv
setup csv files for first column: [size class], unit: millimeter, second column: [count]

and run $python gsplot.py <FolderPath> <Summary.CSV>

@author: chunyaoyang, phantasise
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys


def find_csv_filenames(filePath, suffix=".csv" ):
    filenames = os.listdir(filePath)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]


#compute percents finer in order of ascending size
def cum_pass(gs_data):
    gs_data.loc[gs_data['size class'] == '<1', ['size class']] = '0.5'
    gs_data = gs_data.astype('float').sort('size class')
    gs_data[np.isnan(gs_data)] = 0        #replace NaN with 0
    gs_data['log2_size'] = np.log2(gs_data['size class'])    #log2(size)
    gs_data['perc'] = gs_data['count']/gs_data['count'].sum()
    gs_data['count_sum'] = gs_data['count'].cumsum()
    gs_data['pass_perc'] = (gs_data['count_sum']/gs_data['count'].sum())*100
    return gs_data



def plot(df, path, title, ext='eps'):        
    plt.clf()
    x = df.loc[:,'size class']
    y = df.loc[:,'pass_perc']
        
    plt.subplot(111)
    plt.plot(x, y, color='black')
    plt.scatter(x, y, s=10, color='gray')
    plt.xscale('log')
    plt.ylim(0, 100)
    plt.grid(True, which='both')
    plt.xlabel('Grain Size (mm)')
    plt.ylabel('Percent Finer')
    plt.title(title)
    plt.savefig(path + "/" + title + "." + ext, format=ext, dpi=200, bbox_inches='tight')  #save figure



def getInterpolatedValue(df, x):
    if x not in df.index:
        df.set_value(x, np.nan)
        df = df.sort_index().interpolate(method='index') 
    return df

#extrapolate D0 for computing geometric mean size and geometric standard deviation
def extrapolate_zero(df):
    if 0 not in df.index:
        dzero = df.iget(1)+(((df.iget(0)-df.iget(1))/(df.index[0]-df.index[1]))*(-df.index[1]))
        df.set_value(0, dzero)
        df = df.sort_index()
    return df

def calothers(gs_data):   
    df = pd.Series(index=gs_data.pass_perc, data=gs_data.log2_size.values)   
    df = extrapolate_zero(df)
    mean_psi = 0  #mean grain size on psi scale
    sd_psi = 0   #SD on psi scale 
    
    #compute mean grain size on psi scale
    for i in range(len(df.index)):
        if i+1 < len(df.index):
            a = (df.iget(i+1)+df.iget(i))*0.5*(df.index[i+1]-df.index[i])/100
            mean_psi += a
    #compute SD on psi scale        
    for i in range(len(df.index)):
        if i+1 < len(df.index):
            a = np.square(((df.iget(i+1)+df.iget(i))*0.5)-mean_psi)*(df.index[i+1]-df.index[i])/100
            sd_psi += a
   
    #compute D16, D50, D84
    df = getInterpolatedValue(df, 50)
    df = getInterpolatedValue(df, 16)
    df = getInterpolatedValue(df, 84)
    return [round(2**df[16], 3), round(2**df[50], 3), round(2**df[84], 3), round(2**mean_psi, 3), round(2**np.sqrt(sd_psi), 3)]  

def reduce_data(origin_data, count_sum):
    end = len(origin_data["count_sum"])
    
    for idx, val in enumerate(origin_data["count_sum"]):
        if val == 100:
            end = idx + 1
            break
    reduce_gs_data = origin_data[:end]

    return reduce_gs_data

def read_csv(survey_dir, summaryCSV):
    if not os.path.exists(survey_dir):
        print('Filepath does not exist')
    elif not os.path.isdir(survey_dir):
        print('Filepath is not a directory!')
    
    f_list = find_csv_filenames(survey_dir)
    keyword = 'PebbleCount'
    
    summary_df = pd.DataFrame(columns=['d16','d50','d84','Geometric mean size','SD'])
    is_process = False
    
    for f in f_list:
        if keyword in f:
            if not is_process:
                is_process = True
            print("Process " + f + "......")
            f_fullpath = '%s/%s' % (survey_dir, f)
            gs_data = pd.read_csv(f_fullpath, usecols=['size class', 'count'], nrows=18)
            title = f[0:f.find('_')] + "_" + f[f.rfind('_') + 1:f.rfind('.')]
            gs_data = cum_pass(gs_data)
            reduce_gs_data = reduce_data(gs_data, 100)
            plot(reduce_gs_data, survey_dir, title, "eps")
            summary_data = calothers(gs_data)
            summary_df.loc[f[f.rfind('_') + 1:f.rfind('.')]] = summary_data
    
    if is_process:
        summary_df.to_csv(summaryCSV, encoding='utf-8')

if __name__ == '__main__':
    if len(sys.argv) == 3:
        read_csv(sys.argv[1], sys.argv[2])
    else:
        print("ERROR. Command should have the form:")
        print("python gsdplot.py <Input File Path> <Output File>")
        exit(1)
