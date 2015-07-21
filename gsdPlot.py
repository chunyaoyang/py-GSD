# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 08:29:53 2015

@author: chunyaoyang
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


survey_dir = '/Users/chunyaoyang/GitHub/py-GSD'
site = 'Bear'
XS = '1'
img_out = site+'_XS'+XS


gs_csv = '%s/%s_PebbleCount_XS%s.csv' % (survey_dir, site, XS)


gs_data = pd.read_csv(gs_csv, usecols=['size class', 'count'], nrows=18)

#replace '<1' to '0.5'
gs_data.loc[gs_data['size class'] == '<1', ['size class']] = '0.5'

#covert to float and rearrange size class
gs_data = gs_data.astype('float').sort('size class')

#
gs_data['size_class'] = gs_data['size class']
gs_data['perc'] = gs_data['count']/gs_data['count'].sum()
gs_data['count_sum'] = gs_data['count'].cumsum()
gs_data['pass_perc'] = (gs_data['count_sum']/gs_data['count'].sum())*100
DP = np.log(gs_data['size class'])*gs_data['perc']
GeometricMeanSize = np.exp(DP.sum())
DP2 = np.square(np.log(gs_data['size class'])- np.log(GeometricMeanSize)) * gs_data['perc']
SD = np.exp(np.sqrt(DP2.sum()))
print 'Standard Deviation = ' + str(SD) +'.'
print 'Geometric Mean Size = '+str(GeometricMeanSize)+' mm.'


drop_gs = gs_data.dropna()
#drop_gs = drop_gs.set_index('pass_perc')
drop_gs = drop_gs['size class', 'pass_perc']
#print drop_gs
#idx = pd.Index(np.arange(30,50))
#drop_gs.reindex(drop_gs.index + idx).interpolate(method='values')

print drop_gs
#s = pd.Series(index=drop_gs.pass_perc, data=drop_gs.size_class.values).order().interpolate(method='index')
#print s



# plot GSD
x = gs_data.loc[:,'size class']  #why loc
y = gs_data.loc[:,'pass_perc']  

fig = plt.figure()
ax = plt.subplot(111)
plt.plot(x, y, color='black')
plt.scatter(x, y, s=10, color='gray')
plt.xscale('log')
plt.ylim(0, 100)
plt.grid(True, which='both')
plt.xlabel('Grain Size (mm)')
plt.ylabel('Percent Finer')
plt.title(site+' Cross Section '+XS)


#plt.savefig(img_out,format='eps',dpi=200, bbox_inches='tight')













