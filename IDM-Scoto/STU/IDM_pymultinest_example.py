from __future__ import absolute_import, unicode_literals 
import pymultinest
import math
import commands
import os
import threading, subprocess
import sys

# path to micromegas input parameter file and executable, ADJUST!
MO_PARAM_IN_DM = "/your/path/to/micromegas/ScotoIDM/data.par"
MO_EXE_DM = "/your/path/to/micromegas/ScotoIDM/main"


# path to where MN chains should be stored, ADJUST!
if not os.path.exists("/your/path/to/chains"): os.mkdir("/your/path/to/chains")
def show(filepath): 
	""" open the output (pdf) file for the user """
	if os.name == 'mac': subprocess.call(('open', filepath))
	elif os.name == 'nt': os.startfile(filepath)
	elif os.name == 'posix': subprocess.call(('xdg-open', filepath))

# path to where MN chains should be stored, ADJUST!
if len(sys.argv)==2:
	chains = "/your/path/to/chains/"+str(sys.argv[1])
else:
	chains = "/your/path/to/chains/testrun"
	print "Warning: Please provide run name as argument! Used name 'testrun'.";


def run_micro(param):
    
    mh = param['mh']
    mH0 = param['MHO']
    mA0 = param['MAO']
    mHch = param['MHch']
    lamL = param['lamL']
    lam2 = param['lam2']
    
    OMEGAH2_Planck = 0.12
    # write data.par
    string = "# file to improve default parameters \nmh "+str(mh)+"\nMH0 "+str(mH0)+"\nMA0 "+str(mA0)+"\nMHch "+str(mHch)+"\nlamL "+str(lamL)+"\nlam2 "+str(lam2)    # to be added for HEFT: # +"\nformfacAAH "+str(formfacAAH)+"\nformfacGGH "+str(formfacGGH)
    with open (MO_PARAM_IN_DM, 'w') as f: f.write (string)

    # run MO
    status, output = commands.getstatusoutput(MO_EXE_DM+" "+MO_PARAM_IN_DM)
    omegah2 = extract_contr('Omegah\^2= ','\n',output) 
    if omegah2 < 0:
        omegah2 = 1e-10
    
    if omegah2 >= OMEGAH2_Planck:
        chi2 = (omegah2 - OMEGAH2_Planck)**2/(OMEGAH2_Planck*0.1)**2 # 10% error (not fully correct if theory error but ok...)
    else:
        chi2 = 0.0
    loglikeli_OM = - chi2/2.0 
        
    out = {
        'omegah2': omegah2,
        'loglikeli_OM': loglikeli_OM,
    }
    par = dict(param)
    par.update(out)
    return par

def fFT(m1,m2):
    if m1==m2:
        f_here = 0.0
    else:  
        f_here = 0.5*(m1**2+m2**2) - m1**2*m2**2*math.log(m1**2/m2**2)/(m1**2-m2**2)
    return f_here
    
def run_STU(param):
    
    mh = param['mh']
    mH0 = param['MHO']
    mA0 = param['MAO']
    mHch = param['MHch']
    lamL = param['lamL']
    lam2 = param['lam2']
    
    vev = 246.0
    alpha_ew = 0.007818608

    # TO BE UPDATED!
    S_OBS = 0.06
    T_OBS = 0.097
    """
    the inverse covariance matrix for S,T (inverse of sigma = [[0.00846976, 0.00630211], [0.00630211, 0.00566263]] )
    extracted from fig.4 of 1407.3792v1
    """
    invSigma = array([[ 686.83506807 ,-764.39925456],[ -764.39925456 , 1027.31914078]])

#    # from hep-ph/0603188:
#    integrand = lambda x: x*(1.0-x)*math.log((x*mH0**2+(1.0-x)*mA0**2)/mHch**2)
#    oblpar_S = 1.0/(2.0*math.pi)*integrate.quad(integrand,0.0,1.0,limit=100000,epsabs=1e-4, epsrel=1e-6)[0]
    oblpar_T = 1.0/(16.0*math.pi**2*vev**2*alpha_ew)*( fFT(mHch,mH0) + fFT(mHch,mA0) - fFT(mA0,mH0) )
    # just found in 1107.0975 [eq. (24)]:
    oblpar_S = 1.0/(2.0*math.pi)*(1.0/6.0*math.log(mH0**2/mHch**2)- 5.0/36.0 + mH0**2*mA0**2/(3.0*(mA0**2 - mH0**2)**2)+ mA0**4*(mA0**2-3.0*mH0**2)/(6.0*(mA0**2-mH0**2)**3)*math.log(mA0**2/mH0**2))

    delta = [oblpar_S-S_OBS,oblpar_T-T_OBS]
    
    st_chisq = 0.0

    for i in range(len(invSigma)):
        for j in range(len(invSigma)):
            st_chisq+=(delta[i])*invSigma[i,j]*(delta[j])

    loglikeli_prefactor_ST = 4.93404197589
    loglikeli_ST = loglikeli_prefactor_ST - st_chisq/2.0 
    
    outd = {    
            'oblpar_S': oblpar_S,
            'oblpar_T': oblpar_T,
            #
            'chi2_ST': st_chisq,
            'll_ST': loglikeli_ST,
           }
    par = dict(param)
    par.update(outd)
    
    return par;
    
def logpriorflat(lower,upper,randvar):
	outvar = lower*math.exp(randvar*math.log(upper/lower))
	return outvar;


def myprior(cube, ndim, nparams):
	
	mH0 = logpriorflat(100.0,2000.0,cube[0])
	mA0 = logpriorflat(MH0+0.01,3000.0,cube[1])
	mHch = mA0 - min(mA0-mH0,0.4*mA0) + 0.8*mA0*cube[2]
	lamL = logpriorflat(1e-3,12,cube[3])
	lam2 = logpriorflat(1e-3,12,cube[3])
	
	cube[0]=mH0
	cube[1]=mA0
	cube[2]=mHch
	cube[3]=lamL
	cube[4]=lam2
	
def myloglike(cube, ndim, nparams):

	mH0=cube[0]
	mA0=cube[1]
	mHch=cube[2]
	lamL=cube[3]
	lam2=cube[4]

	param = {
		'mh': 125.1,
		'MHO': mH0,
		'MAO': mA0,
		'MHch': mHch,
		'lamL': lamL, 
		'lam2': lam2, 
	}
	
	# run micromegas and compute likelihoods
	param = run_micro(param)
    param = run_STU(param)   
	
	fit_likelihood = param['ll_ST']+param['loglikeli_OM']

    cube[5] =  param['omegah2']
    cube[6] =  param['loglikeli_OM']
    cube[7] =  param['oblpar_S']
    cube[8] =  param['oblpar_T']
    cube[9] =  param['chi2_ST']
    cube[10] =  param['ll_ST']
    		
	param = {}

	return fit_likelihood;


parameters = [
				# IN PARAMS:
				"MH0", "MA0", "MHch", "lamL", "lam2",
				# results
				"omegah2", "loglikeli_OM", "oblpar_S", "oblpar_T", "chi2_ST", "ll_ST", 
            ] 
		   
n_params = len(parameters)

pymultinest.run(myloglike, myprior, n_params, importance_nested_sampling = False, resume = False, verbose = True,  sampling_efficiency = 0.5, n_live_points = 1000, evidence_tolerance = 0.1, outputfiles_basename=chains, log_zero = -1.0e99,n_iter_before_update = 50)

# For convenience: write file with header in the end
header = "#                     weight                        -2ll "+(" ").join(str(x).rjust(27) for x in parameters)+"\n"
open(chains+"data.dat", "w").write(header+open(chains+".txt").read())


