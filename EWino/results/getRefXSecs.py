#!/usr/bin/env python3

""" python script to add the reference cross sections to slha files.
The cross sections have been scraped off from
https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections
and stored in the xsec*.txt files. """

import os, subprocess, sys
import pyslha

def getXSecFor (pid1, pid2, mass, sqrts, ewk='wino'):
    """ add to file F cross sections for pid1, pid2
    :param order: perturbation order that we should claim this to be
                  (LO=0, NLO=1, NLL=2, ... )
    :param comment: comment to be added to xsec line
    """

    xsecs = getXSecsDictFor(pid1, pid2, sqrts, ewk )
    xsec = interpolate ( mass, xsecs )
    if xsec == None:
        xsec = 0.0

    return xsec

def interpolate ( mass, xsecs ):
    """ interpolate between masses """
    if mass in xsecs:
        return xsecs[mass]
    # if mass < min(xsecs.keys()):
    #     print ( "[addRefXSecs] mass %d<%d too low to interpolate, leave it as is."  % ( mass, min(xsecs.keys() ) ) )
    #     return None
    # if mass > max(xsecs.keys()):
    #     print ( "[addRefXSecs] mass %d>%d too high to interpolate, leave it as is." % ( mass, max(xsecs.keys() ) ) )
    #     return None
    from scipy.interpolate import interp1d
    return interp1d ( list(xsecs.keys()), list(xsecs.values()), bounds_error=False,fill_value="extrapolate" )( mass )

def getXSecsFrom ( filename, pb = True, columns={"mass":0,"xsec":1 } ):
    """ retrieve xsecs from filename
    :param pb: xsecs given in pb
    :param indices: the indices of the columns in the table, for mass and xsec
    """
    ret = {}
    if not os.path.exists ( filename ):
        print ( "[addRefXSecs] could not find %s" % filename )
        return ret
    # print ( "getting xsecs from %s" % filename )
    f = open ( filename, "rt" )
    lines=f.readlines()
    f.close()
    for line in lines:
        if line.find("#")>-1:
            line = line[:line.find("#")]
        if "mass [GeV]" in line: ## skip
            continue
        tokens = line.split ()
        if len(tokens)<2:
            continue
        mass = float(tokens[ columns["mass"] ])
        xsec = float(tokens[ columns["xsec"] ].replace("GeV","") )
        if not pb:
            xsec = xsec / 1000.
        ret[ mass ] = xsec
    return ret

def getXSecsDictFor ( pid1, pid2, sqrts, ewk ):
    """ get the xsec dictionary for pid1/pid2, sqrts
    :param ewk: specify the ewkino process (hino, or wino)
    """
    filename=None
    order = 0
    pb = True
    columns = { "mass": 0, "xsec": 1 }
    isEWK=False
    comment=""
    if pid1 in [ 1000021 ] and pid2 == pid1:
        filename = "xsecgluino%d.txt" % sqrts
        columns["xsec"]=2
        isEWK=False
        order = 2 # 4
    if pid1 in [ -1000024 ] and pid2 in [ 1000023 ]:
        filename = "xsecN2C1m%d.txt" % sqrts
        order = 2
        isEWK=True
        pb = False
    if pid1 in [ 1000023 ] and pid2 in [ 1000024 ]:
        filename = "xsecN2C1p%d.txt" % sqrts
        order = 2
        pb = False
        isEWK=True
    if pid1 in [ 1000023 ] and pid2 in [ 1000023 ]:
        filename = "xsecN2N1p%d.txt" % sqrts
        order = 2
        pb = False
        isEWK=True
    if pid1 in [ 1000024 ] and pid2 in [ 1000025 ]:
        filename = "xsecN2C1p%d.txt" % sqrts
        order = 2
        pb = False
        isEWK=True
    if pid1 in [ -1000024 ] and pid2 in [ 1000025 ]:
        filename = "xsecN2C1m%d.txt" % sqrts
        order = 2
        isEWK=True
        pb = False
    if pid1 in [ -1000005, -1000006, -2000006 ] and pid2 == -pid1:
        ## left handed slep- slep+ production.
        filename = "xsecstop%d.txt" % sqrts
        order = 2 #3
        columns["xsec"]=2
        pb = True
    if pid1 in [ -1000024 ] and pid2 == -pid1:
        ## left handed slep- slep+ production.
        filename = "xsecC1C1%d.txt" % sqrts
        order = 2 #3
        pb = False
    if pid1 in [ -1000011, -1000013, -1000015 ] and pid2 == -pid1:
        ## left handed slep- slep+ production.
        filename = "xsecslepLslepL%d.txt" % sqrts
        order = 2 #3
    if pid1 in [ -2000011, -2000013, -2000015 ] and pid2 == -pid1:
        filename = "xsecslepRslepR%d.txt" % sqrts
        order = 2 # 3
    if filename == None:
        print ( "[addRefXSecs] could not identify filename for xsecs" )
        print ( "              seems like we dont have ref xsecs for the pids %d/%d?" % ( pid1, pid2 ) )
        sys.exit()
    if ewk == "hino":
        filename = filename.replace(".txt","hino.txt" )
    if isEWK:
        comment = " (%s)" % ewk
    filename = os.path.join('./refXsecs',filename)
    if not os.path.exists ( filename ):
        print ( "[addRefXSecs] %s missing" % filename )
        sys.exit()
    xsecs = getXSecsFrom ( filename, pb, columns )
    return xsecs
