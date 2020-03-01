#!/bin/bash

basepath=$(cd `dirname $0`; pwd)
annoFile_path=$1
userpath=$2
annoFile=$(ls $annoFile_path)
genome=$3
model=$4

for filename in $annoFile
do
	if [[ "$filename" == *"k27ac"* ]]; then
  	targetFile=$annoFile_path/$filename
  	break
	fi
done
wait

echo $targetFile

if [ ! -d $userpath/tmp3  ];then
  mkdir $userpath/tmp3
else
  echo "--------------tmp3 fold exist--------------"
fi

if [ ! -d $userpath/log ];then
  mkdir $userpath/log
else
  echo "--------------log fold exist--------------"
fi

for filename in $annoFile
do
	echo $filename
	Rscript $basepath/GRangesTool_neighbor.R $targetFile $annoFile_path/$filename $userpath/tmp3/tmp_feature_$filename $genome &
done >> $userpath/log/GRangeNeighbor_Log.txt
wait
echo "--------------Annotation done!----------------"

target_temp=$userpath/tmp3/target.tmp
awk '{print $1"	"$2"	"$3}' $target_temp > $userpath/tmp3/anchor1.tmp
awk '{print $4"	"$5"	"$6}' $target_temp > $userpath/tmp3/anchor2.tmp
annotatePeaks.pl $userpath/tmp3/anchor1.tmp $genome  >  $userpath/tmp3/tmp_feature_tss_anchor1 &&
annotatePeaks.pl $userpath/tmp3/anchor2.tmp $genome  >  $userpath/tmp3/tmp_feature_tss_anchor2 &&
echo "--------------Homer annotates done!-------------"
rm -f $userpath/tmp3/*.tmp

echo "--------------Merging features!-----------------"
Rscript $basepath/MergeFeature_complete.R  $targetFile  $userpath/tmp3 $model $userpath/feature_out.txt

