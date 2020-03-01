#Merge feature
Args <- commandArgs()
anchors<-Args[6]
tmp_folder<-Args[7]
filter<-Args[8]
feature_out<-Args[9]

file_names<- list.files(tmp_folder)
feature_merge<-read.csv(Args[6],sep="\t",header = FALSE)
num_27ac_a1<-grep("27ac_anchor1", file_names,ignore.case = TRUE,value = FALSE)
num_27ac_a2<-grep("27ac_anchor2", file_names,ignore.case = TRUE,value = FALSE)
num_homer_a1<-grep("homer_anchor1", file_names,ignore.case = TRUE,value = FALSE)
num_homer_a2<-grep("homer_anchor2", file_names,ignore.case = TRUE,value = FALSE)
num_k4me1_a1<-grep("k4me1_anchor1", file_names,ignore.case = TRUE,value = FALSE)
num_k4me1_a2<-grep("k4me1_anchor2", file_names,ignore.case = TRUE,value = FALSE)
num_k4me3_a1<-grep("k4me3_anchor1", file_names,ignore.case = TRUE,value = FALSE)
num_k4me3_a2<-grep("k4me3_anchor2", file_names,ignore.case = TRUE,value = FALSE)
for (i in 1:length(file_names)) {
  file_names_path=paste(tmp_folder,file_names[i], sep = "/")
  new.data = read.csv(file_names_path,sep="\t",header = FALSE,stringsAsFactors = FALSE)
  print(file_names_path)
  new.data=new.data[-1,]
  if (length(new.data[1,])<7){
    feature_merge[file_names[i]]=new.data$V6
    feature_merge[,file_names[i]]<-as.numeric(feature_merge[,file_names[i]])
  }else{
    new.data=as.data.frame(lapply(new.data,as.numeric))
    new.data=new.data[order(new.data$V1),]
    feature_merge[file_names[i]]=abs(as.numeric(new.data$V10))
  }
}

feature_merge[is.na(feature_merge)] <- 0

for (i in 1:nrow(feature_merge)){
  #identification for anchor1
  if(as.numeric(feature_merge[i,num_27ac_a1])>10){
    if(as.numeric(feature_merge[i,num_homer_a1])<2000){
      flag1="pro"
    }
    else{
      if(as.numeric(feature_merge[i,num_k4me1_a1])>as.numeric(feature_merge[i,num_k4me3_a1])){
        flag1="strong_enh"
      }
      else{
      flag1="weak_enh"
     }
    }   
  }
  else{
    flag1="inactivate"
  }

  #identification for anchor2
  if(as.numeric(feature_merge[i,num_27ac_a2])>10){
    if(as.numeric(feature_merge[i,num_homer_a2])<2000){
      flag2="pro"
    }
    else{
      if(as.numeric(feature_merge[i,num_k4me1_a2])>as.numeric(feature_merge[i,num_k4me3_a2])){
        flag2="strong_enh"
      }
      else{
      flag2="weak_enh"
     }
    }   
  }
  else{
    flag2="inactivate"
  }

feature_merge[i,"type"]=paste(flag1, flag2, sep="-")

if((grepl("*enh",flag1)) & (grepl("*enh",flag2))){
  feature_merge[i,"filter"]=3
}else if((grepl("pro", flag1)) & (grepl("pro", flag2))){
  feature_merge[i,"filter"]=4
}else if(flag1=="inactivate" | flag2=="inactivate"){
  feature_merge[i,"filter"]=5
}else{feature_merge[i,"filter"]=2}

}

if(filter==1){
  feature_filter<-feature_merge[,c("V1","type")]
}else if(filter==2){
  feature_filter<-subset(feature_merge[,c("V1","type")],feature_merge[,"filter"]==2)
}else if(filter==3){
    feature_filter<-subset(feature_merge[,c("V1","type")],feature_merge[,"filter"]==3)
}else if(filter==4){  
    feature_filter<-subset(feature_merge[,c("V1","type")],feature_merge[,"filter"]==4)
}else{feature_filter<-subset(feature_merge[,c("V1","type")],feature_merge[,"filter"]==5)}

colnames(feature_filter)<-c("loop","type")

#feature_filter<-subset(feature_merge,feature_merge[,num_27ac+3]>0 | feature_merge[,num_homer+3]<=2000)
#print(feature_filter)
#feature_filter <- as.data.frame(feature_filter)
write.table(feature_filter,feature_out,row.names = FALSE,sep="\t",quote=FALSE)

