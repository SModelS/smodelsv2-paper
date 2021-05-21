# Results for the 2021 Re-interpretation workshop

## Analysing Results and Plotting ##

The SModelS output can be easily combined using Pandas DataFrames and stored
as a pickle file, as shown in [results/IDMResults.ipynb](results/IDMResults.ipynb).

For plotting the results using the DataFrame pickle file, see [results/plotIDMResults.ipynb](results/plotIDMResults.ipynb)

## Data ##

The data tarball (SLHA files and SModelS output) is stored at CERNBox and can be fetched through [this link](https://cernbox.cern.ch/index.php/s/nLBoOZzXGz6UvCu/) or running:

``
wget https://cernbox.cern.ch/index.php/s/QcdSerL470HIyLS/download -O data.tar.gz
``



## Adding SModelS ##

The SModelS version used for the results is 2.0.0-beta. It can be added to the repository running:

``
git subtree add --prefix=smodels-database --squash git@github.com:SModelS/smodels-database.git v2.0.0-beta
git subtree add --prefix=smodels --squash git@github.com:SModelS/smodels.git v2.0.0-beta
``
