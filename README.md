# LoopPredictor
Predicting unknown enhancer-mediated genome topology by an ensemble machine learning model

## Contents
- [What can LoopPredictor do?](#What-can-LoopPredictor-do?)
- [Installation](#Installation)
- [Example usage](#Example-usage)

## What can LoopPredictor do?
LoopPredictor is an ensemble machine learning model, used to predict enhancer mediated loops in a genome-wide fashion across different cell lines, which is also applicable to different model organisms.
 - Annotate current chromatin interactions and classify the loops into "e-p", "e-e", "p-p" and inactivate types through integrating the enrichment of active/inactive histone mark and distance to Transcription Start Sites(TSS), Which helped users to have a keen insight into topology structure of known cell type.
- Predict chromatin interactions for the unknown cell types which lack of 3D profile, LoopPredictor was trained by HiChIP and multi-omics datasets from three cell types (K562, GM12878, HCT116), users only need to feed the multi-omics features of interested cell type into the pre-trained adaptive model, the sensitive predictions helped users to have a preliminary investigation of unknown chromatin interaction.
- Construct customized models for an extensive prediction research. As 3D chromatin detecting technologies are developing at a high speed, LoopPredictor provided an open workframe for users to construct their own model, the features and targets could be organized as user-defined, and the self-adaptive parameters wil be chosen to tarin the model. After training, users can use the customized model to predict the topology structure of interest.


## Installation
LoopPrediction is built on Python 3 and R 3.6.2. Homer is also needed for the annotation of chromatin regions.  
   - Prerequisites:\
       [Python](https://www.python.org/)(>=3.4.0), [R](https://www.r-project.org/)(>=3.6.2), [Homer](http://homer.ucsd.edu/homer/)
   - Dependencies:\
   **python packages:**
       [pandas](https://pandas.pydata.org/), [numpy](http://www.numpy.org/), [scikit-learn](https://scikit-learn.org/stable/), [pathos](https://pypi.org/project/pathos/)\
   **R packages:**
       [stringr](https://stringr.tidyverse.org/), [GenomicRanges](https://bioconductor.org/packages/release/bioc/html/GenomicRanges.html), [TxDb.Hsapiens](http://bioconductor.org/packages/release/data/annotation/html/TxDb.Hsapiens.UCSC.hg19.knownGene.html) (download the corresponding TxDb package for the species you want to predict)

### 1. Create conda environment
The virtual environment of conda was recommended for the installation of LoopPredictor and its dependencies. A virtual environment can be created and (de)activated as follows by using [conda](https://conda.io/docs/):
```bash
# create
conda create -n LoopPredictorenv python=3.6
# activate
conda activate LoopPredictorenv
# deactivate
conda deactivate
```
The virtual environment can also be created by using [*virtualenv*](https://github.com/pypa/virtualenv/).

### 2. Install LoopPredictor
- After creating and activating the environment, download and install LoopPredictor (**lastest version**) from github:
```bash
git clone https://github.com/bioinfomaticsCSU/LoopPredictor.git
cd LoopPredictor
python setup.py install
```
or install LoopPredictor using *pip*:
```bash
pip install looppredictor
```
## Example usage
### 1. Classifying loops
The tesing data were available in /example/K562_classification_example. The classification was taken by the integration of active/inactive histone mark, so the ChIP-seq peaks of H3K27ac, H3K4me1, and H3K4me3 were the basic requirement. The peak files should be the standard ENCODE [narrowPeak/broadPeak](http://genome.ucsc.edu/FAQ/FAQformat#format13) file without head line, as shown below,
```bash
chr22	16843445	16868802	.	322	.	2.120582	13.1	-1
chr22	17024793	17024896	.	985	.	11.483429	2.8	-1
chr22	17038424	17038594	.	854	.	9.633610	5.0	-1
chr22	17050044	17050593	.	465	.	4.143174	2.0	-1
chr22	17050418	17050537	.	984	.	11.468583	4.2	-1
chr22	17066392	17067403	.	892	.	10.169340	14.8	-1
chr22	17067959	17068242	.	878	.	9.966456	13.3	-1
chr22	17068652	17068827	.	835	.	9.358364	4.9	-1
```
You could run the scripts as following,
```bash
cd LoopPredictor/bin
./ClassifyLoops.sh /path/to/example/K562_classification_example/
```

### 2. Predicting loops
### 3. Customize model
