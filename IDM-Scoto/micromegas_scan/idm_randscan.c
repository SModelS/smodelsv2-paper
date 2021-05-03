/*====== Modules ===============
   Keys to switch on 
   various modules of micrOMEGAs  
================================*/
      
//#define MASSES_INFO      
//#define CONSTRAINTS 
//#define OMEGA            
#define DIRECTDETECTION
//#define DECAYS
//#define CROSS_SECTIONS
#define SMODELS 
  
//#define CLEAN   

/*===== End of DEFINE  settings ===== */

#include"../include/micromegas.h"
#include"../include/micromegas_aux.h"
#include"lib/pmodel.h"
#include"Rand.c"

// to compute decay length in meter from decay width in GeV
double decayLength(double width)
{ double ctau;
  if (width>0) ctau = (3E8 / width) / 1.51926778e24; 
  else ctau = INFINITY;
  return ctau;
}

// -2logLikelihood for two parameters (z1,z2); best fit (z10,z20) with plus/minus uncertainties and correlation p
double logLike2d(double z1, double z2, double z10, double sig1p, double sig1m, double z20, double sig2p, double sig2m, double p)
{ double V1 = sig1p*sig1m, V1e = sig1p - sig1m; 
  double V2 = sig2p*sig2m, V2e = sig2p - sig2m; 
  double x1 = (z1-z10), x2 = (z2-z20);
  double V1f = V1 + V1e*x1; 
  double V2f = V2 + V2e*x2; 
  double ll = 1.0/(1-p*p)*(x1*x1/V1f-2*p*x1*x2/sqrt(V1f*V2f)+x2*x2/V2f);
  return ll;
}

// F(m1,m2) for computation of T parameter
double loopF(double m1, double m2)
{ double F;
  F = (m1+m2)/2 - m1*m2/(m1-m2)*log(m1/m2);
  return F;
}

double EWPTchi2(double mH0, double mA0, double mHc)
{
  double mH02,mA02,mHc2,chi2,chi2corr;
  double EE=0.31340;
  mH02 = mH0*mH0;
  mA02 = mA0*mA0;
  mHc2 = mHc*mHc; 

// fits of S,T for U=0: 
// from 1107.0975: S = 0.06 \pm 0.09, T = 0.10 \pm 0.08, correlation: +0.89
// from PDG2019 :  S = 0.02 \pm 0.07, T = 0.06 \pm 0.06, correlation: +0.92
// from PDG2020 :  S = 0.0  \pm 0.07, T = 0.05 \pm 0.06, correlation: +0.92
//  double S0=0.06, dS=0.09, T0=0.10, dT=0.08, corr=0.89;  
  double S0=0., dS=0.07, T0=0.05, dT=0.06, corr=0.92;   
  double S,T;  

  S = ( 1/6*log(mH02/mHc2) - 5/36. + mH02*mA02/3/pow((mA02-mH02),2) 
        + mA02*mA02*(mA02-3*mH02)/6/pow((mA02-mH02),3)*log(mA02/mH02) )/2/M_PI;

  T = (loopF(mHc2,mH02) + loopF(mHc2,mA02) - loopF(mA02,mH02) )/(4*M_PI)/pow((246*EE),2);

  chi2 = pow((S-S0)/dS,2) + pow((T-T0)/dT,2);  // need to add correlation
  chi2corr = logLike2d(S,T, S0,dS,dS, T0,dT,dT, corr);

  printf("EWPO: S = %.3e, T = %.3e, chi2 = %.3e --> %.3e with correlation \n", S,T,chi2,chi2corr);
/*  if (fabs(S-S0)<=2*dS && fabs(T-T0)<=2*dT) printf("      within individual 2 sigma ranges\n"); 
  else  printf("      outside individual 2 sigma ranges\n");  
  if (chi2>5.99) printf("      excluded at 95%% CL w/o correlation\n"); 
  if (chi2corr>5.99) printf("      excluded at 95%% CL with correlation\n"); 
*/
  return chi2corr;
}

/////////////////////////////////////////////////////////////////////////////////////////
// MAIN PROGRAM
/////////////////////////////////////////////////////////////////////////////////////////

int main()
{ int err;
  char cdmName[10];
  int spin2,charge3,cdim;

  ForceUG=0;  /* to Force Unitary Gauge assign 1 */
  //useSLHAwidth=0;

//------------------------------------------------------------------ 
// Declare variables and model parameters for random or MCMC scan   
//------------------------------------------------------------------ 

  double mH0, mA0, mHc, mDM, Mmin=100., Mmax=700.;
  double deltaM, dMmin=0.05, dMmax=200.;
  double lamL, lam2, lam3, lam4, lam5, lamMax=4*M_PI;
  double logdMmin, logdMmax, log4pi=log(4*M_PI), logEps=log(1e-15);
  double chi2, chi2new, chi2old;
//  double x0[10], R0[10], x1[10], R1[10], oldLike, newLike;                              
  int i0, i1, igood=0, iLLP=0, iHSCP=0, iWarn=0, iExcl=0;
  
//  for (i0=0;i0<=10;i0++){ x0[i0]=0.; x1[i0]=0.; }
//  for (i0=0;i0<=100;i0++){ R0[i0]=0.; R1[i0]=0.; }

// for relic density calculation
  int fast=1;
  double Beps=1.E-5, cut=0.01;
  double Omega, Xf=25; 
  double OmegaPlanck=0.12; // value measured by Planck, from 1807.06209
  double delOmega2=pow(0.001,2) + pow((OmegaPlanck/10),2); // exp. error + 10% theory uncertainty

// for direct detection limits
  int sI=1,sD=1;
  double pA0[2],pA5[2],nA0[2],nA5[2];
  double Nmass=0.939; /*nucleon mass*/
  double SCcoeff;        
  double csSIp,csSIn,csSDp,csSDn;
  double pvalFull, pvalRescaled, fOmg;
  char* expName; 

// decays
  double ctauHc;

// SModelS
  int status,smodelsOK;
  double Rvalue;
  char analysis[50]={},topology[100]={},smodelsInfo[100];
  int LHCrun=LHC8|LHC13;  //  LHC8  - 8TeV; LHC13  - 13TeV;   

// output files  
  FILE *fgood =fopen("results/randscan1g.dat", "w");
  fprintf(fgood, "#   mH0       mHc       mA0      lamL     fracDM  DDpval ctau[m]  excl  Rvalue   analysis            topology\n");
  fprintf(fgood, "#---------------------------------------------------------------------------------------------------------------------\n");

/*  FILE *fexcl =fopen("results/exclPoints2.dat", "w");
  fprintf(fexcl, "#   mH0       mHc       mA0      lamL     fracDM  DDpval ctau[m]  excl  Rvalue   analysis            topology\n");
  fprintf(fexcl, "#---------------------------------------------------------------------------------------------------------------------\n");
*/

//--------------------------------------------------------------------- 
// random scan over mH0, mHc-mH0 (log), mA0-mH0, lambdaL (log)  
// use log distribution for mHc-mH0 and lambdaL to favor small values 
//--------------------------------------------------------------------- 

  dMmin = 0.05; 
  dMmax = 0.2; 
  logdMmin=log(dMmin);
  logdMmax=log(dMmax);

int npoints=5000;
for (i0=1;i0<npoints+1;i0++){

//----- 1. random scan over mH0, mHc-mH0 (log), mA0-mH0, lambdaL (log)    
// use log distribution for mHc-mH0 and lambdaL to favor small values 
/*  mH0 = Uniform(Mmin,Mmax);  
  dMmax = 0.5*mH0; logdMmax=log(dMmax);
  deltaM = exp(Uniform(logdMmin,logdMmax));
  mHc = mH0+deltaM;  
  mA0 = (mH0+0.01)*Uniform(1.,1.5);  // mH0 < mH+, mA0
  lamL = exp(Uniform(logEps,log4pi)); 
*/
//----- 1a. random scan over mH0, mHc-mH0 (log), mA0-mH0, lambdaL (log)    
// use log distribution for mHc-mH0 and lambdaL to favor small values 
  mH0 = Uniform(250,700);  
  //deltaM = exp(Uniform(logdMmin,logdMmax));
  deltaM = Normal(0.14,0.005);
  mHc = mH0+deltaM;  
  mA0 = mHc*Uniform(1.,1.4);  // mH0 < mH+, mA0
  lamL = exp(Uniform(logEps,log4pi)); 

//----- 2. random scan over mH0, mHc-mH0<1 GeV, mA0-mH0, lambdaL (log)    
// use log distribution for mHc-mH0 and lambdaL to favor small values 
/*  mH0 = Uniform(100.,800.);  
  mHc = mH0+Uniform(1e-4,1.);  
  mA0 = mH0*Uniform(1.,1.5);  // mH0 < mH+, mA0
  lamL = exp(Uniform(logEps,log4pi)); 
*/
//----- 2.a random scan over mH0, mHc-mH0<1 GeV, mA0-mH0, lambdaL (log)    
// fill region of ctau = 1-10m 
/*  mH0 = Uniform(100.,700.);  
  mHc = mH0+0.1375+0.006*Uniform(0.,1.);  
  mA0 = mH0*Uniform(1.,1.5);  // mH0 < mH+, mA0
  lamL = exp(Uniform(logEps,log4pi)); 
*/
//----- 3. random scan over mH0, mA0, mHc-mA0, lambdaL (log)    
/*  mH0 = exp(Uniform(0,log(200)));
  //mH0 = Uniform(0.,200);
  if(mH0>100) Mmin=mH0;  
  mA0 = Uniform(Mmin,400);   
  mHc = Normal(mA0,5.);  if(mHc<80) continue;
  lamL = 1e-10; 
*/  
//-------------------------------------------------------------------

  printf("\n---------------------------------------------------------------------------------\n");
  printf("%d) random point: %8.3f %8.3f %8.3f  %.3e\n", i0, mH0, mA0, mHc, lamL);

  assignValW("MHX",mH0);
  assignValW("MH3",mA0);
  assignValW("MHC",mHc);
  assignValW("laL",lamL);

  err=sortOddParticles(cdmName);
  if(err) { printf("Can't calculate %s\n",cdmName); return 1;}
   
  printMasses(stdout,1);

  qNumbers(cdmName, &spin2, &charge3, &cdim);
  //printf("Dark matter candidate is '%s' with spin=%d/2\n",cdmName,spin2); 
  if(charge3) { printf("Dark Matter has electric charge %d/3\n",charge3); exit(1);}
  if(cdim!=1) { printf("Dark Matter is a colored particle\n"); exit(1);}

// check lambdas
  lam3 = findValW("la3");
  lam4 = findValW("la4");
  lam5 = findValW("la5");
  printf("lambda_3,4,5 = %.2e %.2e %.2e ... ", lam3,lam4,lam5);
  if (fabs(lam3)>lamMax || fabs(lam4)>lamMax || fabs(lam5)>lamMax) 
  { printf("quartic > 4pi !!\n");
    continue; }
  else printf("ok\n");

// EWPT
  chi2 = EWPTchi2(mH0,mA0,mHc);
  if (chi2>5.99) {
    printf("      excluded at 95%% CL\n"); 
    continue;
  }

// relic density  
  VZdecay=1; VWdecay=1; cleanDecayTable();
  Omega=darkOmega(&Xf,fast,Beps,&err);
  printf("\nOmega = %.2e ... ",Omega);  
  if (Omega<=1.1*OmegaPlanck) printf("ok\n"); 
  else { printf("larger than Planck value + 10%% !!\n"); continue; }
  //if(Omega>0)printChannels(Xf,cut,Beps,1,stdout);   

// direct detection

  fOmg = Omega/OmegaPlanck;
  //printf("Rescaling factor Omega/OmegaPlanck = %.2e \n", fOmg); 
  printf("thermal production gives %4.1f%% of dark matter \n", 100*fOmg); 


  nucleonAmplitudes(CDM1, pA0,pA5,nA0,nA5);
  SCcoeff=4/M_PI*3.8937966E8*pow(Nmass*Mcdm/(Nmass+ Mcdm),2.);
  csSIp=  SCcoeff*pA0[0]*pA0[0];
  csSDp=3*SCcoeff*pA5[0]*pA5[0];
  csSIn=  SCcoeff*nA0[0]*nA0[0];
  csSDn=3*SCcoeff*nA5[0]*nA5[0];
                        
  //printf("\nCDM[antiCDM]-nucleon cross sections[pb]:\n");
  //printf(" proton  SI %.3E  SD %.3E\n", csSIp,csSDp);
  //printf(" neutron SI %.3E  SD %.3E\n", csSIn,csSDn);    
  //printf("Xenon limit = %.2E pb\n", XENON1T_90(Mcdm)/1E-36);  
    
  pvalRescaled=DD_pvalCS(AllDDexp, Maxwell, csSIp*fOmg, csSIn*fOmg, csSDp*fOmg, csSDn*fOmg, &expName);
  printf("DD p-value = %4.2f from %s (DD_pvalCS, rescaled XS)", pvalRescaled, expName);
  if (pvalRescaled>0.1) printf(" ... ok\n"); 
  else { printf(" ... excluded \n"); continue; }
    
  pvalFull=DD_pvalCS(AllDDexp, Maxwell, csSIp, csSIn, csSDp, csSDn, &expName);
  printf("DD p-value = %4.2f from %s (DD_pvalCS, no rescaling)", pvalFull, expName);
  if (pvalFull>0.1) printf(" ... ok\n"); 
  else printf(" ... excluded if all DM\n"); 

/*  pvalFull=DD_pval(AllDDexp, Maxwell, &expName);
  printf("DD p-value = %4.2f from %s (DD_pval, check)", pvalFull, expName);
  if (pvalFull>0.1) printf(" ... ok\n"); 
  else printf(" ... excluded if all DM\n"); 
*/

/*  double DDfac1, DDfac2; 
  DDfac1=DD_factorCS(XENON1T_2018, 0.1, Maxwell, csSIp, csSIn, csSDp, csSDn, &expName);
  printf("XS factor needed for pval=0.1 (all DM):   %.2e from %s\n", DDfac1, expName);
  DDfac2=DD_factorCS(DarkSide_2018, 0.1, Maxwell, csSIp, csSIn, csSDp, csSDn, &expName);
  printf("                                          %.2e from %s\n", DDfac2, expName);
  if (DDfac1>1 && DDfac2>1) 
    printf("Point is safe, no XS scaling necessary\n"); 
  else if (fOmg<DDfac1 && fOmg<DDfac2) 
    printf("Scaling is sufficient to safe point\n"); 
  else 
    printf("Point excluded in any case\n"); 
*/


  igood++;

// charged scalar decays 
  { 
    txtList LZ,Lh;
    double width,br,ctau;
    char * pname;

    if (!VZdecay || ! VWdecay  ){ cleanDecayTable(); VZdecay=1; VWdecay=1;}
    deltaM=mHc-mH0;
    if (deltaM<1.5) assignValW("fpi",0.13);
    else assignValW("fpi",0.);

    pname="~H+";
    width=pWidth(pname,&LZ);
    printf("\n%s :  total width = %.3E GeV\n",pname,width);
    //printTxtList(LZ,stdout);
    ctau=decayLength(width);
    printf("       mean decay length = %.3E m ",ctau);
    if (ctau>1e-3) { 
      ctauHc=ctau;
      iLLP++; 
      printf("--> long lived, deltaM = %6.1f MeV \n", 1000*deltaM); 
      if (deltaM>1) {
        iWarn++;
        printf("*** WARNING: deltaM > 1 GeV ***\n");
      }
    }
    else 
      ctauHc=0.;
      printf("\n");
    if (ctau>10) iHSCP++;

/*    pname="~H3";
    width=pWidth(pname,&LZ);
    printf("\n%s :  total width = %.3E GeV\n",pname,width);
    //printTxtList(LZ,stdout);
    ctau=decayLength(width);
    printf("       mean decay length = %.3E m ",ctau);
    if (ctau>1e-3) printf("--> long lived\n");
    else printf("\n");  
*/

  } // end of decay block


#ifdef SMODELS
{  status=0;
   smodelsOK=0;
   Rvalue=0;

#include "../include/SMODELS.inc" // SLHA interface with SModels:   smodels.slha  ==>  smodels.slha.smodelsslha

   printf("SModelS %s \n",smodelsInfo);
   if(smodelsOK) 
   {  printf(" highest r-value = %.2E",Rvalue); 
      if(Rvalue>0)  printf(" from %s, topology: %s ",analysis,topology);
      if(status==1) { printf("\n excluded"); iExcl++; }
      else if(status==0) printf("\n not excluded"); 
      else if(status==-1) printf("\n not not tested by results in SModelS database"); 
      printf("\n");
   } else system("cat smodels.err"); // problem in version number, downloading or running. See smodels.err
}   
#endif 

  if(status>=0)
    fprintf(fgood, "%9.3f %9.3f %9.3f  %.2e  %.2e  %4.2f  %.2e  %2d  %.2e  %s  '%s'\n", 
                   mH0,mHc,mA0,lamL,fOmg,pvalFull,ctauHc,status,Rvalue,analysis,topology);
  else
    fprintf(fgood, "%9.3f %9.3f %9.3f  %.2e  %.2e  %4.2f  %.2e  %2d  %.2e  %s  %s\n", 
                   mH0,mHc,mA0,lamL,fOmg,pvalFull,ctauHc,status,Rvalue,"none","none");
  fflush(fgood);  

/*  if(status==1){
    fprintf(fexcl, "%9.3f %9.3f %9.3f  %.2e  %.2e  %4.2f  %.2e  %2d  %.2e  %s  '%s'\n", 
                   mH0,mHc,mA0,lamL,fOmg,pvalFull,ctauHc,status,Rvalue,analysis,topology);
    fflush(fexcl);  
  }
*/
}  // --> end of for loop

  printf("\n---------------------------------------------------------------------------------\n");
  printf("Done. Scan summary: %d points, %d good, %d LLP, %d HSCP, %d warnings\n",i0-1,igood,iLLP,iHSCP, iWarn);
  printf("%d points excluded by SModelS \n\n",iExcl);
  fclose(fgood);
//  fclose(fexcl);

  return 0;
}


