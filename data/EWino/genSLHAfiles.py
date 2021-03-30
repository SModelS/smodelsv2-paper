#!/usr/bin/env python3

"""Simple code for running SOFTSUSY over a set of input parameters."""

#Uses an input file to loop over input parameters and run SOFTSUSY over them to generate SLHA files.

#First tell the system where to find the modules:
import sys,os,glob,shutil
from configParserWrapper import ConfigParserExt
import logging
import subprocess
import time,datetime
import multiprocessing
import tempfile
import pyslha

FORMAT = '%(levelname)s in %(module)s.%(funcName)s() in %(lineno)s: %(message)s at %(asctime)s'
logging.basicConfig(format=FORMAT,datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)


def getSoftSusyInput(parser):
    """
    Create a input file for running SoftSUSY using the user defined input.

    :param parser: ConfigParser object with all the parameters needed

    :return: The path to the process card
    """
    #Get template file:
    template = parser.get("options","template")
    if not os.path.isfile(template):
        logger.error("Template file %s not found" %template)
        return None

    cardFile = tempfile.mkstemp(suffix='.in', prefix='softsusy_',
                                   dir=os.getcwd())
    os.close(cardFile[0])
    cardFile = os.path.abspath(cardFile[1])
    shutil.copyfile(template,cardFile)
    inputData = pyslha.readSLHAFile(cardFile,ignorenomass=True,ignorenobr=True)

    for block in parser.sections():
        if block.lower() == 'options':
            continue
        for b in inputData.blocks.values():
            label = str(b)
            if label.lower() == block.lower():
                for par,val in parser.items(block):
                    inputData.blocks[label][int(par)] = val

    outStr = inputData.write()
    with open(cardFile,'w') as f:
        f.write(outStr)

    return cardFile

def runSoftSUSY(parserDict):
    """
    Run SoftSUSY using the parameters given in parser.

    :param parser: ConfigParser object with all the parameters needed.
    """
    t0 = time.time()
    parser = ConfigParserExt()
    parser.read_dict(parserDict)

    cardFile = getSoftSusyInput(parser)
    if cardFile is None:
        logger.error("Error generating input file")
        return False
    logger.debug('Input card %s created' %cardFile)

    outputFile = os.path.abspath(parser.get("options","outputFile"))
    outputFolder = os.path.dirname(outputFile)

    #Create output dirs, if do not exist:
    try:
        os.makedirs(outputFolder)
    except:
        pass

    #Run SoftSUSY
    softsusyFolder = os.path.abspath(parser.get("options","softsusyFolder"))
    if not os.path.isdir(softsusyFolder):
        logger.error("SoftSUSY folder %s not found" %softsusyFolder)
        return False
    logger.info('Running SoftSUSY with input file: %s ' %cardFile)
    logger.debug('Running: %s/softpoint.x leshouches < %s' %(softsusyFolder,cardFile))
    run = subprocess.Popen(' %s/softpoint.x leshouches < %s > %s' %(softsusyFolder,cardFile,outputFile)
                       ,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output,errorMsg= run.communicate()
    logger.debug('SoftSUSY error:\n %s \n' %errorMsg)
    logger.debug('SoftSUSY output:\n %s \n' %output)

    logger.info("Done in %3.2f min" %((time.time()-t0)/60.))

    #Remove parton level events:
    if parser.has_option('options','cleanUp') and parser.get('options','cleanUp') is True:
        os.remove(cardFile)

    now = datetime.datetime.now()

    return "Finished running SoftSUSY at %s" %(now.strftime("%Y-%m-%d %H:%M"))

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
    logger.info("Submitting %i jobs over %i cores" %(len(parserList),ncpus))
    for newParser in parserList:
        parserDict = newParser.toDict(raw=False) #Must convert to dictionary for pickling
        print(parserDict)
        p = pool.apply_async(runSoftSUSY, args=(parserDict,))
        children.append(p)
        # time.sleep(1)


    #Wait for jobs to finish:
    output = [p.get() for p in children]
    for out in output:
        print(out)


if __name__ == "__main__":

    import argparse
    ap = argparse.ArgumentParser( description=
            "Run SoftSUSY over a set of input files to compute SLHA files." )
    ap.add_argument('-p', '--parfile', default='softsusy_pars.ini',
            help='path to the parameters file. Default is checkmate_parameters.ini')
    ap.add_argument('-v', '--verbose', default='info',
            help='verbose level (debug, info, warning or error). Default is error')


    t0 = time.time()

    args = ap.parse_args()

    t0 = time.time()

    args = ap.parse_args()
    output = main(args.parfile,args.verbose)

    print("\n\nDone in %3.2f min" %((time.time()-t0)/60.))
