#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 12:15:04 2021

@author: humberto
"""

import numpy as np
import xslha
import os
import pandas as pd
import math

def directories():

    gael_dir='/Users/humberto/Documents/work/Scoto-IDM/github/smodelsv2-paper/IDM-Scoto/mhc_scan/IDM_scan_mhc_dm_50/slha/'
    notsoLLP_dir='IDM_scan_mhc_dm_50_mhcdecays/'
    
    return notsoLLP_dir,gael_dir
    


def truncate(number):
    "truncate float to 3 decimal places"
        
    if number<1 and number>1e-90:
    
        provisional_number=number
        order=0
    
        while provisional_number<1:
        
            provisional_number=provisional_number*(10)
            order=order+1
        
    
        factor=10**4
        truncated=(math.trunc(provisional_number * factor) / (factor*10**(order)))
    #elif number>1e-90:    # truncated=0.0
    
    else:
        factor=10**5
        truncated=math.trunc(number * factor) / factor
    return truncated

def get_decay_table(decay_width,old_slha_file):

    slha_read=open(old_slha_file).read()
    new_text='DECAY 37  '+str(decay_width)+'  # ~H+'+'\n   1.0000000   2   9000006 11   #  N1,e'
    new_slha_read=slha_read.replace('DECAY 37  0.000000E+00  # ~H+',new_text)
    
    return new_slha_read
    
def edit_mn1_mass(new_slha_read,mn1):
    new_text='9000006  '+str(mn1)+'  # ~N1'
    new_slha_read=new_slha_read.replace('9000006  1.000000E+00  # ~N1',new_text)
        
    return new_slha_read
    

def create_new_slha(new_slha_file,new_slha_read):

    new_slha_file=open(new_slha_file,'w')
    new_slha_file.write(new_slha_read)
    new_slha_file.close()
    
    return




new_dir,gael_dir=directories()
decay_width_data=pd.read_csv('grid_1gen_Deltam5.dat')



for j in range(decay_width_data.shape[0]):

    

    mhc=decay_width_data['mHch[GeV]'][j]
    mn1=truncate(decay_width_data['mN1[GeV]'][j])
    decay_width=decay_width_data['GammaHch_relic[GeV]'][j]
    
    old_slha_file=gael_dir+'IDM_mhc_'+str(mhc)+'_dm_50_la2_0.01_laL_0.01_.slha'
    new_slha_file=new_dir+'IDM_mhc_'+str(mhc)+'_mn1_'+str(mn1)+'_dm_50_la2_0.01_laL_0.01_.slha'

   
    
    
    new_slha_read=get_decay_table(decay_width,old_slha_file)
    new_slha_read=edit_mn1_mass(new_slha_read,mn1)
    
    create_new_slha(new_slha_file,new_slha_read)
    
    




    
    
    
    
    
