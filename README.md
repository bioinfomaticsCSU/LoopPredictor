<img src="/doc/lp_logo_horiz.png" width="35%">
Predicting unrecognized enhancer-mediated genome topology by an ensemble machine learning model

## Contents
- [What can LoopPredictor do?](#What-can-LoopPredictor-do?)
- [Installation](#Installation)\
 [1. Create conda environment](#1.Create-conda-environment)\
 [2. Install LoopPredictor](#2.Install-LoopPredictor)
- [Example usage](#Example-usage)\
 [1. Classifying loops for known chromatin interaction](#1.Classifying-loops-for-known-chromatin-interaction)\
 [2. Predicting loops for unknown cell types](#2.Predicting-loops-for-unknown-cell-types)\
 [3. Customize model for extensive research](#3.Customize-model-for-extensive-research)

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
conda create -n LoopPredictor-env python=3.6 pandas numpy scikit-learn=0.20.3 pathos
# activate
conda activate LoopPredictor-env
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
### 1. Classifying loops for known chromatin interaction
The testing data were available in /example/K562_classification_example. The structure of folder was shown as below, two kinds of necessary files need to be prepared as input, and the classification results will be *_Output.txt.
```bash
 example /
   K562_classification_example /
     featureData /                 # [necessary input]features of corresonding cell line input for the classification
     tmp /                         # [intermediate]temporary files generated within running
     log /                         # [intermediate]log files generated within running
     *.bedpe                       # [necessary input]loops file with .bedpe format
     *_Output.txt                  # [output]results of loops classification
```
#### *Step1: Prepare featureData files*
The classification was taken by the integration of active/inactive histone mark, so the corresonding ChIP-seq peaks of H3K27ac, H3K4me1, and H3K4me3 were the basic requirement. The peak files should be the standard ENCODE [narrowPeak/broadPeak](http://genome.ucsc.edu/FAQ/FAQformat#format13) file without head line, shown as below, which were listed in the folder /example/K562_classification_exampleas/featureData.
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
#### *Step2: Prepare loops file*
The loops file should be .bedpe format with at least 6 columns, columns were seperated by tab. The minimum columns should include the chrom name, start, end of each anchor, shown as below.
```bash
chr22	38290514	38294289	chr22	38680609	38682339
chr5	96033605	96042289	chr5	96259190	96260539
chr1	23665194	23673403	chr1	24097536	24108995
chr3	176676833	176679516	chr3	176741264	176748850
chr11	63604132	63609924	chr11	63751693	63756217
chr17	37005563	37012402	chr17	38801324	38806978
chr3	138311141	138315068	chr3	138482903	138484460
chr11	126078482	126084019	chr11	126210767	126227804
```
#### *Step3: Running classification*
The parameters of the script are as following,
```bash
classifyloops -l <loops> -f <featurePath> -g <genome> -o <output_name> -i <integer>
-l [string] loop file with ./bedpe format to be classified.
-f [string] absolute path of the featureData folder.
-g [string] genome of loops.
-o [string] path to save the output result. 
-i [integer(1-5)] 1. Output all types of loops without filtering;
                  2. Output only "e-p"/"p-e" type loops;
                  3. Output only "e-e" type loops;
                  4. Output only "p-p" type loops;
                  5. Output only "inactivate-*"/"*-inativate" type loops;
```
Here is a running example:
```bash
classifyloops -l /path/to/example/K562_classification_example/K562_classifyLoop_example.bedpe \
                   -f /path/to/example/K562_classification_example/featureData \
                   -o /path/to/example/K562_classification_example -g hg19 -i 1
```

### 2. Predicting loops for unknown cell types
The testing data were available in /example/NIH3T3_prediction_example. The structure of folder was shown as below, the featureData is the necessary input for the prediction, and if you want to investigate the topology structures of a set of specific genes, a bed file containing the regions of genes could be provided. If there is no bed file inputing, the prediction will be performed for the whole genome in de novo, which will take some time.
```bash
 example /
   NIH3T3_prediction_example /
     featureData /                          # [necessary input]features of corresonding cell line input for the prediction
     tmp3 /                                 # [intermediate]temporary files generated within running
     log /                                  # [intermediate]log files generated within running
     *.bed                                  # [optional input]input bed file of interested regions for loops prediction
     feature_out.txt                        # [intermediate]features are extracted from files within running
     *predicted_result.bedpe                # [output]predicted results of loops
```

#### *Step1: Choose the proper pre-trained model*
We provided three typical pre-trained model for the prediction, which could be found in folder /trained_model/. The model should be chosen to match the features you can get access to.

pre-trained model | multi-omics features requirement
 ---- | ----- 
 Minimum model | -ATAC-seq, -ChIP-seq/CUT&RUN(H3K27ac,H3K4me3)
 Median model  | -ATAC-seq, -ChIP-seq/CUT&RUN(H3K27ac,H3K4me3,H3K4me1,H3K9ac,H3K9me3,CTCF), -RNA-seq
 Maximum model | -ATAC-seq, -ChIP-seq/CUT&RUN(H3K27ac,H3K4me3,H3k4me2,H3K4me1,H3K9ac,H3K9me3,H3K36me3,H3K79me2,CTCF,ELF1,JUND,MAX,YY1), -RNA-seq, -Methylation

#### *Step2: Prepare the input features*
The multi-omics features data should be put into folder featureData/.
For ATAC-seq and ChIP-seq/CUT&RUN data, the format should be standard [narrowPeak/broadPeak](http://genome.ucsc.edu/FAQ/FAQformat#format13), as shown above.
For RNA-seq data, we recommend to use [Homer](http://homer.ucsd.edu/homer/) to build 
tag files for the alignment, and then "findPeaks" function is utilized to detect the highly enriched regions, the output from "findPeaks" can be used as the feature file of RNA-seq data after removing the head line.
For Methylation data, we recommend to download the .bedRrbs format of RRBS data from [ENCODE](https://www.encodeproject.org/), 
which is shown as below,
```bash
chr1	1000170	1000171	K562_Rep3_RRBS	46	+	1000170	1000171	155,255,0	46	35
chr1	1000190	1000191	K562_Rep3_RRBS	46	+	1000190	1000191	105,255,0	46	15
chr1	1000191	1000192	K562_Rep3_RRBS	53	-	1000191	1000192	55,255,0	53	9
chr1	1000198	1000199	K562_Rep3_RRBS	46	+	1000198	1000199	105,255,0	46	20
chr1	1000199	1000200	K562_Rep3_RRBS	53	-	1000199	1000200	105,255,0	53	15
chr1	1000206	1000207	K562_Rep3_RRBS	53	-	1000206	1000207	155,255,0	53	26
```
#### *Step3: Prepare the interested gene file (optional)*
If you want to detect the enhancer-mediated interactions for a set of interested gene, we recommend to extract the name of genes to the coordinates on the chromatin by [UCSC Table Browser](https://genome.ucsc.edu/cgi-bin/hgTables?hgsid=804701707_AsIp981xpMMb6T4p83FooaNvjQup). The coordinates should be ./bed format with at least 3 columns(chrom,start,end).

#### *Step4: Running prediction*
After preparing the input files, you can run the script "LoopPredictor.py" to perform the prediction.
The parameters of the script are as following,
```bash
looppredictor -b <bedfile> -f <featurePath> -g <genome> -t <trainfile> -m <model> -c <cutoff> -o <output_name>
-b [string] coordinate .bed file of a set of interested genes.
-f [string] absolute path of the featureData folder.
-g [string] genome of the features data.
-t [string] .fix file for the pre-trained model.
-m [string] the pre-trained model chosen to use.
-c [integer(>0)] the cutoff of loop score to filter the predicted output loops. 
-o [string] path to save the output result.
```
Here is a running example:
```bash
looppredictor -b /path/to/example/NIH3T3_prediction_example/NIH_geneEnh_example.bed \
                   -f /path/to/example/NIH3T3_prediction_example/featureData \
                   -g mm10 \
                   -t /path/to/trained_model/features_median_forTraining.fix \
                   -m /path/to/trained_model/GBRT_trained_model_median.m \
                   -c 1 \
                   -o /path/to/example/NIH3T3_prediction_example
```
### 3. Customize model for extensive research
- *Step1: prepare trianing data*\
The training data contains target and multi-omics data, target file shoule be the chromatin interactions in ./bedpe format, which is the prior knowledge to train the model. The target file should be 8 columns without head line, the final column must be the score of interaction, which is important for the prediction, shown as below,
```bash
chr17 75115676 75125670 chr17 76731709 76734226 loop_name_1 1
chr12 56649935 56654417 chr12 56860478 56865446 loop_name_2 17
chr18 53026973 53030447 chr18 54302527 54308273 loop_name_3 2
chr10 15644687 15646877 chr10 15825760 15862181 loop_name_4 7
chr21 35439250 35465483 chr21 36693517 36722679 loop_name_5 3
```
The multi-omics data for the corresponding cell line should be prepared in the featureData/ folder as mentioned [above](#step2-prepare-the-input-features).

- *Step2: Running training workflow*\
After preparing the input training data, you can run the script "Customized_GBRT_trainer.py" to train your own model.
The parameters of the script are as following,
```bash
customized_gbrt_trainer -t <trainfile> -f <feature> -g <genome> -o <output_path> -n <output_name>
-t [string] target file of a set of loops with score to train the model, which is .bedpe format.
-f [string] absolute path of the featureData folder.
-g [string] genome of the features data.
-o [string] path to save the output result.
-n [string] output name of the model.
```
Here is a running example:
```bash
customized_gbrt_trainer -t /path/to/example/HCT116_custom_model_example/HCT116_custom_example.bedpe \
                   -f /path/to/example/HCT116_custom_model_example/featureData \
                   -g hg19 \
                   -o /path/to/example/NIH3T3_prediction_example \
                   -n /path/to/example/NIH3T3_prediction_example/HCT116_custom_model.m
```
