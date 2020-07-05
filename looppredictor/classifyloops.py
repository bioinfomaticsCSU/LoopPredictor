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

   argv=sys.argv[1:]
   time_start = time.time()
   loops = ''
   featurePath = ''
   genome= ''
   output_path=''
   integer = 1
   
   try:
      opts, args = getopt.getopt(argv,"l:f:g:o:i:",["loops=","featurePath=","genome=","output_path=","integer="])
   except getopt.GetoptError:
      print ('ClassifyLoops.py -l <loops> -f <featurePath> -g <genome> -o <output_path> -i <integer>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('ClassifyLoops.py -l <loops> -f <featurePath> -g <genome> -o <output_path> -i <integer>')
         sys.exit()
      elif opt in ("-l", "--loops"):
          loops = arg
      elif opt in ("-f", "--featurePath"):
          featurePath = arg
      elif opt in ("-g","--genome"):
         genome=arg
      elif opt in ("-o","--output_path"):
         output_path=arg
      elif opt in ("-i","--integer"):
         integer=arg


   print ("----------------------------Your parameters are:----------------------------")
   if loops !='':
      print ("loops: "+loops)
   else:
      print ("Please input the path of loop file!")
      sys.exit()
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
   if output_path!='':
      print ("output_path: " + output_path)
   else:
      print ("Please input output_path!")
      sys.exit()
   if integer!='':
      print ("integer: " + integer)
   else:
      print ("Please input integer(1-5) to filter the output type!")
   

   #output_path = os.path.dirname(output)
   flag=False
   #work_path=os.getcwd()
   #curPath = os.path.abspath(os.path.dirname(__file__))
   work_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
   
   commandline=work_path+"/looppredictor/Bash/ClassifyLoops.sh " +loops+" "+featurePath+" "+output_path+" "+genome+" "+integer
   print ("commandline: "+commandline)
   flag=os.system(commandline)
   if flag==0:
      print ("----------------------------Classification success!--------------------\n")
     
      #TrainingTool.predict(output_path+"/feature_out.txt",trainfile,model,cutoff,output_path)


   else:
      print ("----------------------------Classification failed!---------------------\n")
      sys.exit()


if __name__ == "__main__":
   main()