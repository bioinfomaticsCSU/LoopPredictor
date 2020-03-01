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

#process the format of input file and set index
#-----------------------------------------------------------------------------------------------------------------------
def pre_file(filter_me1,filter_me3,filter_ac):
   filter_me1_dataframe = pd.read_csv(filter_me1, sep="\t", header=None)
   filter_me1_dataframe.drop(columns=[3,4,5,7,8], inplace=True)
   filter_me3_dataframe = pd.read_csv(filter_me3, sep="\t", header=None)
   filter_me3_dataframe.drop(columns=[3, 4, 5, 7, 8], inplace=True)
   filter_ac_dataframe = pd.read_csv(filter_ac, sep="\t", header=None)
   filter_ac_dataframe.drop(columns=[3, 4, 5, 7, 8], inplace=True)

   filter_me1_dataframe['index_bin'] = 0
   filter_me1_dataframe['index_bin'] = filter_me1_dataframe.apply(lambda x: (int(x[1])//1000)*1000, axis=1)
   filter_me3_dataframe['index_bin'] = 0
   filter_me3_dataframe['index_bin'] = filter_me3_dataframe.apply(lambda x: (int(x[1]) // 1000) * 1000, axis=1)
   filter_ac_dataframe['index_bin'] = 0
   filter_ac_dataframe['index_bin'] = filter_ac_dataframe.apply(lambda x: (int(x[1]) // 1000) * 1000, axis=1)

   filter_me1_dataframe=filter_me1_dataframe.set_index(keys=[0,'index_bin'],append=False,drop=True)
   filter_me3_dataframe=filter_me3_dataframe.set_index(keys=[0,'index_bin'],append=False,drop=True)
   filter_ac_dataframe = filter_ac_dataframe.set_index(keys=[0, 'index_bin'], append=False, drop=True)
   filter_me1_dataframe.columns = ['start_me1','end_me1','score_me1']
   filter_me3_dataframe.columns=['start_me3','end_me3','score_me3']
   filter_ac_dataframe.columns = ['start_ac', 'end_ac', 'score_ac']

   filter_me_merge_tmp=pd.merge(filter_me1_dataframe,filter_me3_dataframe, left_index=True, right_index=True, how='outer')
   filter_me_merge=pd.merge(filter_me_merge_tmp,filter_ac_dataframe, left_index=True, right_index=True, how='outer')

   return filter_me_merge

def peak_filter_poi(infile):
   # obtain the column of counts
   input_dataframe = pd.read_csv(infile, sep=" ", header=None)
   input_colnum = input_dataframe.shape[1]
   input_rownum = input_dataframe.shape[0]

   if (input_colnum == 1):
      input_dataframe = pd.read_csv(infile, sep=" ", header=None)
   input_count = input_dataframe[7]
   # calculate lam for poission model
   input_count_narray = input_count.mean()
   x = poisson.ppf(0.2, input_count_narray)
   # calculate the count for each num, and sort the num
   input_count_col = collections.Counter(input_count)
   # filter the input dataset according to the counts
   input_dataframe_filt = input_dataframe[input_dataframe[7] > x]
   input_dataframe_filt_rowNum = input_dataframe_filt.shape[0]
   input_dataframe_filt.index = list(range(input_dataframe_filt_rowNum))
   return input_dataframe_filt
   #return input_dataframe

def pre_file_hmm(filter_hmm):
   filter_hmm_dataframe=pd.read_csv(filter_hmm, sep="\t", header=None)
   filter_hmm_dataframe.drop(columns=[4, 5, 6, 7, 8], inplace=True)
   filter_hmm_dataframe['index_bin'] = 0
   filter_hmm_dataframe['index_bin'] = filter_hmm_dataframe.apply(lambda x: (int(x[1]) // 1000) * 1000, axis=1)
   filter_hmm_dataframe = filter_hmm_dataframe.set_index(keys=[0, 'index_bin'], append=False, drop=True)
   filter_hmm_dataframe.columns = ['start_hmm', 'end_hmm', 'anno_hmm']
   return filter_hmm_dataframe

def pre_file_four(filter_me1,filter_me3,filter_ac,filter_hmm):
   filter_me1_dataframe = pd.read_csv(filter_me1, sep="\t", header=None)
   filter_me1_dataframe.drop(columns=[3, 4, 5, 7, 8], inplace=True)
   filter_me3_dataframe = pd.read_csv(filter_me3, sep="\t", header=None)
   filter_me3_dataframe.drop(columns=[3, 4, 5, 7, 8], inplace=True)
   filter_ac_dataframe=pd.read_csv(filter_ac, sep="\t", header=None)
   filter_ac_dataframe.drop(columns=[3, 4, 5, 7, 8], inplace=True)
   filter_hmm_dataframe=pd.read_csv(filter_hmm, sep="\t", header=None)
   filter_hmm_dataframe.drop(columns=[ 4, 5, 6, 7,8], inplace=True)

   filter_me1_dataframe['index_bin'] = 0
   filter_me1_dataframe['index_bin'] = filter_me1_dataframe.apply(lambda x: (int(x[1]) // 1000) * 1000, axis=1)
   filter_me3_dataframe['index_bin'] = 0
   filter_me3_dataframe['index_bin'] = filter_me3_dataframe.apply(lambda x: (int(x[1]) // 1000) * 1000, axis=1)
   filter_ac_dataframe['index_bin'] = 0
   filter_ac_dataframe['index_bin'] = filter_ac_dataframe.apply(lambda x: (int(x[1]) // 1000) * 1000, axis=1)
   filter_hmm_dataframe['index_bin'] = 0
   filter_hmm_dataframe['index_bin'] = filter_hmm_dataframe.apply(lambda x: (int(x[1]) // 1000) * 1000, axis=1)

   filter_me1_dataframe = filter_me1_dataframe.set_index(keys=[0, 'index_bin'], append=False, drop=True)
   filter_me3_dataframe = filter_me3_dataframe.set_index(keys=[0, 'index_bin'], append=False, drop=True)
   filter_ac_dataframe = filter_ac_dataframe.set_index(keys=[0, 'index_bin'], append=False, drop=True)
   filter_hmm_dataframe=filter_hmm_dataframe.set_index(keys=[0, 'index_bin'], append=False, drop=True)
   filter_me1_dataframe.columns = ['start_me1', 'end_me1', 'score_me1']
   filter_me3_dataframe.columns = ['start_me3', 'end_me3', 'score_me3']
   filter_ac_dataframe.columns = ['start_ac', 'end_ac', 'score_ac']
   filter_hmm_dataframe.columns = ['start_hmm', 'end_hmm', 'anno_hmm']

   filter_me_merge_tmp1 = pd.merge(filter_me1_dataframe, filter_me3_dataframe, left_index=True,right_index=True,how='outer')
   filter_me_merge_tmp2=pd.merge(filter_me_merge_tmp1,filter_ac_dataframe, left_index=True, right_index=True,how='outer')
   filter_me_merge = pd.merge(filter_me_merge_tmp2,filter_hmm_dataframe, left_index=True, right_index=True,how='outer')

   return filter_me_merge

def pre_file_input(filter_me):
   filter_me_dataframe = pd.read_csv(filter_me, sep="\t", header=None)
   filter_me_dataframe.drop([0], inplace=True)
   filter_me_dataframe.drop(columns=[0], inplace=True)
   filter_me_dataframe_rowNum = filter_me_dataframe.shape[0]
   filter_me_dataframe.reset_index()
   filter_me_dataframe.index = list(range(filter_me_dataframe_rowNum))
   filter_me_colnum = filter_me_dataframe.shape[1]
   filter_me_dataframe.columns = range(filter_me_colnum)
   filter_me_dataframe.set_index([0], append=True)
   return filter_me_dataframe

#multiprocessing first interface, using map function
#-----------------------------------------------------------------------------------------------------------------------

def anchor_pro_multiprocessing(input_anchor_pro,row,filter_hmm_forPro):
   input_anchor_pro_chromName = input_anchor_pro.ix[[row]].values[0][0]
   input_pro_x1 = int(input_anchor_pro.ix[[row]].values[0][1])
   input_pro_x2 = int(input_anchor_pro.ix[[row]].values[0][2])
   ann_hmm_pro, count_hmm_tmp, count_pro_tmp, count_enh_tmp = peak_extr_anchor_pro(
      input_anchor_pro_chromName,input_pro_x1, input_pro_x2,filter_hmm_forPro)

   #add new column to anchor...
   #input_anchor_pro.loc[row, 'anchor_hmm'] = ann_hmm_pro
   #input_anchor_pro.loc[row, 'anchor_feature'] = "promoter"

   return count_pro_tmp,count_enh_tmp,count_hmm_tmp,ann_hmm_pro

def anchor_other_multiprocessing(input_anchor_other,filter_merge_dataframe,flag,row):
   count_enhancer_I=0.0
   count_promoter_E_temp=0.0
   count_enhancer_E_temp=0.0
   count_hmm_temp=0.0
   anchor_hmm=''
   count_NA_I=0.0
   annot_my=''
   input_anchor_chromName = input_anchor_other.ix[[row]].values[0][0]
   input_x1 = int(input_anchor_other.ix[[row]].values[0][1])
   input_x2 = int(input_anchor_other.ix[[row]].values[0][2])

   #add hmm anotation
   if flag:
      score, annot_hmm, count_hmm_temp, count_enhancer_E_temp, count_promoter_E_temp = peak_extr_anchor(
         input_anchor_chromName, input_x1, input_x2, filter_merge_dataframe, flag)
      #input_anchor_other.loc[row, 'anchor_hmm'] = annot_hmm
      anchor_hmm=annot_hmm
   else:
      score = peak_extr_anchor(input_anchor_chromName, input_x1, input_x2, filter_merge_dataframe, flag)
   # add my anotation according to score
   if score >= 10:
      #input_anchor_other.loc[row, 'anchor_feature'] = 'strong enhancer'
      annot_my='strong enhancer'
      count_enhancer_I =1
      print ("strong enhancer")
   elif score > 0 and score < 10:
      #input_anchor_other.loc[row, 'anchor_feature'] = 'weak enhancer'
      annot_my = 'weak enhancer'
      count_enhancer_I = 1
      print ("weak enhancer")
   else:
      #input_anchor_other.loc[row, 'anchor_feature'] = 'NA'
      annot_my = 'NA'
      count_NA_I = 1
      print ("NA")
   return  count_promoter_E_temp,count_enhancer_E_temp,count_hmm_temp,count_enhancer_I,count_NA_I,anchor_hmm,annot_my

def loop_anchor_etr(input_loop_dataframe,anchor_annot_dataframe,row):
   row_count=input_loop_dataframe.shape[0]
   chromName_left=input_loop_dataframe.ix[[row]].values[0][0]
   x1_left=str(input_loop_dataframe.ix[[row]].values[0][1]+1)
   chromName_right=input_loop_dataframe.ix[[row]].values[0][3]
   x1_right=str(input_loop_dataframe.ix[[row]].values[0][4]+1)

   anchor_annot_dataframe = anchor_annot_dataframe.set_index(keys=[0, 1], append=False, drop=True)
   anchor_annot_dataframe=anchor_annot_dataframe.sort_index()
   anchor_extrChrom_left = anchor_annot_dataframe.loc[chromName_left].loc[x1_left]
   anchor1_annotation=anchor_extrChrom_left.values[2]
   anchor1_hmm=anchor_extrChrom_left.values[1]


   anchor_extrChrom_right = anchor_annot_dataframe.loc[chromName_right].loc[x1_right]
   anchor2_annotation= anchor_extrChrom_right.values[2]
   anchor2_hmm=anchor_extrChrom_right.values[1]

   loop_type=anchor_extrChrom_left.values[2]+"-"+anchor_extrChrom_right.values[2]
   print (loop_type,row,row_count)
   return anchor1_annotation,anchor1_hmm,anchor2_annotation,anchor2_hmm,loop_type

def loop_index_multipleprocessing(loop_dataframe,loop_index_1,loop_index_2,loop_index_3):
   index_1 = loop_index_1[0]
   index_2 = loop_index_2[0]
   index_3 = loop_index_3[0]

   loop_group = loop_dataframe.loc[index_1].loc[index_2]
   print(loop_group)
   pd_loop=loop_group.groupby("loop_type").size()
   pd_index = list(pd_loop.index)
   pd_list=list(pd_loop)
   loop_group_newdf = index_1 + " " + str(index_2) + " " + str(index_3)
   pd_df=pd.DataFrame({loop_group_newdf:pd_index,'count':pd_list})
   print(pd_df)
   return pd_df

#multiprocessing second interface, using map function
#-----------------------------------------------------------------------------------------------------------------------
def peak_extr_anchor_pro(chromName,input_x1,input_x2,hmm_file):
   colume_num = hmm_file.shape[1]
   h3k4me_index_list = hmm_file.ix[chromName].index.values.tolist()
   h3k4me_file_extrChrom = pd.DataFrame(columns=[colume_num])
   index_bin1 = str(int(input_x1 // 1000 * 1000) - 1000)
   index_bin2 = str(int(input_x2 // 1000 * 1000) + 1000)

   folds = fold_bin(index_bin1, index_bin2) + 1
   for fold in range(folds):
      index_bin = int(int(index_bin1) + fold * 1000)
      if index_bin in h3k4me_index_list:
         h3k4me_file_extrChrom = h3k4me_file_extrChrom.append(hmm_file.loc[chromName].loc[index_bin])
      else:
         continue

   annot_hmm = ''
   count_hmm=0
   count_pro=0
   count_enh=0
   h3k4me_file_rowNum = h3k4me_file_extrChrom.shape[0]
   if h3k4me_file_rowNum!=0:
      h3k4me_file_extrChrom.reset_index()
      h3k4me_file_extrChrom.index = list(range(h3k4me_file_rowNum))
      order =[3,"start_hmm","end_hmm","anno_hmm"]
      h3k4me_file_extrChrom = h3k4me_file_extrChrom[order]
      h3k4me_file_rowNum = h3k4me_file_extrChrom.shape[0]

      list_extrChrom=[h3k4me_file_extrChrom for row in range(h3k4me_file_rowNum)]
      list_row=[row for row in range(h3k4me_file_rowNum)]
      list_input_x1=[input_x1 for row in range(h3k4me_file_rowNum)]
      list_input_x2=[input_x2 for row in range(h3k4me_file_rowNum)]
      extr_out_list=list(map(map_peak_extr_pro,list_extrChrom,list_row,list_input_x1,list_input_x2))
      extr_out_dataframe=DataFrame(extr_out_list)
      extr_dataframe =extr_out_dataframe[[0,1,2]].apply(lambda x: x.sum())
      count_hmm = extr_dataframe[0]
      count_enh=extr_dataframe[1]
      count_pro=extr_dataframe[2]
      annot_list=extr_out_dataframe[3].values.tolist()
      annot_list=list(filter(None, annot_list))
      annot_hmm= ";".join(annot_list)
      #annot_tmp=annot_tmp_dataframe[0]

   return annot_hmm,count_hmm,count_pro,count_enh

def peak_extr_anchor(chromName,input_x1,input_x2,h3k4me_file,flag):
   colume_num=h3k4me_file.shape[1]
   h3k4me_index_list=h3k4me_file.ix[chromName].index.values.tolist()
   h3k4me_file_extrChrom = pd.DataFrame(columns=[colume_num])
   index_bin1=str(int(input_x1//1000*1000)-1000)
   index_bin2=str(int(input_x2//1000*1000)+1000)

   folds=fold_bin(index_bin1,index_bin2)+1
   for fold in range(folds):
      index_bin=int(int(index_bin1)+fold*1000)
      if index_bin in h3k4me_index_list:
         h3k4me_file_extrChrom=h3k4me_file_extrChrom.append(h3k4me_file.loc[chromName].loc[index_bin])
      else:
         continue

   h3k4me_file_rowNum = h3k4me_file_extrChrom.shape[0]

   score=0
   count_enhancer_E=0
   count_promoter_E=0
   annot_hmm=""
   count_hmm=0
   count_enh=0
   count_pro=0
   if h3k4me_file_rowNum!=0:
      h3k4me_file_extrChrom.reset_index()
      h3k4me_file_extrChrom.index = list(range(h3k4me_file_rowNum))
      if flag:
         order = [12, "start_me1", "end_me1", "score_me1", "start_me3", "end_me3", "score_me3","start_ac",
                  "end_ac","score_ac","start_hmm","end_hmm","anno_hmm"]
      else:
         order = [9,"start_me1","end_me1","score_me1","start_me3","end_me3","score_me3","start_ac","end_ac","score_ac"]
      h3k4me_file_extrChrom=h3k4me_file_extrChrom[order]

      list_extrChrom = [h3k4me_file_extrChrom for row in range(h3k4me_file_rowNum)]
      list_row = list(range(h3k4me_file_rowNum))
      list_input_x1 = [input_x1 for row in range(h3k4me_file_rowNum)]
      list_input_x2 = [input_x2 for row in range(h3k4me_file_rowNum)]
      list_flag=[flag for row in range(h3k4me_file_rowNum)]
      extr_out_list = list(map(map_peak_extr_other, list_extrChrom, list_row, list_input_x1, list_input_x2,list_flag))
      extr_out_dataframe = DataFrame(extr_out_list)
      extr_dataframe = extr_out_dataframe[[0, 1, 2,3]].apply(lambda x: x.sum())
      score=extr_dataframe[0]
      count_hmm = extr_dataframe[1]
      count_enhancer_E = extr_dataframe[2]
      count_promoter_E = extr_dataframe[3]
      annot_list = extr_out_dataframe[4].values.tolist()
      annot_list = list(filter(None, annot_list))
      annot_hmm = ";".join(annot_list)

   if flag:
      return score,annot_hmm,count_hmm,count_enhancer_E,count_promoter_E
   else:
      return score

#multiprocessing third interface, using map function
#-----------------------------------------------------------------------------------------------------------------------
def map_peak_extr_pro(h3k4me_file_extrChrom,row,input_x1,input_x2):
   count_hmm=0
   count_enh=0
   count_pro=0
   annot_tmp=''
   hmm_x1 = h3k4me_file_extrChrom.ix[[row]].values[0][1]
   hmm_x2 = h3k4me_file_extrChrom.ix[[row]].values[0][2]
   if peak_within(input_x1, input_x2, hmm_x1, hmm_x2):
      if "Enhancer" in h3k4me_file_extrChrom.ix[[row]].values[0][3] or "Promoter" in h3k4me_file_extrChrom.ix[[row]].values[0][3]:
         annot_tmp = h3k4me_file_extrChrom.ix[[row]].values[0][3]
         count_hmm =  1
         if "Enhancer" in annot_tmp:
            count_enh =  1
         if 'Promoter' in annot_tmp:
            count_pro =  1

   return count_hmm,count_enh,count_pro,annot_tmp

def map_peak_extr_other(h3k4me_file_extrChrom,row,input_x1,input_x2,flag):
   h3k4me1_file_x1 = h3k4me_file_extrChrom.ix[[row]].values[0][1]
   h3k4me1_file_x2 = h3k4me_file_extrChrom.ix[[row]].values[0][2]
   h3k4me3_file_x1 = h3k4me_file_extrChrom.ix[[row]].values[0][4]
   h3k4me3_file_x2 = h3k4me_file_extrChrom.ix[[row]].values[0][5]
   h3k27ac_file_x1 = h3k4me_file_extrChrom.ix[[row]].values[0][7]
   h3k27ac_file_x2 = h3k4me_file_extrChrom.ix[[row]].values[0][8]

   me1_ex = peak_within(input_x1, input_x2, h3k4me1_file_x1, h3k4me1_file_x2)
   me3_ex = peak_within(input_x1, input_x2, h3k4me3_file_x1, h3k4me3_file_x2)
   score_me1_tmp = h3k4me_file_extrChrom.ix[[row]].values[0][3]
   score_me3_tmp = h3k4me_file_extrChrom.ix[[row]].values[0][6]

   score=0
   count_hmm=0
   count_enhancer_E=0
   count_promoter_E=0
   annot_temp=''

   if peak_within(input_x1, input_x2, h3k27ac_file_x1, h3k27ac_file_x2):
      if me1_ex and not (me3_ex):
         score = 10
      elif me3_ex and not (me1_ex):
         score =  1
      elif me1_ex and me3_ex:
         if score_me1_tmp > 1.2 * score_me3_tmp:
            score = 2
         else:
            score = 1
      else:
         score = 2

   if flag:
      hmm_x1 = h3k4me_file_extrChrom.ix[[row]].values[0][10]
      hmm_x2 = h3k4me_file_extrChrom.ix[[row]].values[0][11]
      if peak_within(input_x1, input_x2, hmm_x1, hmm_x2):
         if "Enhancer" in h3k4me_file_extrChrom.ix[[row]].values[0][12] or "Promoter" in h3k4me_file_extrChrom.ix[[row]].values[0][12]:
            annot_temp = h3k4me_file_extrChrom.ix[[row]].values[0][12]
            count_hmm = 1
            if "Enhancer" in annot_temp:
               count_enhancer_E = 1
            if "Promoter" in annot_temp:
               count_promoter_E = 1
   return score,count_hmm,count_enhancer_E,count_promoter_E,annot_temp

#Facilitate function
#-----------------------------------------------------------------------------------------------------------------------
def peak_within(ref_axis_left,ref_axis_right,target_axis_left,target_axis_right):
   left_flag=False
   right_flag=False
   if target_axis_left >= (ref_axis_left-1000) and target_axis_left < ref_axis_right:
      left_flag=True
   if target_axis_right <= (ref_axis_right+1000) and target_axis_right >ref_axis_left:
      right_flag=True

   if left_flag and right_flag:
      return True
   else:
      return False

def append_str(x,y):
   sum=x[0]+";"+y[0]+";"
   return sum

def fold_bin(index_bin1,index_bin2):
   fold=(int(index_bin2)-int(index_bin1))//1000
   return fold

def all_np(arr):
    arr = np.array(arr)
    key = np.unique(arr)
    result = {}
    for k in key:
        mask = (arr == k)
        arr_new = arr[mask]
        v = arr_new.size
        result[k] = v
    return result

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
      opts, args = getopt.getopt(argv,"a:b:c:d:i:l:g:o:",["filter1=","filter2=","filter3=","chromhmm=","infile=","anchor=","genome=","output="])
   except getopt.GetoptError:
      print ('H3K27ac_filter.py -a <h3k4me1_file> -b <h3k4me3_file> -c <h3k27ac_file> -i <hichip_anchor> -l <hichip_loop> -g <genome> -o <output_name>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('H3K27ac_filter.py -a <h3k4me1_file> -b <h3k4me3_file> -c <h3k27ac_file> -i <hichip_file> -l <hichip_loop> -g <genome> -o <output_name>')
         sys.exit()
      elif opt in ("-a", "--filter1"):
          filter_me1 = arg
      elif opt in ("-b", "--filter2"):
          filter_me3 = arg
      elif opt in ("-c", "--filter3"):
          filter_ac = arg
      elif opt in ("-d","--chromhmm"):
         filter_hmm=arg
      elif opt in ("-i", "--anchor"):
         infile_anchor = arg
      elif opt in ("-l", "--loop"):
         infile_loop=arg
      elif opt in ("-g","--genome"):
         genome=arg
      elif opt in ("-o","--output"):
         output=arg

   print ("Your parameters are:")
   if filter_me1 !='':
      print ("h3k4me1_file:"+filter_me1)
   else:
      print ("Please input the corresponding h3k4me1 ChIP-seq file!")
   if filter_me3!='':
      print ("h3k4me3_file:"+filter_me3)
   else:
      print ("Please input the corresponding h3k4me3 ChIP-seq file!")
   if filter_me3!='':
      print ("h3k27ac_file:" + filter_ac)
   if filter_hmm!='':
      print ("chromhmm:"+filter_hmm)
      if genome!='':
         print ("genome:" + genome)
      else:
         print ("You have input chromhmm file, so you need to input genome(hg19/mm9/mm10...)")
   if infile_anchor!='':
      print ("hichip_anchor:"+infile_anchor)
   else:
      print ("Please input the anchor file!")
   if infile_loop!='':
      print ("hichip_loop:"+infile_loop)
   else:
      print ("Please input the loop file!")
   if output!='':
      print ("output:"+output)
   else:
      print ("Please input the path of results!")

   output_path = os.path.dirname(output)
   flag=False
   commandline="annotatePeaks.pl " + infile_anchor +" "+genome + " > " + output
   print (commandline)
   print ("----------------------------homer running!-------------------------------\n")
   #flag_homer=os.system(commandline)
   flag_homer=0
   if flag_homer==0:
      print ("----------------------------homer success!-----------------------------\n")

      # read h3k4me1/h3kme3/hmm/... data file, and re-set header, set index
      if filter_hmm!='':
         filter_merge_dataframe = pre_file_four(filter_me1, filter_me3,filter_ac,filter_hmm)
         filter_hmm_forPro=pre_file_hmm(filter_hmm)
         flag=True
      else:
         filter_merge_dataframe=pre_file(filter_me1,filter_me3,filter_ac)

      infile_anchor_homer=output
      input_anchor_dataframe = pre_file_input(infile_anchor_homer)
      input_loop_dataframe=peak_filter_poi(infile_loop)

      #get rid of promoter, and extract the other anchors
      input_anchor_dataframe[8] = input_anchor_dataframe[8].astype('int')
      input_anchor_pro=input_anchor_dataframe[abs(input_anchor_dataframe[8])<2000]
      input_anchor_dataframe = input_anchor_dataframe.append(input_anchor_pro)
      input_anchor_dataframe = input_anchor_dataframe.append(input_anchor_pro)
      input_anchor_other = input_anchor_dataframe.drop_duplicates(keep=False)
      input_anchor_other_rowNum = input_anchor_other.shape[0]
      input_anchor_other.reset_index()
      input_anchor_other.index = list(range(input_anchor_other_rowNum))

      print ("Finish annotating promoter!")
      #input_anchor_other['anchor_hmm'] = 'null'
      #input_anchor_other['anchor_feature'] = 'null'

      #annotate the other anchors by integrating three files
      #-----------------------------------------------------------------------------------------------------------------
      count_promoter_I=0.0
      count_enhancer_I=0.0
      count_promoter_E=0.0
      count_enhancer_E=0.0
      count_hmm=0.0
      count_NA_I=0.0

      pool = ProcessPool(4)
      list_anchor_other=[input_anchor_other for row in range(input_anchor_other_rowNum)]
      list_filtermerge=[filter_merge_dataframe for row in range(input_anchor_other_rowNum)]
      list_flag=[flag for row in range(input_anchor_other_rowNum)]
      list_row_other = [row for row in range(input_anchor_other_rowNum)]
      anchor_other_retr=list(pool.map(anchor_other_multiprocessing,list_anchor_other,list_filtermerge,list_flag,list_row_other))
      anchor_other_dataframe = DataFrame(anchor_other_retr)
      extr_dataframe = anchor_other_dataframe[[0,1,2,3,4]].apply(lambda x: x.sum())
      count_promoter_E=extr_dataframe[0]
      count_enhancer_E=extr_dataframe[1]
      count_hmm=extr_dataframe[2]
      count_enhancer_I=extr_dataframe[3]
      count_NA_I=extr_dataframe[4]
      input_anchor_other['anchor_feature']=anchor_other_dataframe[[6]].values
      input_anchor_other['anchor_hmm']=anchor_other_dataframe[[5]].values

      #annotate the extracted pro part by hmm file
      #-----------------------------------------------------------------------------------------------------------------
      count_pro_P=0.0
      count_enh_P=0.0
      input_anchor_pro_rowNum=input_anchor_pro.shape[0]
      count_promoter_I=input_anchor_pro.shape[0]
      input_anchor_pro.index=list(range(input_anchor_pro_rowNum))
      input_anchor_pro['anchor_hmm'] = 'null'
      input_anchor_pro['anchor_feature'] = 'null'

      list_row=[row for row in range(input_anchor_pro_rowNum)]
      list_anchor = [input_anchor_pro for row in range(input_anchor_pro_rowNum)]
      list_filter=[filter_hmm_forPro for row in range(input_anchor_pro_rowNum)]
      anchor_pro_retr=list(pool.map(anchor_pro_multiprocessing,list_anchor,list_row,list_filter))
      anchor_pro_dataframe=DataFrame(anchor_pro_retr)[[0,1,2]].apply(lambda x: x.sum())
      count_pro_P=anchor_pro_dataframe[0]
      count_enh_P=anchor_pro_dataframe[1]
      count_hmm=anchor_pro_dataframe[2]+count_hmm
      input_anchor_pro['anchor_feature']="promoter"
      input_anchor_pro['anchor_hmm']=DataFrame(anchor_pro_retr)[[3]].values

      input_anchor_pro = input_anchor_pro.append(input_anchor_other)
      input_anchor_pro.to_csv(output_path+'/anchor_annotation.csv', index = False, header = False)
      input_anchor_pro.drop(columns=[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17], inplace=True)
      input_anchor_pro.columns=[0,1,2,3,4]

      input_loop_dataframe_rowNum=input_loop_dataframe.shape[0]
      list_loop_dataframe=[input_loop_dataframe for row in range(input_loop_dataframe_rowNum)]
      list_anchor_annot=[input_anchor_pro for row in range(input_loop_dataframe_rowNum)]
      list_row=[row for row in range(input_loop_dataframe_rowNum)]

      loop_anchor_list=list(pool.map(loop_anchor_etr,list_loop_dataframe,list_anchor_annot,list_row))
      loop_anchor_dataframe=DataFrame(loop_anchor_list)
      input_loop_dataframe["anchor1_annotation"]=loop_anchor_dataframe[[0]].values
      input_loop_dataframe["anchor1_hmm"] = loop_anchor_dataframe[[1]].values
      input_loop_dataframe["anchor2_annotation"] = loop_anchor_dataframe[[2]].values
      input_loop_dataframe["anchor2_hmm"] = loop_anchor_dataframe[[3]].values
      input_loop_dataframe["loop_type"] = loop_anchor_dataframe[[4]].values
      input_loop_dataframe.to_csv(output_path+'/loop_annotation.csv', index=False, header=True)

      #generate the report for loop annotation......
      #---------------------------------------------------------------------------------------------------------------------
      list_type=loop_anchor_dataframe[[4]].values

      print(list_type)

      #list_type=map(list,zip(*list_type))
      out=all_np(list_type)
      tmp_file = open(output_path+'/loop_report', "w")
      tmp_file.write("Anchor types:"+"\r\n")
      tmp_file.write("promoter:"+str(count_promoter_I)+"\r\n")
      tmp_file.write("enhancer:"+str(count_enhancer_I)+"\r\n")

      print(out)

      tmp_file.write("Loop types:"+"\r\n")
      total=out["promoter-promoter"]+out["promoter-strong enhancer"]+out["weak enhancer-promoter"]+out["promoter-strong enhancer"]+out["promoter-weak enhancer"]+out["strong enhancer-promoter"]+out["strong enhancer-strong enhancer"]+out["strong enhancer-weak enhancer"]+out["weak enhancer-strong enhancer"]+out["weak enhancer-weak enhancer"]
      pe=out["promoter-strong enhancer"]+out["weak enhancer-promoter"]+out["promoter-strong enhancer"]+out["promoter-weak enhancer"]+out["strong enhancer-promoter"]
      ee=out["strong enhancer-strong enhancer"]+out["strong enhancer-weak enhancer"]+out["weak enhancer-strong enhancer"]+out["weak enhancer-weak enhancer"]
      tmp_file.write("promoter-promoter:"+str(out["promoter-promoter"])+","+str(out["promoter-promoter"]/total)+"\r\n")
      tmp_file.write("promoter-enhancer:"+str(pe)+","+str(pe/total)+"\r\n")
      tmp_file.write("enhancer-enhancer:"+str(ee)+","+str(ee/total)+"\r\n")


if __name__ == "__main__":
   main(sys.argv[1:])