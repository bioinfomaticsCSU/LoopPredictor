# LoopPredictor
Predicting unknown enhancer-mediated genome topology by an ensemble machine learning model

## Contents
- [What can LoopPredictor do?](#What-can-LoopPredictor-do?)
- [Installation](#Installation)
- [Example usage](#Example-usage)

## What can LoopPredictor do?
LoopPredictor is an ensemble machine learning model, used to predict enhancer mediated loops in a genome-wide fashion across different cell lines, which is also applicable to different model organisms.
 - Annotate current chromatin interactions and classify the loops into "e-p", "e-e", "p-p" and inactivate types through integrating the enrichment of active/inactive histone mark, distance to Transcription Start Sites(TSS). Which helped users to have a keen insight into topology structure.
- Predict chromatin interactions for the unknown cell types which lack of 3D profile, LoopPredictor was trained by HiChIP and multi-omics datasets from several cell types, users only need to feed the multi-omics features of interested cell type into the adaptive model, 


## Installation
LoopPrediction is built on Python 3 and R 3.6.2. Homer is also needed for the annotation of chromatin regions.  
   - Prerequisites:\
       [Python](https://www.python.org/)(>=3.4.0), [R](https://www.r-project.org/)(>=3.6.2), [Homer](http://homer.ucsd.edu/homer/)
   - Dependencies:\
   python packages:
       [pandas](https://pandas.pydata.org/), [numpy](http://www.numpy.org/), [scikit-learn](https://scikit-learn.org/stable/), [pathos](https://pypi.org/project/pathos/)\
   R packages:
       [stringr](https://stringr.tidyverse.org/), [GenomicRanges](https://bioconductor.org/packages/release/bioc/html/GenomicRanges.html), [TxDb.Hsapiens]
(http://bioconductor.org/packages/release/data/annotation/html/TxDb.Hsapiens.UCSC.hg19.knownGene.html)(dowload the corresponding TxDb package the species you want to predict)

### 1. Create conda environment
We highly recommend to use a virtual environment for the installation of LoopPredictor and its dependencies. A virtual environment can be created and (de)activated as follows by using [conda](https://conda.io/docs/):
```bash
# create
conda create -n deepsignalenv python=3.6
# activate
conda activate deepsignalenv
# deactivate
conda deactivate
```
The virtual environment can also be created by using [*virtualenv*](https://github.com/pypa/virtualenv/).

### 2. Install deepsignal
- After creating and activating the environment, download and install deepsignal (**lastest version**) from github:
```bash
git clone https://github.com/bioinfomaticsCSU/deepsignal.git
cd deepsignal
python setup.py install
```
or install deepsignal using *pip*:
```bash
pip install deepsignal
```

- [tombo](https://github.com/nanoporetech/tombo) is required to be installed in the same environment:
```bash
# install using conda
conda install -c bioconda ont-tombo
# or install using pip
pip install ont-tombo[full]
``` 

- install [tensorflow](https://www.tensorflow.org/)  (version: 1.8.0<=tensorflow<=1.13.1) in the same environment:

```bash
# install using conda
conda install -c anaconda tensorflow==1.13.1
# or install using pip
pip install 'tensorflow==1.13.1'
```
If a GPU-machine is used, install the gpu version of tensorflow. The cpu version is not required:
```bash
# install using conda
conda install -c anaconda tensorflow-gpu==1.13.1
# or install using pip
pip install 'tensorflow-gpu==1.13.1'
```

