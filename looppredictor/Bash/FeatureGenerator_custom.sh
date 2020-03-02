#!/bin/bash

script_dir=$(cd $(dirname $0);pwd)
basepath=$(dirname $script_dir)
targetFile=$1
feature=$2
annoFile=$(ls $feature)
userpath=$3
genome=$4

if [ ! -d $userpath/tmp  ];then
  mkdir $userpath/tmp
else
  echo "----------------tmp fold exist----------------------"
fi

if [ ! -d $userpath/log  ];then
  mkdir $userpath/log
else
  echo "----------------log fold exist-----------------------"
fi

for filename in $annoFile
do
Rscript $basepath/Rscript/GRangesTool.R $targetFile $feature/$filename $userpath/tmp/feature_tmp_${filename}_anchor1 $userpath/tmp/feature_tmp_${filename}_anchor2 &
done >> $userpath/log/GRange_Log.txt
wait
echo "--------------Feature extraction done!----------------"

awk '{print $1"	"$2"	"$3}' $targetFile > $userpath/tmp/anchor1.tmp
awk '{print $4"	"$5"	"$6}' $targetFile > $userpath/tmp/anchor2.tmp
annotatePeaks.pl $userpath/tmp/anchor1.tmp $genome  >  $userpath/tmp/feature_tmp_anno_homer_anchor1 && >> $userpath/log/Homer_log.txt
annotatePeaks.pl $userpath/tmp/anchor2.tmp $genome  >  $userpath/tmp/feature_tmp_anno_homer_anchor2 && >> $userpath/log/Homer_log.txt
echo "--------------Homer annotates done!-------------------"

rm -f $userpath/tmp/*.tmp
out_file=$(basename -- "$targetFile")
out_filename="${out_file%.*}_Output.txt"

echo "--------------Merging features!-----------------------"
Rscript $basepath/Rscript/MergeFeature_custom.R  $targetFile $userpath/tmp $userpath/feature_out.txt

