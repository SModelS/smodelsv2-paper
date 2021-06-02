#!/usr/bin/env python3

"""Simple code for running SModelS xseccomputer over a set of input files."""

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


def computeXsecs(parserDict):

    t0 = time.time()
    parser = ConfigParserExt()
    parser.read_dict(parserDict)


    file = os.path.abspath(parser.get("options","file"))
    xsecflags  = parser.get("options","xsecflags")

    if not parser.has_option('options','smodelsFolder'):
        logger.error("smodelsFolder not defined")
        return False

    nevents = int(parser.get('options','nevents'))
    smodelsFolder = os.path.abspath(parser.get('options','smodelsFolder'))
    if not os.path.isdir(smodelsFolder):
        logger.error("Could not found SModelS folder %s" %smodelsFolder)
    else:
        logger.debug("Running ./smodelsTools.py xseccomputer -f %s -e %i -p %s" %(file,nevents,xsecflags))
        run = subprocess.Popen('./smodelsTools.py xseccomputer -f %s -e %i -p %s' %(file,nevents,xsecflags)
                   ,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=smodelsFolder)
        output,errorMsg= run.communicate()
        logger.debug('smodelsTools error:\n %s \n' %errorMsg)
        logger.debug('smodelsTools output:\n %s \n' %output)

    logger.debug("Done in %3.2f min" %((time.time()-t0)/60.))
    now = datetime.datetime.now()
    return "Finished running xseccomputer at %s" %(now.strftime("%Y-%m-%d %H:%M"))

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
    for newParser in parserList[:10]:
        parserDict = newParser.toDict(raw=False) #Must convert to dictionary for pickling
        logger.debug('\n'+str(parserDict)+'\n')
        p = pool.apply_async(computeXsecs, args=(parserDict,))
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
            "Run SModelS xseccomputer over a set of files to compute cross-sections and add them to the input SLHA files." )
    ap.add_argument('-p', '--parfile', default='computeXsecs_pars.ini',
            help='path to the parameters file. Default is checkmate_parameters.ini')
    ap.add_argument('-v', '--verbose', default='info',
            help='verbose level (debug, info, warning or error). Default is error')


    t0 = time.time()

    args = ap.parse_args()

    t0 = time.time()

    args = ap.parse_args()
    output = main(args.parfile,args.verbose)

    print("\n\nDone in %3.2f min" %((time.time()-t0)/60.))
