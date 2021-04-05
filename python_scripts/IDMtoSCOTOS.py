#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 12:15:04 2021

@author: humberto
"""

import numpy as np




def translate(mh0,ma0,mhc,la2,laL):
    ''' Translate IDM variables to Scoo_singlet variables '''
    
    
    lPhi=la2
    
    #setting extra scalar to heavy masses so is effectively decoupled
    meta2=5000
    #Theta set two zero, so heavy scalar is not involved
    theta=0
    
    delta1=mh0-meta2
    deltaA=ma0-meta2
    
    vev=246.22

    
    lHPhi2=(mhc**2-.5*ma0**2-.5*mh0**2*np.cos(theta)**2-.5*meta2**2*np.sin(theta)**2)*(-2/vev**2)
    
    lHPhi1=2*laL-lHPhi2-(1/vev**2)*(mh0**2*np.cos(theta)**2+meta2**2*np.sin(theta)-ma0**2)
    
    
    return meta2,lPhi,delta1,deltaA,lHPhi1,lHPhi2
    
    
    
    
mh0=500.000
ma0=510.00
mhc=502.
la2=0.01
#laL= -.5
laL=1e-10

#meta2,lPhi,delta1,deltaA,lHPhi1,lHPhi2=translate(mh0,ma0,mhc,la2,laL)    
print(translate(mh0,ma0,mhc,la2,laL))
    
    
    
    
    
    
    
    
    
