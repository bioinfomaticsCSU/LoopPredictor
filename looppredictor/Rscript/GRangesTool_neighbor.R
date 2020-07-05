#extract feature
Args <- commandArgs()
targrt<-Args[6]
annoFile<-Args[7]
save_tmp<-Args[8]
genome<-Args[9]


save_path<-normalizePath(dirname(save_tmp))
library(stringr)


#library(TxDb.Hsapiens.UCSC.hg19.knownGene)
if(genome=="mm10"){
  if (!requireNamespace("TxDb.Mmusculus.UCSC.mm10.knownGene", quietly = TRUE))
    BiocManager::install("TxDb.Mmusculus.UCSC.mm10.knownGene")
  
  library("TxDb.Mmusculus.UCSC.mm10.knownGene")
}else{
  if (!requireNamespace("TxDb.Hsapiens.UCSC.hg19.knownGene", quietly = TRUE))
    BiocManager::install("TxDb.Hsapiens.UCSC.hg19.knownGene")
  
  library("TxDb.Hsapiens.UCSC.hg19.knownGene")
}

targetFile <- read.table(Args[6],sep="\t",header = FALSE)
#row.names(targetFile)<-c(1:nrow(targetFile))
#print(targetFile)

#end_3<-as.numeric(column_num)+2
#######################################window
  print("parsing window...")
  targetRegion3 <- GRanges(seqnames = targetFile[,1],strand = "+",ranges = IRanges(start = targetFile[,3]+1,end = targetFile[,5]-1))
  targetRegion3$mean <- NaN
  targetRegion3$sd <- NaN
  annotationFile <- read.table(annoFile,header = FALSE)
  annotationRegion<- GRanges(seqnames = annotationFile[,1],ranges = IRanges(start = annotationFile[,2], end=annotationFile[,3]))
  hitObj3<- findOverlaps(targetRegion3,annotationRegion)
  annotationRegion$score<-annotationFile$V7
  peakid<- unique(hitObj3@from)
  for(i in 1:length(peakid)){
    secondid<- hitObj3[hitObj3@from==peakid[i],]@to
    overlap <- annotationRegion[secondid]
    targetRegion3[peakid[i]]$mean<- mean(overlap$score)
    targetRegion3[peakid[i]]$sd<- sd(overlap$score)
  }
targetRegion3[is.na(targetRegion3)] = 0
targetRegion3 <- as.data.frame(targetRegion3)
window_save_tmp<-paste(save_tmp,"_window")
write.table(targetRegion3,window_save_tmp,sep = "\t",quote = FALSE,row.names = FALSE)
#######################################neighbor1
print("parsing neighbor region1...")
  targetRegion1 <- GRanges(seqnames = targetFile[,1],strand = "+",ranges = IRanges(start = targetFile[,2]-2000,end = targetFile[,2]-1))
  targetRegion1$mean <- NaN
  targetRegion1$sd <- NaN
  hitObj1<- findOverlaps(targetRegion1,annotationRegion)
  annotationRegion$score<-annotationFile$V7
  peakid<- unique(hitObj1@from)
  for(i in 1:length(peakid)){
    secondid<- hitObj1[hitObj1@from==peakid[i],]@to
    overlap <- annotationRegion[secondid]
    targetRegion1[peakid[i]]$mean<- mean(overlap$score)
    targetRegion1[peakid[i]]$sd<- sd(overlap$score)
  }
targetRegion1[is.na(targetRegion1)] = 0
targetRegion1 <- as.data.frame(targetRegion1)
neighbor1_save_tmp<-paste(save_tmp,"_neighbor1")
write.table(targetRegion1,neighbor1_save_tmp,sep = "\t",quote = FALSE,row.names = FALSE)
#######################################neighbor2
print("parsing neighbor region2...")
targetRegion2 <- GRanges(seqnames = targetFile[,4],strand = "+",ranges = IRanges(start = targetFile[,6]+1,end = targetFile[,6]+2000))
  targetRegion2$mean <- NaN
  targetRegion2$sd <- NaN
  annotationFile <- read.table(annoFile,header = FALSE)
  hitObj2<- findOverlaps(targetRegion2,annotationRegion)
  annotationRegion$score<-annotationFile$V7
  peakid<- unique(hitObj2@from)
  for(i in 1:length(peakid)){
    secondid<- hitObj2[hitObj2@from==peakid[i],]@to
    overlap <- annotationRegion[secondid]
    targetRegion2[peakid[i]]$mean<- mean(overlap$score)
    targetRegion2[peakid[i]]$sd<- sd(overlap$score)
  }
targetRegion2[is.na(targetRegion2)] = 0
targetRegion2 <- as.data.frame(targetRegion2)
neighbor2_save_tmp<-paste(save_tmp,"_neighbor2")
write.table(targetRegion2,neighbor2_save_tmp,sep = "\t",quote = FALSE,row.names = FALSE)
#######################################anchor1
print("parsing neighbor anchor1...")
  targetRegion <- GRanges(seqnames = targetFile[,1],strand = "+",ranges = IRanges(start = targetFile[,2],end = targetFile[,3]))
  targetRegion$value <- NaN
  hitObj<- findOverlaps(targetRegion,annotationRegion)
  if (str_detect(annoFile,'Methyl')==TRUE){
    annotationRegion$meth<-annotationFile$V10
    annotationRegion$cov<-annotationFile$V11
    peakid<- unique(hitObj@from)
    for(i in 1:length(peakid)){
    secondid<- hitObj[hitObj@from==peakid[i],]@to
    overlap <- annotationRegion[secondid]
    targetRegion[peakid[i]]$value<- weighted.mean(overlap$meth,overlap$cov)
  }
}else{
    annotationRegion$score<-annotationFile$V7
    peakid<- unique(hitObj@from)
    for(i in 1:length(peakid)){
    secondid<- hitObj[hitObj@from==peakid[i],]@to
    overlap <- annotationRegion[secondid]
    targetRegion[peakid[i]]$value<- sum(overlap$score)
  }
}
targetRegion[is.na(targetRegion)] = 0
targetRegion <- as.data.frame(targetRegion)
anchor1_save_tmp<-paste(save_tmp,"_anchor1")
write.table(targetRegion,anchor1_save_tmp,sep = "\t",quote = FALSE,row.names = FALSE)
#######################################anchor2
print("parsing neighbor anchor2...")
  targetRegion4 <- GRanges(seqnames = targetFile[,4],strand = "+",ranges = IRanges(start = targetFile[,5],end = targetFile[,6]))
  targetRegion4$value <- NaN
  hitObj4<- findOverlaps(targetRegion4,annotationRegion)
  if (str_detect(annoFile,'Methyl')==TRUE){
    annotationRegion$meth<-annotationFile$V10
    annotationRegion$cov<-annotationFile$V11
    peakid<- unique(hitObj4@from)
    for(i in 1:length(peakid)){
    secondid<- hitObj4[hitObj4@from==peakid[i],]@to
    overlap <- annotationRegion[secondid]
    targetRegion4[peakid[i]]$value<- weighted.mean(overlap$meth,overlap$cov)
  }
}else{
    annotationRegion$score<-annotationFile$V7
    peakid<- unique(hitObj4@from)
    for(i in 1:length(peakid)){
    secondid<- hitObj4[hitObj4@from==peakid[i],]@to
    overlap <- annotationRegion[secondid]
    targetRegion4[peakid[i]]$value<- sum(overlap$score)
  }
}
targetRegion4[is.na(targetRegion4)] = 0
targetRegion4 <- as.data.frame(targetRegion4)
anchor2_save_tmp<-paste(save_tmp,"_anchor2")
write.table(targetRegion4,anchor2_save_tmp,sep = "\t",quote = FALSE,row.names = FALSE)
#########################################
#target_total<-cbind(targetRegion, targetRegion4, targetRegion1, targetRegion3, targetRegion2)      #anchor1,2,neighbor1,window,neighbor2
#write.table(target_total,save_tmp,sep = "\t",quote = FALSE,row.names = FALSE)


