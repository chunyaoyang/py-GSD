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
import multiplot


def find_csv_filenames(filePath, suffix=".csv" ):
    filenames = []
    paths = []
    for root, dirs, files in os.walk(filePath):
        for file in files:
            if file.endswith(suffix):
                paths.append(root + "/")
                filenames.append(file)
    return paths, filenames


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
#def extrapolate_zero(df):
#    if len(df) > 1:
#        if 0 not in df.index:
#            dzero = df.iget(1)+(((df.iget(0)-df.iget(1))/(df.index[0]-df.index[1]))*(-df.index[1]))
#            df.set_value(0, dzero)
#            df = df.sort_index()
#    if len(df) == 1:
#        dzero = df.iloc[0]
#        df.set_value(0, dzero)
#        df = df.sort_index()
#    return df

def calothers(gs_data):   
    df = pd.Series(index=gs_data.pass_perc, data=gs_data.log2_size.values)
#    df = extrapolate_zero(df)
#    mean_psi = 0  #mean grain size on psi scale
#    sd_psi = 0   #SD on psi scale 
#    
#    #compute mean grain size on psi scale
#    for i in range(len(df.index)):
#        if i+1 < len(df.index):
#            a = (df.iget(i+1)+df.iget(i))*0.5*(df.index[i+1]-df.index[i])/100
#            mean_psi += a
#            break
#    #compute SD on psi scale        
#    for i in range(len(df.index)):
#        if i+1 < len(df.index):
#            a = np.square(((df.iget(i+1)+df.iget(i))*0.5)-mean_psi)*(df.index[i+1]-df.index[i])/100
#            sd_psi += a
#            break
   
    #compute D16, D50, D84
    df = getInterpolatedValue(df, 50)
    df = getInterpolatedValue(df, 16)
    df = getInterpolatedValue(df, 84)
    df = getInterpolatedValue(df, 25)
    df = getInterpolatedValue(df, 75)
    dmin=df.min(); d16=df[16].min(); d25=df[25].min(); d50=df[50].min(); d75=df[75].min(); d84=df[84].min() #choose the smaller value if there are more than one


    return [round(2**dmin,3), round(2**d16, 3), round(2**d25, 3), round(2**d50, 3), round(2**d75, 3), round(2**d84, 3), round(2**df[100], 3)]  

def reduce_data(origin_data, pass_perc):
    start = 0
    end = len(origin_data["pass_perc"])
    
    last_val = -1
    for idx, val in enumerate(origin_data["pass_perc"]):
        if val != 0 and last_val == 0:
            start = idx - 1
        if val == pass_perc:
            end = idx + 1
            break
        last_val = val
    reduce_gs_data = origin_data[start:end]

    return reduce_gs_data

def addtofnames(fnames_dict, fname, df):
    if fname not in fnames_dict.keys():
        fnames_dict[fname] = list()
    fnames_dict[fname].append(df)

def read_csv(survey_dir):
    if not os.path.exists(survey_dir):
        print('Filepath does not exist')
    elif not os.path.isdir(survey_dir):
        print('Filepath is not a directory!')

    keyword = 'PebbleCount'
    
    summary_df = pd.DataFrame(columns=['dmin','d16','d25','d50','d75','d84','d100'])
    is_process = False
    
    same_fnames = dict()
    
    suffix = ".csv"
    for root, dirs, files in os.walk(survey_dir):
        f_path = root + "/"
        out_csv = ""
        for fname in files:
            if fname.endswith(suffix) and keyword in fname:
                print("Process " + f_path + fname + "......")
                try:
                    gs_data = pd.read_csv(f_path + fname, usecols=['size class', 'count'], nrows=18)
                    title = fname[0:fname.find('_')] + "_" + fname[fname.rfind('_') + 1:fname.rfind('.')]
                    gs_data = cum_pass(gs_data)
                    reduce_gs_data = reduce_data(gs_data, 100)
                    plot(reduce_gs_data, f_path, title, "eps")
                    addtofnames(same_fnames, fname, reduce_gs_data)
                    summary_data = calothers(reduce_gs_data)
                    summary_df.loc[fname[fname.rfind('_') + 1:fname.rfind('.')]] = summary_data
                    out_csv = f_path + fname[0:fname.find('_')] + '_summary.csv'
                    
                except ValueError:
                    print "Read Error...Skip"
                    pass
        if out_csv != "":
            summary_df.to_csv(out_csv, encoding='utf-8')
        
    for key, value in same_fnames.iteritems():
        if len(value) > 1:
            multiplot.plot(value, survey_dir, key[0:key.find('_')] + "_" + key[key.rfind('_') + 1:key.rfind('.')], "eps")
        
if __name__ == '__main__':
    if len(sys.argv) == 2:
        read_csv(sys.argv[1])
    else:
        print("ERROR. Command should have the form:")
        print("python gsdplot.py <Input File Path>")
        exit(1)
