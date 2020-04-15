# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 11:29:14 2020

@author: KevinL
"""
import pandas as pd

def sma(depth,vals):
    sma_depth = pd.Series(depth.size-vals)
    
    for ii in range(vals-1,depth.size):
        temp = 0
        zz = 0
        while zz <vals:
            temp = temp + depth[ii-zz]
            zz = zz+1
        temp = temp/vals       
        sma_depth[ii-(vals-1)] = temp
    
    
    return  sma_depth
    
    sma(depth)
    
    