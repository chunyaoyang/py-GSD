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
survey_dir = '/Users/chunyaoyang/GitHub/py-GSD'
# site = 'Bear'
# XS = '4'
# img_out = site+'_XS'+XS
# 
# 
# gs_csv = '%s/%s_PebbleCount_XS%s.csv' % (survey_dir, site, XS)
#==============================================================================


## utility to check if directory exists, if not, create it
def check_dir(f):
    d = os.path.dirname(f)
    if not os.path.isdir(d):
        os.makedirs(d)
    return


def find_csv_filenames(survey_dar, suffix=".csv" ):
    filenames = os.listdir(survey_dar)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]


    
def read_csv():
    f_list = find_csv_filenames(survey_dir)
    keyword = 'PebbleCount'
    for f in f_list:
        if f in keyword:
            f_fullpath = '%s/%s' % (survey_dir, f)
            gs_data = pd.read_csv(f_fullpath, usecols=['size class', 'count'], nrows=18)
            return gs_data        

print gs_data


#==============================================================================
# def cum_pass():
#     gs_data.loc[gs_data['size class'] == '<1', ['size class']] = '0.5'
#     gs_data = gs_data.astype('float').sort('size class')
#     gs_data['size_class'] = gs_data['size class']
#     gs_data['perc'] = gs_data['count']/gs_data['count'].sum()
#     gs_data['count_sum'] = gs_data['count'].cumsum()
#     gs_data['pass_perc'] = (gs_data['count_sum']/gs_data['count'].sum())*100
#     return gs_data
#==============================================================================
        
        
#==============================================================================
# def plot(df):        
#     x = df.loc[:,'size class']
#     y = df.loc[:,'pass_perc']
#     img_out = gs_data[:-3] + 'GSD.eps'
#         
#     plt.subplot(111)
#     plt.plot(x, y, color='black')
#     plt.scatter(x, y, s=10, color='gray')
#     plt.xscale('log')
#     plt.ylim(0, 100)
#     plt.grid(True, which='both')
#     plt.xlabel('Grain Size (mm)')
#     plt.ylabel('Percent Finer')
#     plt.title(img_out)
#     plt.savefig(img_out,format='eps',dpi=200, bbox_inches='tight')  #save figure
#     return
#     
# plot(gs_data)
#==============================================================================
 




#calculating Geometric Mean Size and SD
#DP = np.log(gs_data['size class'])*gs_data['perc']
#GeometricMeanSize = np.exp(DP.sum())
#DP2 = np.square(np.log(gs_data['size class'])- np.log(GeometricMeanSize)) * gs_data['perc']
#SD = np.exp(np.sqrt(DP2.sum()))
#print 'Standard Deviation = ' + str(round(SD,2)) +'.'
#print 'Geometric Mean Size = '+str(round(GeometricMeanSize,2))+' mm.'

                             
          

def getInterpolatedValue(df, x):
    if x not in df.index:
        df.set_value(x, np.nan)
        df = df.sort_index().interpolate(method='index') 
    return df

drop_gs = gs_data.dropna()
df = pd.Series(index=drop_gs.pass_perc, data=drop_gs.size_class.values)
df = getInterpolatedValue(df, 50)
df = getInterpolatedValue(df, 16)
df = getInterpolatedValue(df, 84)




    
print "D16 = " + str(round(df[16],2)) + ', D50 = ' + str(round(df[50],2)) + ', D84 = ' + str(round(df[84],2)) +'.'





    

















