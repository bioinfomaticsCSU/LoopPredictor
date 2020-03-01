#!/usr/bin/python
import collections
import getopt
import os
import sys
import json
import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
import time
from pathos.multiprocessing import ProcessPool
from scipy.stats import poisson
from looppredictor import trainingtool

#main function
#-----------------------------------------------------------------------------------------------------------------------
def main(argv):
   time_start = time.time()
   filter_me1 = ''
   filter_me3 = ''
   filter_ac= ''
   infile_loop=''
   infile_anchor = ''
   filter_hmm= ''
   genome=''
   try:
      opts, args = getopt.getopt(argv,"b:f:o:g:t:m:c:",["bedfile=","featurePath=","outPath=","genome=","trainfile=","model=","cutoff="])
   except getopt.GetoptError:
      print ('LoopPredictor.py -b <bedfile> -f <featurePath> -g <genome> -o <output_name> -t <trainfile> -m <model> -c <cutoff>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('LoopPredictor.py -b <bedfile> -f <featurePath>  -g <genome> -o <output_path> -t <trainfile> -m <model> -c <cutoff>')
         sys.exit()
      elif opt in ("-b", "--bedfile"):
          bedfile = arg
      elif opt in ("-f", "--featurePath"):
          featurePath = arg
      elif opt in ("-g","--genome"):
         genome=arg
      elif opt in ("-o","--output_path"):
         output_path=arg
      elif opt in ("-t","--trainfile"):
         trainfile=arg
      elif opt in ("-m","--model"):
         model=arg
      elif opt in ("-c","--cutoff"):
         cutoff=arg

   print ("----------------------------Your parameters are:----------------------------")
   if bedfile !='':
      print ("bedfile: "+bedfile)
   else:
      print ("No bedfile, running de novo detecting mode!")
   if featurePath!='':
      print ("featurePath: "+featurePath)
   else:
      print ("Please input the path of feature fold!")
   if genome!='':
      print ("genome: " + genome)
   else:
      print ("Please input genome!")
   if output_path!='':
      print ("output_path: " + output_path)
   else:
      print ("Please input output_path!")
   if trainfile!='':
      print ("trainfile: " + trainfile)
   else:
      print ("Please input the .fix file of trained model!")
   if model!='':
      print ("model: " + model)
   else:
      print ("Please input a trained model!")
   if cutoff!='':
      print ("cutoff: " + cutoff)
   else:
      print ("Please input a cutoff value to filter loops integer:[0-1000]!")
   

   #output_path = os.path.dirname(output)
   flag=False
   #work_path=os.getcwd()
   work_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
   if(bedfile!=''):
      commandline=work_path+"/looppredictor/Bash/FeatureGenerator.sh " +bedfile+" "+featurePath+" "+output_path+" "+genome+" "+model
   else:
      commandline=work_path+"/looppredictor/Bash/FeatureGenerator_nobed.sh " +featurePath+" "+output_path+" "+genome+" "+model
   print ("commandline: "+commandline)
   flag=os.system(commandline)
   
   if flag==0:
      print ("----------------------------FeatureGenerator success!--------------------\n")
      trainingtool.predict(output_path+"/feature_out.txt",trainfile,model,cutoff,output_path)

   else:
      print ("----------------------------FeatureGenerator failed!---------------------\n")
      sys.exit()



if __name__ == "__main__":
   main(sys.argv[1:])