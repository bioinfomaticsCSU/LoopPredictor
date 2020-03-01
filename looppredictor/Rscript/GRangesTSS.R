#extract feature
Args <- commandArgs()
targrt<-Args[6]
save_tmp<-Args[7]

library(stringr)
library(ChIPpeakAnno)
#library(TxDb.Hsapiens.UCSC.hg19.knownGene)
#data(TSS.human.GRCh37)


targetFile <- read.table(Args[6],sep="\t",header = FALSE)
temp_df<-cbind(targetFile,targetFile)
temp_df<-temp_df[1,]
temp_df<-temp_df[-1,]
for(i in 1:nrow(targetFile)){
  chrom<-targetFile[i,1]
  extract_chrom<-subset(targetFile,targetFile[,"V1"]==chrom)
  for(j in 1:nrow(extract_chrom)){
    if(targetFile[i,2]<extract_chrom[j,2]){
      temp<-cbind(targetFile[i,],extract_chrom[j,])
      temp_df<-rbind(temp_df,temp)
    }
  }
}

targetFile<-temp_df

#######################################anchor1
targetRegion1 <- GRanges(seqnames = targetFile[,1],strand = "+",ranges = IRanges(start = targetFile$V2,end = targetFile$V3))
targetRegion1$TSS <- NaN
annotatedPeak <- annotatePeakInBatch(targetRegion1,AnnotationData=TSS.human.GRCh37,multiple=FALSE,select="first")
targetRegion1$TSS<-abs(annotatedPeak$distancetoFeature)
targetRegion1 <- as.data.frame(targetRegion1)

#######################################anchor2
targetRegion2 <- GRanges(seqnames = targetFile[,1],strand = "+",ranges = IRanges(start = targetFile$V5,end = targetFile$V6))
targetRegion2$TSS <- NaN
annotatedPeak <- annotatePeakInBatch(targetRegion2,AnnotationData=TSS.human.GRCh37,multiple=FALSE,select="first")
targetRegion2$TSS<-abs(annotatedPeak$distancetoFeature)
targetRegion2 <- as.data.frame(targetRegion2)

target_total<-cbind(targetRegion1, targetRegion2)
write.table(target_total,save_tmp,sep = "\t",quote = FALSE,row.names = FALSE)