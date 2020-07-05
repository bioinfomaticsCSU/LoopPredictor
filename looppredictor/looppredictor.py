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
def main():
   time_start = time.time()
   bedfile = ''
   featurePath = ''
   genome= ''
   output_path='./'
   trainfile = ''
   model= ''
   cutoff=''
   minsize="10000"
   maxsize="5000000"
   argv=sys.argv[1:]
   try:
      opts, args = getopt.getopt(argv,"b:f:o:g:t:m:c:s1:s2",["bedfile=","featurePath=","outPath=","genome=","trainfile=","model=","cutoff=","minsize=","maxsize="])
   except getopt.GetoptError:
      print ('LoopPredictor.py -b <bedfile> -f <featurePath> -g <genome> -o <output_path> -t <trainfile> -m <model> -c <cutoff> -s1 <minsize> -s2 <maxsize>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('LoopPredictor.py -b <bedfile> -f <featurePath>  -g <genome> -o <output_path> -t <trainfile> -m <model> -c <cutoff> -s1 <minsize> -s2 <maxsize>')
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
      elif opt in ("-s1","--minsize"):
         minsize=arg
      elif opt in ("-s2","--maxsize"):
         maxsize=arg

   print ("----------------------------Your parameters are:----------------------------")
   if bedfile !='':
      print ("bedfile: "+bedfile)
   else:
      print ("No bedfile, running de novo detecting mode!")
   if featurePath!='':
      print ("featurePath: "+featurePath)
   else:
      print ("Please input the path of feature fold!")
      sys.exit()
   if genome!='':
      print ("genome: " + genome)
   else:
      print ("Please input genome!")
      sys.exit()
   if trainfile!='':
      print ("trainfile: " + trainfile)
   else:
      print ("Please input the .fix file of trained model!")
      sys.exit()
   if model!='':
      print ("model: " + model)
   else:
      print ("Please input a trained model!")
      sys.exit()
   if cutoff!='':
      print ("cutoff: " + cutoff)
   else:
      print ("Please input a cutoff value to filter loops integer:[0-1000]!")

   if output_path!='':
      print ("output_path: " + output_path)
   if minsize!='':
      print ("minimum size of loops: " + minsize)
   if maxsize!='':
      print ("maximum size of loops: " + maxsize)
   

   #output_path = os.path.dirname(output)
   flag=False
   #work_path=os.getcwd()
   work_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
   if(bedfile!=''):
      commandline=work_path+"/looppredictor/Bash/FeatureGenerator.sh " +bedfile+" "+featurePath+" "+output_path+" "+genome+" "+model
   else:
      commandline=work_path+"/looppredictor/Bash/FeatureGenerator_nobed.sh " +featurePath+" "+output_path+" "+genome+" "+model+" "+minsize+" "+maxsize
   print ("commandline: "+commandline)
   flag=os.system(commandline)
   
   if flag==0:
      print ("----------------------------FeatureGenerator success!--------------------\n")
      trainingtool.predict(output_path+"/feature_out.txt",trainfile,model,cutoff,output_path)

   else:
      print ("----------------------------FeatureGenerator failed!---------------------\n")
      sys.exit()



if __name__ == "__main__":
   main()