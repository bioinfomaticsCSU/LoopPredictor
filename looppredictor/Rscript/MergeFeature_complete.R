#Merge feature
Args <- commandArgs()
anchors<-Args[6]
tmp_folder<-Args[7]
model<-Args[8]
feature_out<-Args[9]


file_names<- list.files(tmp_folder)
feature_merge<-read.csv(Args[6],sep="\t",header = FALSE)

feature_merge["window_size"]<-feature_merge[,5]-feature_merge[,3]
#feature_merge<-subset(feature_merge,select=-c(1:7))
colnames(feature_merge)<-c("chrom_a1","start_a1","end_a1","chrom_a2","start_a2","end_a2","window_size")
for (i in 1:length(file_names)) {
  file_names_path=paste(tmp_folder,file_names[i], sep = "/")
  new.data = read.csv(file_names_path,sep="\t",header = FALSE,fill = TRUE,quote = "",stringsAsFactors = FALSE)
  print(file_names_path)
  new.data=new.data[-1,]
  name1<-paste(file_names[i],"a1",sep="_")
  name2<-paste(file_names[i],"a2",sep="_")
  name3<-paste(file_names[i],"n1_mean",sep="_")
  name4<-paste(file_names[i],"n1_std",sep="_")
  name5<-paste(file_names[i],"window_mean",sep="_")
  name6<-paste(file_names[i],"window_std",sep="_")
  name7<-paste(file_names[i],"n2_mean",sep="_")
  name8<-paste(file_names[i],"n2_std",sep="_")
  
  if (length(new.data[1,])>20){
  feature_merge[name1]=new.data$V6
  feature_merge[name2]=new.data$V12
	feature_merge[name3]=new.data$V18
	feature_merge[name4]=new.data$V19
	feature_merge[name5]=new.data$V25
	feature_merge[name6]=new.data$V26
	feature_merge[name7]=new.data$V32
	feature_merge[name8]=new.data$V33   
  }else{
    feature_merge[file_names[i]]=abs(as.numeric(new.data$V10))
  }
}

feature_merge[is.na(feature_merge)]<-0

#classify loop type
num_a1_27ac<-grep(".*K27ac.*a1", colnames(feature_merge),ignore.case = TRUE)
num_a2_27ac<-grep(".*K27ac.*a2", colnames(feature_merge),ignore.case = TRUE)
num_a1_tss<-grep("*tss_anchor1", colnames(feature_merge),ignore.case = TRUE)
num_a2_tss<-grep("*tss_anchor2", colnames(feature_merge),ignore.case = TRUE)

for(i in 1:nrow(feature_merge)){
  #anchor1
  if(as.numeric(feature_merge[i,num_a1_27ac])>10){
    if(abs(as.numeric(feature_merge[i,num_a1_tss]))<2000){
      flag1="Pro"
    }else{flag1="Enh"}
  }
  else{
    flag1="inactivete"
  }
  #anchor2
  if(as.numeric(feature_merge[i,num_a2_27ac])>10){
    if(abs(as.numeric(feature_merge[i,num_a2_tss]))<2000){
      flag2="Pro"
    }else{flag2="Enh"}
  }
  else{
    flag2="inactivete"
  }
feature_merge[i,"type"]=paste(flag1,flag2,sep="-")
}

select_df<-feature_merge[,c("chrom_a1","start_a1","end_a1","chrom_a2","start_a2","end_a2","type")]
if(grepl(".*median.*m", model,ignore.case = TRUE)){
  match_list<-c(".*ATAC.*a1",".*H3k27ac.*a1",".*H3k27me3.*a1",".*H3K4me1.*a1",".*H3k4me3.*a1",".*H3K9ac.*a1",".*H3K9me3.*a1",".*RNA.*a1",".*TSS.*anchor1",".*CTCF.*a1",".*ATAC.*a2",".*H3k27ac.*a2",".*H3k27me3.*a2",".*H3K4me1.*a2",".*H3k4me3.*a2",".*H3K9ac.*a2",".*H3K9me3.*a2",".*RNA.*a2",".*TSS.*anchor2",".*CTCF.*a2","window_size")
  for(j in match_list){
    temp_num<-grep(j, colnames(feature_merge),ignore.case = TRUE)
    temp_df<-feature_merge[,temp_num]
    select_df<-cbind(select_df,temp_df)
  }
}

#feature_merge<-select_df

#feature_filter<-feature_merge
#feature_filter<-feature_merge[, feature_merge [,num_27ac]>0 | feature_merge[,num_tss]<=2000]
#feature_filter <- as.data.frame(feature_filter)
write.table(select_df,feature_out,row.names = FALSE,sep="\t",quote=F)

