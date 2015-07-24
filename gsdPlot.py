# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 08:29:53 2015

@author: chunyaoyang
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

#==============================================================================
def find_csv_filenames(filePath, suffix=".csv" ):
    filenames = os.listdir(filePath)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]
#==============================================================================

#==============================================================================
def cum_pass(gs_data):
    gs_data.loc[gs_data['size class'] == '<1', ['size class']] = '0.5'
    gs_data = gs_data.astype('float').sort('size class')
    gs_data['size_class'] = gs_data['size class']
    gs_data['perc'] = gs_data['count']/gs_data['count'].sum()
    gs_data['count_sum'] = gs_data['count'].cumsum()
    gs_data['pass_perc'] = (gs_data['count_sum']/gs_data['count'].sum())*100
    return gs_data
#==============================================================================

#==============================================================================
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
# plot(gs_data)
#==============================================================================

#==============================================================================
def getInterpolatedValue(df, x):
    if x not in df.index:
        df.set_value(x, np.nan)
        df = df.sort_index().interpolate(method='index') 
    return df
#==============================================================================

#==============================================================================
def calothers(gs_data):
    #calculating Geometric Mean Size and SD
    DP = np.log(gs_data['size class']) * gs_data['perc']
    GeometricMeanSize = np.exp(DP.sum())
    DP2 = np.square(np.log(gs_data['size class']) - np.log(GeometricMeanSize)) * gs_data['perc']
    SD = np.exp(np.sqrt(DP2.sum()))
    # print 'Standard Deviation = ' + str(round(SD,2)) +'.'
    # print 'Geometric Mean Size = '+str(round(GeometricMeanSize,2))+' mm.'

    drop_gs = gs_data.dropna()
    df = pd.Series(index=drop_gs.pass_perc, data=drop_gs.size_class.values)
    df = getInterpolatedValue(df, 50)
    df = getInterpolatedValue(df, 16)
    df = getInterpolatedValue(df, 84)

    return [round(df[16], 2), round(df[50], 2), round(df[84], 2), round(GeometricMeanSize, 2), round(SD, 2)]
#==============================================================================

def read_csv(survey_dir, summaryCSV):
    if not os.path.exists(survey_dir):
        print('Filepath does not exist')
    elif not os.path.isdir(survey_dir):
        print('Filepath is not a directory!')
    
    f_list = find_csv_filenames(survey_dir)
    keyword = 'PebbleCount'
    
    summary_df = pd.DataFrame(columns=['d16','d50','d84','Geometric Mean Size', 'SD'])
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
            plot(gs_data, survey_dir, title)
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