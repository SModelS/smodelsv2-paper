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
import shutil

def writePar(parName, mh0, ma0, mhc, la2, laL):

    with open(parName, 'w') as out:
        out.write('Mtp     175.0\n')
        out.write('MHX     %s\n' % mh0)
        out.write('MH3     %s\n' % ma0)
        out.write('MHC     %s\n' % mhc)
        out.write('laL     %s\n' % laL)
        out.write('la2     %s\n' % la2)
        out.write('Mh      125\n')



la2=0.01
laL=0.01
#laL=1e-10

#meta2,lPhi,delta1,deltaA,lHPhi1,lHPhi2=translate(mh0,ma0,mhc,la2,laL)
dm = 5
scanFolder = "IDM_scan_mhc_dm_" + str(dm)
if os.path.exists(scanFolder):
    shutil.rmtree(scanFolder)
os.makedirs(scanFolder)
SLHA = os.path.join(scanFolder, "slha")
os.makedirs(SLHA)
PAR = os.path.join(scanFolder, "par")
os.makedirs(PAR)

for m in range(100, 1001, 300):
    mh0 = m + dm
    ma0 = m + dm + 1E-3
    mhc = m
    out = "IDM_mhc_" + str(mhc) + "_dm_" + str(dm) + "_la2_" + str(la2) + "_laL_" + str(laL)
    outPar = os.path.join(PAR, out+"_.par")
    outSlha = os.path.join(SLHA, out+"_.slha")
    writePar(outPar, mh0, ma0, mhc, la2, laL)
    os.system("./main " + outPar)
    os.system("mv smodels.slha " + outSlha)
