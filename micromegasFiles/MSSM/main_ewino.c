/*======  Spectrum calculator  =========
   Choose RGE from the list below. SuSpect is included
   in micrOMEGAs, to use another code define the path
   to the corresponding package in lib/Makefile
=====================================*/

// #define RGE  suspect

     /* choose 'suspect','softSusy','spheno', 'tree' */

/*=========   SUSY scenario  ==========
  One can define SUGRA, AMSB, EWSB (for low scale input).
  By default the program reads SLHA data file
=======================================*/
//#define SUGRA
//#define SUGRANUH
//#define AMSB

// #define EWSB

/*====== Modules ===============
   Keys to switch on
   various modules of micrOMEGAs
================================*/

#define MASSES_INFO
      /* Display information about SUSY and Higgs masses
      */
#define CONSTRAINTS
      /* Display  deltarho, B_>sgamma, Bs->mumu, gmuon and
         check LEP mass limits
      */
//#define CheckMassMatrix
#define HIGGSBOUNDS
#define HIGGSSIGNALS
//#define SUPERISO
//#define LILITH
//#define SMODELS
//#define MONOJET

#define OMEGA
      /* Calculate relic density and display contribution of
         individual channels
      */

//#define INDIRECT_DETECTION
      /* Compute spectra of gamma/positron/neutrinos
         for DM annihilation; calculate <sigma*v> and
         integrate gamma signal over DM galactic squared
         density for given line of sight.
      */
//#define LoopGAMMA
      /* Calculate discrete  photon spectrum caused by annihilation of
         neutralinos into two photons and Z-photon
      */

//#define RESET_FORMFACTORS
      /* Modify default nucleus form factors,
         DM velocity distribution,
         A-dependence of Fermi-dencity
      */
#define CDM_NUCLEON
      /* Calculate amplitudes and cross-sections for
         CDM-mucleon collisions
      */
//#define TEST_Direct_Detection
      /*
        Compare analytical formula for DD against micrOMEGAS calculation.
        As well as compare tree level and box improved approaches.
       */
#define CDM_NUCLEUS
     // Calculate  exclusion rate for direct detection experiments Xenon1T and DarkSide50

//#define NEUTRINO
 /*  Neutrino signal of DM annihilation in Sun and Earth */

//#define DECAYS
      /* Calculate decay widths and branchings  */
//#define CROSS_SECTIONS
      /* Calculate cross sections of reactions specified by the user */

/*===== end of Modules  ======*/

/*===== Options ========*/
//#define SHOWPLOTS
     /* Display  graphical plots on the screen */

#define CLEAN    to clean intermediate files

/*===== End of DEFINE  settings ===== */

#include"../include/micromegas.h"
#include"../include/micromegas_aux.h"
#include"lib/pmodel.h"

#define SUGRAMODEL_(A) A ## SUGRA
#define SUGRAMODEL(A) SUGRAMODEL_(A)

#define SUGRANUHMODEL_(A) A ## SUGRAnuh
#define SUGRANUHMODEL(A) SUGRANUHMODEL_(A)

#define AMSBMODEL_(A) A ## AMSB
#define AMSBMODEL(A) AMSBMODEL_(A)

#define EWSBMODEL_(A) A ## EwsbMSSM
#define EWSBMODEL(A) EWSBMODEL_(A)

#define PRINTRGE_(A) printf(" Spectrum calculator is %s\n", #A)
#define PRINTRGE(A)  PRINTRGE_(A)



int main(int argc,char** argv)
{  int err;
   char cdmName[10];
   int spin2, charge3,cdim;

// sysTimeLim=1000;
   ForceUG=0;   /* to Force Unitary Gauge assign 1 */
   //useSLHAwidth=0;
//  nPROCSS=0; /* to switch off multiprocessor calculations */
//   useSLHAwidth=1;

/*
   if you would like to work with superIso
    setenv("superIso","./superiso_v3.1",1);
*/



   printf("\n========= Reading SLHA file =========\n");
   printf("Initial file  \"%s\"\n",argv[1]);
   err=lesHinput(argv[1]);
   if(err==-1)     { printf("Can not open the file\n"); exit(2);}
   else if(err>0)  { printf("Wrong file contents at line %d\n",err);exit(3);}

   err=sortOddParticles(cdmName);

  if(err) { printf("Can't calculate %s\n",cdmName); return 1;}

//  err=treeMSSM();


  qNumbers(cdmName,&spin2, &charge3, &cdim);
  printf("\nDark matter candidate is '%s' with spin=%d/2  mass=%.2E\n",
  cdmName,       spin2, Mcdm);

//  if(charge3) { printf("Dark Matter has electric charge %d/3\n",charge3); exit(1);}
  if(cdim!=1) { printf("Dark Matter is a color particle\n"); exit(1);}
  if(strcmp(cdmName,"~o1")) printf(" ~o1 is not CDM\n");
                              else o1Contents(stdout);


#ifdef MASSES_INFO
{
  printf("\n=== MASSES OF HIGGS AND SUSY PARTICLES: ===\n");
  printHiggs(stdout);
  printMasses(stdout,1);
}
#endif


#ifdef CONSTRAINTS
{ double SMbsg,dmunu,csLim;
  printf("\n\n==== Physical Constraints: =====\n");
  printf("deltartho=%.2E\n",deltarho());
//  printf("gmuon=%.2E\n", gmuon());
  printf("bsgnlo=%.2E ", bsgnlo(&SMbsg)); printf("( SM %.2E )\n",SMbsg);

  printf("bsmumu=%.2E\n", bsmumu());
  printf("btaunu=%.2E\n", btaunu());

  printf("dtaunu=%.2E  ", dtaunu(&dmunu)); printf("dmunu=%.2E\n", dmunu);
  printf("Rl23=%.3E\n", Rl23());
  if(Zinvisible()) printf("Excluded by Z->invisible\n");
  if(LspNlsp_LEP(&csLim)) printf("Excluded by LEP  by e+,e- -> DM q qbar. Cross section =%.2E [pb] \n",csLim);

  if(masslimits()==0) printf("MassLimits OK\n");

  if(blockExists("SPhenoLowEnergy"))
  {
    printf("\n SPheno  low energy observables\n");
    printf("  BR(b -> s gamma)                         %.3E \n", slhaVal("SPhenoLowEnergy",0.,  1,   1   ));
    printf("  BR(b -> s mu+ mu-)                       %.3E \n", slhaVal("SPhenoLowEnergy",0.,  1,   2   ));
    printf("  BR(b -> s nu nu)                         %.3E \n", slhaVal("SPhenoLowEnergy",0.,  1,   3   ));
    printf("  BR(Bd -> e+ e-)                          %.3E \n", slhaVal("SPhenoLowEnergy",0.,  1,   4   ));
    printf("  BR(Bd -> mu+ mu-)                        %.3E \n", slhaVal("SPhenoLowEnergy",0.,  1,   5   ));
    printf("  BR(Bd -> tau+ tau-)                      %.3E \n", slhaVal("SPhenoLowEnergy",0.,  1,   6   ));
    printf("  BR(Bs -> e+ e-)                          %.3E \n", slhaVal("SPhenoLowEnergy",0.,  1,   7   ));
    printf("  BR(Bs -> mu+ mu-)                        %.3E \n", slhaVal("SPhenoLowEnergy",0.,  1,   8   ));
    printf("  BR(Bs -> tau+ tau-)                      %.3E \n", slhaVal("SPhenoLowEnergy",0.,  1,   9   ));
    printf("  BR(B_u -> tau nu)                        %.3E \n", slhaVal("SPhenoLowEnergy",0.,  1,  10   ));
    printf("  BR(B_u -> tau nu)/BR(B_u -> tau nu)_SM   %.3E \n", slhaVal("SPhenoLowEnergy",0.,  1,  11   ));
    printf("  |Delta(M_Bd)| [ps^-1]                    %.3E \n", slhaVal("SPhenoLowEnergy",0.,  1,  12   ));
    printf("  |Delta(M_Bs)| [ps^-1]                    %.3E \n", slhaVal("SPhenoLowEnergy",0.,  1,  13   ));
    printf("  epsilon_K                                %.3E \n", slhaVal("SPhenoLowEnergy",0.,  1,  16   ));
    printf("  Delta(M_K)                               %.3E \n", slhaVal("SPhenoLowEnergy",0.,  1,  17   ));
    printf("  BR(K^0 -> pi^0 nu nu)                    %.3E \n", slhaVal("SPhenoLowEnergy",0.,  1,  18   ));
    printf("  BR(K^+ -> pi^+ nu nu)                    %.3E \n", slhaVal("SPhenoLowEnergy",0.,  1,  19   ));
    printf("  Delta(g-2)_electron/2                    %.3E \n", slhaVal("SPhenoLowEnergy",0.,  1,  20   ));
    printf("  Delta(g-2)_muon/2                        %.3E \n", slhaVal("SPhenoLowEnergy",0.,  1,  21   ));
    printf("  Delta(g-2)_tau/2                         %.3E \n", slhaVal("SPhenoLowEnergy",0.,  1,  22   ));
  }

}
#endif

#ifdef SUPERISO
{
  int err= callSuperIsoSLHA();
  if(err==0)
  { printf("\nSuperIso Flavour MSSM and ( SM)  observables :\n");
    printf("  BR(b->s gamma)                     %.3E  (%.3E)\n", slhaValFormat("FOBS",0.,"    5    1  %lf    0     2     3    22        "), slhaValFormat("FOBSSM",0.,"    5    1  %lf    0     2     3    22        "));
    printf("  Delta0(B->K* gamma)                %.3E  (%.3E)\n", slhaValFormat("FOBS",0.,"  521    4  %lf    0     2   313    22        "), slhaValFormat("FOBSSM",0.,"  521    4  %lf    0     2   313    22        "));
    printf("  BR(B_s->mu+ mu-)                   %.3E  (%.3E)\n", slhaValFormat("FOBS",0.,"  531    1  %lf    0     2    13   -13        "), slhaValFormat("FOBSSM",0.,"  531    1  %lf    0     2    13   -13        "));
    printf("  BR(B_u->tau nu)                    %.3E  (%.3E)\n", slhaValFormat("FOBS",0.,"  521    1  %lf    0     2   -15    16        "), slhaValFormat("FOBSSM",0.,"  521    1  %lf    0     2   -15    16        "));
    printf("  R(B_u->tau nu)                     %.3E  (%.3E)\n", slhaValFormat("FOBS",0.,"  521    2  %lf    0     2   -15    16        "), slhaValFormat("FOBSSM",0.,"  521    2  %lf    0     2   -15    16        "));
    printf("  BR(D_s->tau nu)                    %.3E  (%.3E)\n", slhaValFormat("FOBS",0.,"  431    1  %lf    0     2   -15    16        "), slhaValFormat("FOBSSM",0.,"  431    1  %lf    0     2   -15    16        "));
    printf("  BR(D_s->mu nu)                     %.3E  (%.3E)\n", slhaValFormat("FOBS",0.,"  431    1  %lf    0     2   -13    14        "), slhaValFormat("FOBSSM",0.,"  431    1  %lf    0     2   -13    14        "));
    printf("  BR(B+->D0 tau nu)                  %.3E  (%.3E)\n", slhaValFormat("FOBS",0.,"  521    1  %lf    0     3   421   -15    16  "), slhaValFormat("FOBSSM",0.,"  521    1  %lf    0     3   421   -15    16  "));
    printf("  BR(B+->D0 tau nu)/BR(B+-> D0 e nu) %.3E  (%.3E)\n", slhaValFormat("FOBS",0.,"  521   11  %lf    0     3   421   -15    16  "), slhaValFormat("FOBSSM",0.,"  521   11  %lf    0     3   421   -15    16  "));
    printf("  BR(K->mu nu)/BR(pi->mu nu)         %.3E  (%.3E)\n", slhaValFormat("FOBS",0.,"  321   11  %lf    0     2   -13    14        "), slhaValFormat("FOBSSM",0.,"  321   11  %lf    0     2   -13    14        "));
    printf("  R_mu23                             %.3E  (%.3E)\n", slhaValFormat("FOBS",0.,"  321   12  %lf    0     2   -13    14        "), slhaValFormat("FOBSSM",0.,"  321   12  %lf    0     2   -13    14        "));
  }
}
#endif



#if defined(HIGGSBOUNDS) || defined(HIGGSSIGNALS)
{  int NH0=3, NHch=1; // number of neutral and charged Higgs particles.
   int HB_id[3]={0,0,0},HB_result[3];
   double  HB_obsratio[3],HS_observ=-1,HS_chi2, HS_pval;
   char HB_chan[3][100]={""}, HB_version[50], HS_version[50];
   NH0=hbBlocksMO("HB.in",&NHch);
   system("echo 'BLOCK DMASS\n 25  2  '>> HB.in");
#include "../include/hBandS.inc"
#ifdef HIGGSBOUNDS
   printf("HiggsBounds(%s)\n", HB_version);
   for(int i=0;i<3;i++) if(HB_id[i]) printf("  id= %d  result = %d  obsratio=%.2E  channel= %s \n", HB_id[i],HB_result[i],HB_obsratio[i],HB_chan[i]);
#endif
#ifdef HIGGSSIGNALS
   if(HS_observ>=0)
   {
     printf("HiggsSignals(%s)\n",HS_version);
     printf("  Nobservables=%.0f chi^2 = %.2E pval= %.2E\n",HS_observ,HS_chi2, HS_pval);
   }
#endif
}
#endif

#ifdef LILITH
{  double m2logL, m2logL_reference=0,pvalue;
   int exp_ndf,n_par=0,ndf;
   char  Lilith_version[50];
   if( LilithMO("Lilith_in.xml"))
   {
#include "../include/Lilith.inc"
      if(ndf)
      {
        printf("LILITH(DB%s):  -2*log(L): %.2f; -2*log(L_reference): %.2f; ndf: %d; p-value: %.2E \n",
        Lilith_version,m2logL,m2logL_reference,ndf,pvalue);
      }
   } else printf("LILITH: there is no Higgs candidate\n");
}
#endif


#ifdef OMEGA
{ int fast=1;
  double Beps=1.E-5, cut=0.01;
  double Omega,Xf=25;

// to exclude processes with virtual W/Z in DM   annihilation
//    VZdecay=0; VWdecay=0; cleanDecayTable();

// to include processes with virtual W/Z  also  in co-annihilation
   VZdecay=2; VWdecay=2; cleanDecayTable();

  printf("\n==== Calculation of relic density =====\n");

//  sortOddParticles(cdmName);

   Omega=darkOmega(&Xf,fast,Beps,&err);
   printf("Xf=%.2e Omega=%.2e\n",Xf,Omega);

   if(Omega>0)printChannels(Xf,cut,Beps,1,stdout);
/*
   Omega=darkOmega2(fast,Beps);
   displayPlot("Y","T",Tend,Tstart, 0,2,"Y",0,YF,NULL,"Y1",0,Y1F,NULL);
   printf("Omega2=%e\n",Omega);
*/

// direct access for annihilation channels

/*
if(omegaCh){
  int i;
  for(i=0; omegaCh[i].weight>0  ;i++)
  printf(" %.2E %s %s -> %s %s\n", omegaCh[i].weight, omegaCh[i].prtcl[0],
  omegaCh[i].prtcl[1],omegaCh[i].prtcl[2],omegaCh[i].prtcl[3]);
}
*/

// to restore default switches


    VZdecay=1; VWdecay=1; cleanDecayTable();

}
#endif



#ifdef RESET_FORMFACTORS
{
/*
   The user has approach to form factors  which specifies quark contents
   of  proton and nucleon via global parametes like
      <Type>FF<Nucleon><q>
   where <Type> can be "Scalar", "pVector", and "Sigma";
         <Nucleon>     "P" or "N" for proton and neutron
         <q>            "d", "u","s"

   calcScalarQuarkFF( Mu/Md, Ms/Md, sigmaPiN[MeV], sigmaS[MeV])
   calculates and rewrites Scalar form factors
*/

  printf("protonFF (default) d %E, u %E, s %E\n",ScalarFFPd, ScalarFFPu,ScalarFFPs);
  printf("neutronFF(default) d %E, u %E, s %E\n",ScalarFFNd, ScalarFFNu,ScalarFFNs);


//                    To restore default form factors of  version 2  call
     calcScalarQuarkFF(0.553,18.9,55.,243.5);

  printf("protonFF (new)     d %E, u %E, s %E\n",ScalarFFPd, ScalarFFPu,ScalarFFPs);
  printf("neutronFF(new)     d %E, u %E, s %E\n",ScalarFFNd, ScalarFFNu,ScalarFFNs);


//                    To restore default form factors of  current version  call
//  calcScalarQuarkFF(0.56,20.2,34,42);

}
#endif

#ifdef CDM_NUCLEON
{ double pA0[2],pA5[2],nA0[2],nA5[2];
  double Nmass=0.939; /*nucleon mass*/
  double SCcoeff;
  double csSIp,csSIn,csSDp,csSDn;
  int sI,sD;
printf("\n==== Calculation of CDM-nucleons amplitudes  =====\n");

    nucleonAmplitudes(CDM1,pA0,pA5,nA0,nA5);
    printf("%s-nucleon micrOMEGAs amplitudes:\n",CDM1);
    printf("proton:  SI  %.3E  SD  %.3E\n",pA0[0],pA5[0]);
    printf("neutron: SI  %.3E  SD  %.3E\n",nA0[0],nA5[0]);

    SCcoeff=4/M_PI*3.8937966E8*pow(Nmass*Mcdm/(Nmass+ Mcdm),2.);
    csSIp=  SCcoeff*pA0[0]*pA0[0];
    csSDp=3*SCcoeff*pA5[0]*pA5[0];
    csSIn=  SCcoeff*nA0[0]*nA0[0];
    csSDn=3*SCcoeff*nA5[0]*nA5[0];

    printf("\n==== %s-nucleon cross sections[pb] ====\n",CDM1);
    printf(" proton  SI %.3E  SD %.3E\n",csSIp,csSDp);
    printf(" neutron SI %.3E  SD %.3E\n",csSIn,csSDn);

    if(pA0[0]*nA0[0]<0) sI=-1; else sI=1;
    if(pA5[0]*nA5[0]<0) sD=-1; else sD=1;
    char*expName="";
    double pval=DD_pvalCS(AllDDexp, Maxwell, csSIp, sI*csSIn,csSDp,sD*csSDn, &expName);
    if(pval<0.1 )  printf("Excluded by %s [CDM_NUCLEON] %.1f%% \n", expName, 100*(1-pval));
    else printf("Not excluded by DD experiments  at 90%% level \n");
}
#endif

#ifdef CDM_NUCLEUS
{ char* expName;
  printf("\n===== Direct detection exclusion:======\n");
  double pval=DD_pval(AllDDexp, Maxwell, &expName);
       if(pval<0.1 )  printf("Excluded by %s [CDM_NUCLEUS]  %.1f%%\n", expName, 100*(1-pval));
  else printf("Not excluded by DD experiments  at 90%% level \n");
}
#endif

  return 0;
}
