#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 12:15:04 2021

@author: humberto

Modified on Thu Apr 01 2021

@author: Gaël Alguero
"""

import numpy as np
import sys
import os




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

def writePar(parName, pars):

    meta2,lPhi,delta1,deltaA,lHPhi1,lHPhi2 = translate(*pars)

    with open(parName, 'w') as out:
        out.write('emeta2     %s\n' % meta2)
        out.write('lPhi       %s\n' % lPhi)
        out.write('delta1     %s\n' % delta1)
        out.write('deltaA     %s\n' % deltaA)
        out.write('lHPhi1     %s\n' % lHPhi1)
        out.write('lHPhi2     %s\n' % lHPhi2)
        out.write('lvarphi    0.\n')
        out.write('lHvarphi   0.\n')
        out.write('lPhivarphi 0.\n')
        out.write('emN1       1\n')
        out.write('emN2       100000\n')
        out.write('etheta     0.\n')


la2=0.01
laL=0.01
#laL=1e-10

#meta2,lPhi,delta1,deltaA,lHPhi1,lHPhi2=translate(mh0,ma0,mhc,la2,laL)

scanFolder = "scoto_scan_mhc_dm_" + str(dm)
if os.path.exists(scanFolder):
    os.rmdir(scanFolder)
os.makedirs(scanFolder)
SLHA = os.path.join(scanFolder, "slha")
os.makedirs(SLHA)
PAR = os.path.join(scanFolder, "par")
os.makedirs(PAR)

dm = 5
for m in range(100, 1001, 300):
    mh0 = m
    ma0 = m + 1E-3
    mhc = m + dm
    pars = [mh0, ma0, mhc, la2, laL]
    out = "scoto_mhc_" + str(mhc) + "_dm_" + str(dm) + "_la2_" + str(la2) + "_laL_" + str(laL)
    outPar = os.path.join(PAR, out)
    outSlha = os.path.join(SLHA, out)
    writePar(outPar, pars)
    os.system("./main " + outPar)
    os.system("cp smodels.slha " + outSlha)
