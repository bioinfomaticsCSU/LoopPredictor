#extract feature
Args <- commandArgs()
targrt<-Args[6]
annoFile<-Args[7]
save_tmp1<-Args[8]
save_tmp2<-Args[9]
library(stringr)
library(TxDb.Hsapiens.UCSC.hg19.knownGene)

  targetFile <- read.table(targrt,sep="\t",header = FALSE)
  if(length(targetFile[1,])<3){
    targetFile <- read.table(targrt,sep=" ",header = FALSE)
  }
  targetRegion1 <- GRanges(seqnames = targetFile$V1,strand = "+",ranges = IRanges(start = targetFile$V2,end = targetFile$V3))
  targetRegion2 <- GRanges(seqnames = targetFile$V4,strand = "+",ranges = IRanges(start = targetFile$V5,end = targetFile$V6))
  targetRegion1$value <- NaN
  targetRegion2$value <- NaN
  annotationFile <- read.table(annoFile,header = FALSE)
  annotationRegion<- GRanges(seqnames = annotationFile$V1,ranges = IRanges(start = annotationFile$V2, end=annotationFile$V3))
  hitObj1<- findOverlaps(targetRegion1,annotationRegion)
  hitObj2<- findOverlaps(targetRegion2,annotationRegion)

    annotationRegion$score<-annotationFile$V7
    peakid<- unique(hitObj1@from)
    for(i in 1:length(peakid)){
    secondid<- hitObj1[hitObj1@from==peakid[i],]@to
    overlap <- annotationRegion[secondid]
    targetRegion1[peakid[i]]$value<- sum(overlap$score)
	}
	
	annotationRegion$score<-annotationFile$V7
    peakid<- unique(hitObj2@from)
    for(i in 1:length(peakid)){
    secondid<- hitObj2[hitObj2@from==peakid[i],]@to
    overlap <- annotationRegion[secondid]
    targetRegion2[peakid[i]]$value<- sum(overlap$score)
	}


targetRegion1 <- as.data.frame(targetRegion1)
write.table(targetRegion1,save_tmp1,sep = "\t",quote = FALSE,row.names = FALSE)
targetRegion2 <- as.data.frame(targetRegion2)
write.table(targetRegion2,save_tmp2,sep = "\t",quote = FALSE,row.names = FALSE)



