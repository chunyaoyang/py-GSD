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




def run(self):
    # Get the number of arguments
    numArgs = len(sys.argv)
    # Check there are only 2 input argument (i.e., the input file
    # and output base).
    # Note that argument 0 (i.e., sys.argv[0]) is the name
    # of the script uncurrently running.
    if numArgs == 3:
        # Retrieve the input directory
        filePath = sys.argv[1]
        # Retrieve the output file
        summaryCSV = sys.argv[2]

        # Check input file path exists and is a directory
        if not os.path.exists(filePath):
            print 'Filepath does not exist'
        elif not os.path.isdir(filePath):
            print 'Filepath is not a directory!'
    else:
        print "ERROR. Command should have the form:"
        print "python gsdplot.py <Input File Path> <Output File>"





def find_csv_filenames(filePath, suffix=".csv" ):
    filenames = os.listdir(filePath)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]


    
def read_csv():
    f_list = find_csv_filenames(survey_dir)
    keyword = 'PebbleCount'
    for f in f_list:
        if f in keyword:
            f_fullpath = '%s/%s' % (survey_dir, f)
            gs_data = pd.read_csv(f_fullpath, usecols=['size class', 'count'], nrows=18)
            return gs_data        




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





    

















