#!/usr/bin/env python3

"""Simple code for running Prospino over a set of input files."""

#First tell the system where to find the modules:
import sys,os,glob,shutil
from configParserWrapper import ConfigParserExt
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

def getPDGsFrom(process,id1,id2):
    """
    Gets the pdgs of the produced particles from Prospino process and id notation.
    """

    if process != "nn":
        logger.error("Conversion for process %s not defined. Stopping.")
        return None
    pdgsDict = {1 : 1000022, 2 : 1000023, 3: 1000025, 4 : 1000035,
                5 : 1000024, 6 : 1000037, 7 : -1000024, 8 : -1000037}
    if not id1 in pdgsDict:
        logger.error("Conversion for id1 = %is not defined." %id1)
        return None
    if not id2 in pdgsDict:
        logger.error("Conversion for id2 = %is not defined." %id2)
        return None

    pdgs = [pdgsDict[id1],pdgsDict[id2]]
    pdgs = sorted(pdgs)

    return pdgs

def prospino2SLHA(prospino_out,slhafile,sqrts):
    """
    Converts the Prospino output (xxx.dat file) to a XSECTION block and add it to the slhafile.
    """

    if not os.path.isfile(prospino_out):
        logger.debug("Prospino output %s not found" %prospino_out)
        return
    if not os.path.isfile(slhafile):
        logger.debug("SLHA filet %s not found" %slhafile)
        return

    with open(prospino_out,'r') as f:
        prospinoData = f.readlines()

    xsecDict = {}
    f = open(slhafile,'a')
    for l in prospinoData:
        if not l.strip(): continue
        if l.strip()[0] == '#': continue
        if "LO" in l: continue
        vals = l.split()
        process = vals[0]
        id1 = eval(vals[1])
        id2 = eval(vals[2])
        xsecNLO_pb = eval(vals[11])
        pdgs = getPDGsFrom(process,id1,id2)
        block = '\nXSECTION  %1.2e  2212 2212 2 %i %i # [pb], Prospino for NLO\n' %(sqrts,pdgs[0],pdgs[1])
        block += '  0  1  0  0  0  0    %1.5e \n' %(xsecNLO_pb)
        f.write(block)

    f.close()

def computeProspinoXsecs(parserDict):

    t0 = time.time()
    parser = ConfigParserExt()
    parser.read_dict(parserDict)


    file = os.path.abspath(parser.get("options","file"))

    if not parser.has_option('options','prospinoFolder'):
        logger.error("Prospino folder not defined")
        return False

    prospinoFolder = os.path.abspath(parser.get('options','prospinoFolder'))
    if not os.path.isdir(prospinoFolder):
        logger.error("Could not found Prospino folder %s" %prospinoFolder)
        return False

    if parser.has_option('options','sqrts'):
        sqrtsList = parser.get('options','sqrts')
        if isinstance(sqrtsList,(float,int)):
            sqrtsList = [sqrtsList]
    else:
        sqrtsList = [8000.,13000.]

    for sqrts in sqrtsList:
        logger.debug("Running ./prospino_ewino.run %s %s" %(file,sqrts))
        run = subprocess.Popen('./prospino_ewino.run %s %s' %(file,sqrts)
                   ,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=prospinoFolder)
        output,errorMsg= run.communicate()
        logger.debug('Prospino error:\n %s \n' %errorMsg)
        logger.debug('Prospino output:\n %s \n' %output)

        #Clean up prospino output
        f2 = os.path.join(prospinoFolder,file+'.dat2')
        if os.path.isfile(f2):
            os.remove(f2)
        f3 = os.path.join(prospinoFolder,file+'.dat3')
        if os.path.isfile(f3):
            os.remove(f3)

        #Extract prospino cross-sections:
        f1 = os.path.join(prospinoFolder,file+'.dat')
        if not os.path.isfile(f1):
            continue

        prospino2SLHA(f1,file,sqrts)
        os.remove(f1)

    logger.debug("Done in %3.2f min" %((time.time()-t0)/60.))
    now = datetime.datetime.now()
    return "Finished running Prospino at %s" %(now.strftime("%Y-%m-%d %H:%M"))

def main(parfile,verbose):
    """
    Submit parallel jobs using the parameter file.

    :param parfile: name of the parameter file.
    :param verbose: level of debugging messages.
    """
    level = args.verbose.lower()
    levels = { "debug": logging.DEBUG, "info": logging.INFO,
               "warn": logging.WARNING,
               "warning": logging.WARNING, "error": logging.ERROR }
    if not level in levels:
        logger.error ( "Unknown log level ``%s'' supplied!" % level )
        sys.exit()
    logger.setLevel(level = levels[level])

    parser = ConfigParserExt(inline_comment_prefixes=';')
    ret = parser.read(parfile)
    if ret == []:
        logger.error( "No such file or directory: '%s'" % parfile)
        sys.exit()

    parserList = parser.expandLoops()

    ncpus = int(parser.get("options","ncpu"))
    if ncpus  < 0:
        ncpus =  multiprocessing.cpu_count()
    ncpus = min(ncpus,len(parserList))
    pool = multiprocessing.Pool(processes=ncpus)
    children = []
    #Loop over parsers and submit jobs
    for newParser in parserList:
        parserDict = newParser.toDict(raw=False) #Must convert to dictionary for pickling
        # Check if files already containing Prospino cross-sections should be skipped
        if 'skipFiles' in parserDict['options']:
            skipFiles = parserDict['options']['skipFiles']
        else:
            skipFiles = False
        if skipFiles:
            logger.info('Skipping files containing Prospino cross-sections')
            filename = parserDict['options']['file']
            with open(filename,'r') as f:
                if 'Prospino for NLO' in f.read():
                    continue
        logger.debug('\n'+str(parserDict)+'\n')
        p = pool.apply_async(computeProspinoXsecs, args=(parserDict,))
        children.append(p)
        # time.sleep(1)

    print("Submitted %i jobs over %i cores" %(len(children),ncpus))
    # logger.info("Submitted %i jobs over %i cores" %(len(children),ncpus))

    #Wait for jobs to finish:
    output = [p.get() for p in children]
    for out in output:
        logger.debug(str(out))


if __name__ == "__main__":

    import argparse
    ap = argparse.ArgumentParser( description=
            "Run Propsino over a set of files to compute cross-sections and add them to the input SLHA files." )
    ap.add_argument('-p', '--parfile', default='computeXsecs_prospino_pars.ini',
            help='path to the parameters file. Default iscomputeXsecs_prospino_pars.ini')
    ap.add_argument('-v', '--verbose', default='info',
            help='verbose level (debug, info, warning or error). Default is error')


    t0 = time.time()

    args = ap.parse_args()

    t0 = time.time()

    args = ap.parse_args()
    output = main(args.parfile,args.verbose)

    print("\n\nDone in %3.2f min" %((time.time()-t0)/60.))
