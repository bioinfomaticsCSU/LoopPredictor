#Merge feature
Args <- commandArgs()

tmp_folder<-Args[7]
feature_out<-Args[8]

file_names<- list.files(tmp_folder)
feature_merge<-read.csv(Args[6],sep="\t",header = FALSE)

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

#feature_filter<-subset(feature_merge,feature_merge[,num_27ac+3]>0 | feature_merge[,num_homer+3]<=2000)
#print(feature_filter)
#feature_filter <- as.data.frame(feature_filter)
write.table(feature_merge,feature_out,row.names = FALSE,sep="\t",quote=FALSE)

