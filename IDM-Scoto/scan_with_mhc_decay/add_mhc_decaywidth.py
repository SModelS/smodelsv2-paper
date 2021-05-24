#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 12:15:04 2021

@author: humberto
"""

import numpy as np
import xslha
import os


def directories():
    
    old_dir='sample_slhas/'
    new_dir='sample_new_slhas/'
    return old_dir,new_dir
    


def yukawa1(m1,mhc,mh0,ma0):

    y1=(2e-9)*np.sqrt(10*10e-6/m1)*np.sqrt((mhc+mh0+ma0)/(100))
    
    
    return y1
    
def decay_width(m1,mhc,mh0,ma0):
    
    y1=yukawa1(m1,mhc,mh0,ma0)
    Gamma=((1-m1**2/mhc**2)**2)*(mhc*(y1**2))/(16*np.pi)
    
    return Gamma
    
def ctau(m1,mhc,mh0,ma0):

    gamma=decay_width(m1,mhc,mh0,ma0)
    hbar=6.582119569e-16*10e-9
    c=299792458
    ctau=c*hbar/(gamma)


    return ctau




def get_masses(old_dir,slha_file):

    spc=xslha.read(old_dir+slha_file)
    mhc=spc.Value('MASS',[37])
    ma0=spc.Value('MASS',[36])
    mh0=spc.Value('MASS',[35])
    m1=spc.Value('MASS',[9000006])
    
    return mhc,ma0,mh0,m1
    
def get_decay_table(decay_width,slha_file,old_dir):

    slha_read=open(old_dir+slha_file).read()
    new_text='DECAY 37  '+str(decay_width)+'  # ~H+'+'\n   1.0000000   2   9000006 11   #  N1,e'
    new_slha_read=slha_read.replace('DECAY 37  0.000000E+00  # ~H+',new_text)
    
    return new_slha_read

def create_new_slha(slha_file,new_dir,new_slha_read):

    new_slha_file=open(new_dir+slha_file,'w')
    new_slha_file.write(new_slha_read)
    new_slha_file.close()
    
    return


old_dir,new_dir=directories()

slha_files=os.listdir(old_dir)



for slha_file in slha_files:

    
    mhc,ma0,mh0,m1=get_masses(old_dir,slha_file)
    gamma=decay_width(m1,mhc,mh0,ma0)
    new_slha_read=get_decay_table(gamma,slha_file,old_dir)
    
    create_new_slha(slha_file,new_dir,new_slha_read)
    
    

    






'''
    
mhc=98
ma0=mhc+5
mh0=ma0
m1=1e-5


y1=yukawa1(m1,mhc,ma0,mh0)
gamma=decay_width(m1,mhc,ma0,mh0)
ctau=ctau(m1,mhc,ma0,mh0)

print('y1:'+str(y1))
print('gamma:'+str(gamma))
print('ctau:'+str(ctau))
'''


    
    
    
    
    
