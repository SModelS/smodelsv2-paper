#!/usr/bin/env python3

"""Simple code for running Micromegas over a set of input SLHA files."""

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


def runMicroMegas(parserDict):
    """
    Run Micromegas over a single File

    :param parserDict: Dictionary containing the parser.
    """


    t0 = time.time()
    parser = ConfigParserExt()
    parser.read_dict(parserDict)

    if not parser.has_option('options','micromegasExec'):
        logger.error("micromegas executable not defined")
        return False

    microExe = os.path.abspath(parser.get('options','micromegasExec'))
    if not os.path.isfile(microExe):
        logger.error("Could not found Micromegas executable %s" %microExe)
        return False

    inputFile = os.path.abspath(parser.get("options","inputFile"))
    outputFile = parser.get("options","outputFile")
    outputFolder = os.path.abspath(parser.get("options","outputFolder"))
    #Create output dirs, if do not exist:
    try:
        os.makedirs(outputFolder)
    except:
        pass
    #Define absolute path to output file
    if not outputFile:
        outputFile = os.path.basename(inputFile).replace('.slha','')+'.micro'
    outputFile = os.path.join(outputFolder,os.path.basename(outputFile))
    outputFile = os.path.abspath(outputFile)

    microFolder = os.path.dirname(microExe)
    microExe = os.path.basename(microExe)

    logger.debug("Running ./%s %s" %(microExe,inputFile))
    run = subprocess.Popen('./%s %s > %s' %(microExe,inputFile,outputFile)
                   ,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=microFolder)
    output,errorMsg= run.communicate()
    logger.debug('Micromegas error:\n %s \n' %errorMsg)

    logger.debug("Done in %3.2f min" %((time.time()-t0)/60.))
    now = datetime.datetime.now()
    return "Finished running Micromegas at %s" %(now.strftime("%Y-%m-%d %H:%M"))

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
        logger.debug('\n'+str(parserDict)+'\n')
        p = pool.apply_async(runMicroMegas, args=(parserDict,))
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
            "Run Micromegas over a set of files to compute relic density and other observables." )
    ap.add_argument('-p', '--parfile', default='micromegas_pars.ini',
            help='path to the parameters file. Default is micromegas_pars.ini')
    ap.add_argument('-v', '--verbose', default='info',
            help='verbose level (debug, info, warning or error). Default is error')


    t0 = time.time()

    args = ap.parse_args()

    t0 = time.time()

    args = ap.parse_args()
    output = main(args.parfile,args.verbose)

    print("\n\nDone in %3.2f min" %((time.time()-t0)/60.))
