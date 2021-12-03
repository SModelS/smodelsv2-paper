#!/usr/bin/env python3

"""Simple code for warpping information from multiple SLHA files in a single object."""

#Uses an input file to loop over input parameters and run SOFTSUSY over them to generate SLHA files.

#First tell the system where to find the modules:
import sys,os,glob,shutil
import logging
import subprocess
import time,datetime
import multiprocessing
import tempfile
import pyslha

FORMAT = '%(module)s.%(funcName)s() in %(lineno)s: %(message)s'
logging.basicConfig(format=FORMAT,datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)



class SLHAScan(object):


    def __init__(self,slhafiles= [])

        self.slhafiles = []
        self.slhaData = []
        for f in slhafiles:
            if not os.path.isfile(f):
                continue
            try:
               data = pyslha.readSLHAFile(f)
               self.slhafiles.append(f)
               self.slhaData.append(data)
            except:
               logger.warning("Error loading %s" %f)

   def __getattr__(self,attr):
