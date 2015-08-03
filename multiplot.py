import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

def plot(dfs, path, title, ext='eps'):
    plt.clf()
    
    colors = ['black', 'gray', 'red']
    plt.title(title)
    plt.ylim(0, 100)
    plt.grid(True, which='both')
    plt.xlabel('Grain Size (mm)')
    plt.ylabel('Percent Finer')
    plt.xscale('log')
    
    for idx, df in enumerate(dfs):
        x = df.loc[:,'size class']
        y = df.loc[:,'pass_perc']
        
        plt.plot(x, y, color=colors[idx])
        plt.scatter(x, y, s=10, color=colors[idx])
    
    plt.savefig(path + "/" + title + "." + ext, format=ext, dpi=200, bbox_inches='tight')