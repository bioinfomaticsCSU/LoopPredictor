#!/bin/bash

script_dir=$(cd $(dirname $0);pwd)
basepath=$(dirname $script_dir)
targetFile=$1
annoFile_path=$2
userpath=$3
annoFile=$(ls $annoFile_path)
genome=$4
model=$5

if [ ! -d $userpath/tmp3  ];then
  mkdir $userpath/tmp3
else
  echo "----------------------------tmp3 fold exist----------------------------"
fi

if [ ! -d $userpath/log ];then
  mkdir $userpath/log
else
  echo "----------------------------log fold exist-----------------------------"
fi

for filename in $annoFile
do
	echo $filename
	Rscript $basepath/Rscript/GRangesTool_neighbor.R $targetFile $annoFile_path/$filename $userpath/tmp3/tmp_feature_$filename $genome &
done >> $userpath/log/GRangeNeighbor_Log.txt
wait
echo "----------------------------Annotation done!-----------------------------"

target_temp=$userpath/tmp3/target.tmp
awk '{print $1"	"$2"	"$3}' $target_temp > $userpath/tmp3/anchor1.tmp
awk '{print $4"	"$5"	"$6}' $target_temp > $userpath/tmp3/anchor2.tmp
annotatePeaks.pl $userpath/tmp3/anchor1.tmp $genome  >  $userpath/tmp3/tmp_feature_tss_anchor1 && >> $userpath/log/Homer_log.txt
annotatePeaks.pl $userpath/tmp3/anchor2.tmp $genome  >  $userpath/tmp3/tmp_feature_tss_anchor2 && >> $userpath/log/Homer_log.txt
echo "----------------------------Homer annotates done!-------------------------"
rm -f $userpath/tmp3/*.tmp

echo "----------------------------Merging features!-----------------------------"
Rscript $basepath/Rscript/MergeFeature_complete.R  $targetFile  $userpath/tmp3  $model $userpath/feature_out.txt

