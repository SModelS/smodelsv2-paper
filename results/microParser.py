#!/usr/bin/env python3

"""Simple code for converting the micrOmegas output to a python dictionary."""

#First tell the system where to find the modules:
import sys,os,glob,shutil
import logging
import numpy as np
import time

FORMAT = '%(levelname)s in %(module)s.%(funcName)s() in %(lineno)s: %(message)s at %(asctime)s'
logging.basicConfig(format=FORMAT,datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)

def micro2Py(mfile,relicContributions=False):
    outputDict = {}
    if not os.path.isfile(mfile):
        print('File %s not found' %mfile)
        return outputDict

    with open(mfile,'r') as f:
        output = f.read()
        #Get block for physical constraints
        physConst = output.split('==== Physical Constraints: =====')[1].split('===')[0]
        obs_dict = {}
        for l in physConst.split('\n'):
            if not l.strip(): continue
            if '=' in l:
                line = l[:]
                while '=' in line:
                    label = line.split('=',1)[0].strip()
                    line = line.split('=',1)[1]
                    val = line.split()[0].strip() #Get value
                    line = line.replace(val,'',1)
                    try:
                        val = eval(val)
                    except:
                        pass
                    obs_dict[label] = val
            elif 'MassLimits' in l:
                if l.split()[1].strip() == 'OK':
                    val = True
                else:
                    val = False
                obs_dict['MassLimits'] = val
                break

        #Get block for relic density
        relic = output.split('==== Calculation of relic density',1)[1]
        relic = relic.split('\n====')[0]
        relic = relic.split('\n')
        channels = None
        if relicContributions:
            channels = []
            for i,chan in enumerate(relic):
                if "contributions" in chan:
                    break
            for l in relic[i+1:]:
                if '->' in l:
                    l = l.strip()
                    frac = l.split(' ',1)[0]
                    frac = eval(frac.replace('%',''))/100.0
                    chan = l.split(' ',1)[1]
                    chan = chan.strip()
                    channels.append([frac,chan])
            obs_dict['ChannelsRelic'] = channels

        line = relic[1]
        while '=' in line:
            if not line.strip():
                continue
            label = line.split('=',1)[0].strip()
            line = line.split('=',1)[1]
            val = line.split()[0].strip() #Get value
            line = line.replace(val,'',1)
            try:
                val = eval(val)
            except:
                pass
            obs_dict[label] = val


        #Get block for CDM nucleon cross-section
        CDMxsec = output.split('==== ~o1-nucleon cross sections[pb] ====')[1].split('===')[0]
        CDMxsec = CDMxsec.split('\n')
        for l in CDMxsec:
            l = l.strip()
            if not l: continue
            nucleons = ['proton','neutron']
            for nucleon in nucleons:
                if nucleon in l:
                    l = l.replace(nucleon,'')
                    l = l.strip()
                    l = l.split()
                    labels = ['%s_%s'%(nucleon,v) for v in l[::2]]
                    vals = [eval(v) for v in l[1::2]]
                    for i,label in enumerate(labels):
                        obs_dict[label] = vals[i]
    return obs_dict

if __name__ == "__main__":

    import argparse
    ap = argparse.ArgumentParser( description=
            "Reads the micrOmegas output and convert to a python dictionary." )
    ap.add_argument('-f', '--file',required=True,
            help='path to the micromegas output file.')
    ap.add_argument('-v', '--verbose', default='info',
            help='verbose level (debug, info, warning or error). Default is error')


    t0 = time.time()

    args = ap.parse_args()

    t0 = time.time()

    args = ap.parse_args()
    output = micro2Py(args.file,relicContributions=True)
    print(output)
