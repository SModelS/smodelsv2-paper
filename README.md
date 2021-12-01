# smodelsv2-paper
A repository to store the code and data for the SModelS v2 physics paper


## Basic Installation ##

The script installer.sh will try to fetch and install the following packages:

  * [smodels](https://smodels.github.io/)
  * [SoftSUSY](https://softsusy.hepforge.org/)  
  * [Prospino](https://www.thphys.uni-heidelberg.de/~plehn/index.php?show=prospino)
  * [Micromegas](https://lapth.cnrs.fr/micromegas/)    

The Prospino installation includes small [changes to the Prospino code](prospinoModFiles) in order to make it easier to run the code in parallel.
The required Micromegas files are stored in [micromegaFiles](micromegaFiles) and compiled during installation.


## Running the scans

### EW scan ###

The main scripts generating the SLHA files using SoftSUSY and computing the cross-sections (using SModelS or Prospino) are:

  * [EWino/genSLHAfiles.py](EWino/genSLHAfiles.py) : runs a scan to compute the SUSY spectrum using SoftSUSY and compute cross-sections using SModelS
  * [EWino/computeXsecs.py](EWino/computeXsecs.py) : compute cross-sections using SModelS for a set of SLHA files
  * [EWino/computeXsecs_prospino.py](EWino/computeXsecs_prospino.py) : compute cross-sections using Prospino for a set of SLHA files (only cross-sections for combinations of C1,N1 and N2 are included!)

The input of the above scripts are controlled by par (.ini) files stored in the [EWino](EWino) folder.    

The SModelS output is computed using the runSModelS.py script with this [parameter file](EWino/smodels_parameters.ini)

## Analysing Results and Plotting ##

The SLHA input and SModelS output can be easily combined using Pandas DataFrames and stored
as a pickle file, as shown in [EWino/results/getEWinoData.ipynb](EWino/results/getEWinoData.ipynb).

For plotting the results using the DataFrame pickle file, see [EWino/results/plots-EWinoScan.ipynb](EWino/results/plots-EWinoScan.ipynb)

## Data ##

Due to GitHub storage limitations the data (SLHA files, SModelS and Micromegas output) are stored in CERNBox.

### EWino random scan data ###

The data for the EW-ino scan can be download from CERNBox
using:

``
wget https://cernbox.cern.ch/index.php/s/QUNh8UjTjLBuo8O/download -O EWinoData.tar.gz
``

The tarball contains 3 folders containing
the SLHA files (slha_scanRandom), the SModelS output (smodels_scanRandom) and the Micromegas output (micromegas_scanRandom).


### Scotogenic Scan data ###

#### Scalar DM Scenario ####


#### Fermionic DM Scenario ####
