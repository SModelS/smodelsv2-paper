#!/usr/bin/env python3

"""Simple code for removing xsecs from SLHA files."""
#%%
#Uses an input file to loop over input parameters and run SOFTSUSY over them to generate SLHA files.

#First tell the system where to find the modules:
import sys,os,glob,shutil
import logging
import subprocess
import time,datetime
import multiprocessing
import tempfile
import pyslha
import numpy as np

FORMAT = '%(levelname)s in %(module)s.%(funcName)s() in %(lineno)s: %(message)s at %(asctime)s'
logging.basicConfig(format=FORMAT,datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)


infolder = './slha_scanRandom'
outfolder = './slha_scanRandom_pythia6'

#%%
if not os.path.isdir(outfolder):
    os.makedirs(outfolder)

#%%
for f in glob.glob(os.path.join(infolder,'*.slha')):
    print(f)
    with open(f,'r') as ff:
        data = ff.read()
        data = data[:data.find('XSECTION')]
    fnew = os.path.join(outfolder,os.path.basename(f))
    with open(fnew,'w') as ff:
        ff.write(data+'\n')
