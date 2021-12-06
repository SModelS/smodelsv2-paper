# smodelsv2-paper
A repository to store the code and data for the SModelS v2 physics paper



## Scan Data ##

Due to GitHub storage limitations the data (SLHA files, SModelS and Micromegas output) are stored in CERNBox.

### EW-ino random scan data ###

The data for the EW-ino scan can be downloaded from CERNBox
using:

``
wget https://cernbox.cern.ch/index.php/s/gE7wsm4GQf2GHTw/download -O EWinoData.tar.gz
``

The tarball contains 3 folders containing
the SLHA files (slha_scanRandom), the SModelS output (smodels_scanRandom) and the Micromegas output (micromegas_scanRandom).


### Scotogenic Scan data ###

#### Scalar DM Scenario ####

The data for the scalar DM scenario (SLHA files and SModelS output) scan can be downloaded from CERNBox
using:


``
wget https://cernbox.cern.ch/index.php/s/BtynYoh6QiEWraP/download -O ScotoScalarDMData.tar.gz
``

The tarball contains 2 folders containing the SLHA files (slha) and the SModelS output (smodelsOutput).


#### Fermionic DM Scenario ####

The data for the Fermionic DM scenario (SLHA files and SModelS output) scan can be downloaded from CERNBox
using:


``
wget https://cernbox.cern.ch/index.php/s/XossUMgVmjksVO2/download -O ScotoFermionDMData.tar.gz
``

The tarball contains 2 folders containing the SLHA files (slha) and the SModelS output (smodelsOutput).
Each folder has the following structure:

 * mhc_electronic_decays: scenario with BR(H<sup>+</sup> -> e<sup>+</sup> + N<sub>1</sub>) = 100%
   * deltam_5: scan with m<sub>H<sup>0<sup></sub>-m<sub>H<sup>+<sup></sub> = 5 GeV
   * deltam_50: scan with m<sub>H<sup>0<sup></sub>-m<sub>H<sup>+<sup></sub> = 50 GeV
 * mhc_muonic_decays: scenario with BR(H<sup>+</sup> -> mu<sup>+</sup> + N<sub>1</sub>) = 100%
   * deltam_5: scan with m<sub>H<sup>0<sup></sub>-m<sub>H<sup>+<sup></sub> = 5 GeV
   * deltam_50: scan with m<sub>H<sup>0<sup></sub>-m<sub>H<sup>+<sup></sub> = 50 GeV
 * mhc_mixed_decays: scenario with BR(H<sup>+</sup> -> e<sup>+</sup> + N<sub>1</sub>) =  BR(H<sup>+</sup> -> mu<sup>+</sup> + N<sub>1</sub>) = 50%
   * deltam_5: scan with m<sub>H<sup>0<sup></sub>-m<sub>H<sup>+<sup></sub> = 5 GeV
   * deltam_50: scan with m<sub>H<sup>0<sup></sub>-m<sub>H<sup>+<sup></sub> = 50 GeV

## Results and Plotting ##

### EW-ino ###

The SLHA input and SModelS output can be easily combined using Pandas DataFrames and stored
as a pickle file, as shown in [EWino/results/getEWinoData.ipynb](EWino/results/getEWinoData.ipynb).

For plotting the results using the DataFrame pickle file, see [EWino/results/plots-EWinoScan.ipynb](EWino/results/plots-EWinoScan.ipynb)

### Scotogenic Scalar DM ###

The SLHA input and SModelS output can be read and plotted using the notebook example
 [IDM-Scoto/scalar_DM_scenario/plotScotoScalarExample.ipynb](IDM-Scoto/scalar_DM_scenario/plotScotoScalarExample.ipynb).


## Running the scans

### Basic Installation ###

The script installer.sh will try to fetch and install the following packages:

  * [smodels](https://smodels.github.io/)
  * [SoftSUSY](https://softsusy.hepforge.org/)  
  * [Prospino](https://www.thphys.uni-heidelberg.de/~plehn/index.php?show=prospino)
  * [Micromegas](https://lapth.cnrs.fr/micromegas/)    

The Prospino installation includes small [changes to the Prospino code](prospinoModFiles) in order to make it easier to run the code in parallel.
The required Micromegas files are stored in [micromegaFiles](micromegaFiles) and compiled during installation.



### EW scan ###

The main scripts generating the SLHA files using SoftSUSY and computing the cross-sections (using SModelS or Prospino) are:

  * [EWino/genSLHAfiles.py](EWino/genSLHAfiles.py) : runs a scan to compute the SUSY spectrum using SoftSUSY and compute cross-sections using SModelS
  * [EWino/computeXsecs.py](EWino/computeXsecs.py) : compute cross-sections using SModelS for a set of SLHA files
  * [EWino/computeXsecs_prospino.py](EWino/computeXsecs_prospino.py) : compute cross-sections using Prospino for a set of SLHA files (only cross-sections for combinations of C1,N1 and N2 are included!)

The input of the above scripts are controlled by par (.ini) files stored in the [EWino](EWino) folder.    

The SModelS output is computed using the runSModelS.py script with this [parameter file](EWino/smodels_parameters.ini)
