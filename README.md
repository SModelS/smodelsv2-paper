# smodelsv2-paper
A repository to store the code and data for the SModelS v2 physics paper


## Basic Installation ##

The script installer.sh will try to fetch and install the following packages:

  * [smodels](https://smodels.github.io/)
  * [SoftSUSY](https://softsusy.hepforge.org/)  



## Analysing Results and Plotting ##

The SModelS output can be easily combined using Pandas DataFrames and stored
as a pickle file, as shown in [results/getIDMResults.ipynb](results/getIDMResults.ipynb).

For plotting the results using the DataFrame pickle file, see [results/plotIDMResults.ipynb](results/plotIDMResults.ipynb)

## Data ##

Due to GitHub storage limitations the data (SLHA files and SModelS output) should be stored in CERNBox.

### EWino random scan data ###

``
wget https://cernbox.cern.ch/index.php/s/7V4jYOk1Q2XzxY0/download -O slha_scanRandom.tar.gz
``


``
wget https://cernbox.cern.ch/index.php/s/xf0jIxeiNfkbsrN/download -O smodels_scanRandom.tar.gz
``



