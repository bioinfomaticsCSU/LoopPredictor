#!/bin/bash

script_dir=$(cd $(dirname $0);pwd)
basepath=$(dirname $script_dir)
targetFile=$1
feature=$2
annoFile=$(ls $feature)
userpath=$3
genome=$4
filter=$5

for filename in $annoFile
do
	echo "${filename}"
	if [[ "$filename" == *"k27ac"* ]]; then
  		k27ac=$feature/$filename
  		echo "${k27ac}"
	elif [[ "$filename" == *"k4me1"* ]]; then
		k4me1=$feature/$filename
		echo "${k4me1}"
	elif [[ "$filename" == *"k4me3"* ]]; then
		k4me3=$feature/$filename
		echo "${k4me3}"
	else
		echo "------------------------------------------------"
	fi
done
wait

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

Rscript $basepath/Rscript/GRangesTool.R $targetFile $k27ac $userpath/tmp/feature_tmp_anno_27ac_anchor1 $userpath/tmp/feature_tmp_anno_27ac_anchor2 &
Rscript $basepath/Rscript/GRangesTool.R $targetFile $k4me1 $userpath/tmp/feature_tmp_anno_k4me1_anchor1 $userpath/tmp/feature_tmp_anno_k4me1_anchor2 &
Rscript $basepath/Rscript/GRangesTool.R $targetFile $k4me3 $userpath/tmp/feature_tmp_anno_k4me3_anchor1 $userpath/tmp/feature_tmp_anno_k4me3_anchor2 &
>> $userpath/log/GRange_Log.txt
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
Rscript $basepath/Rscript/MergeFeature.R  $targetFile $userpath/tmp $filter $userpath/$out_filename

