import sys
import numpy
import pandas as pd
import getopt
import os
import shutil
from sklearn.neural_network import MLPRegressor

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from pathos.multiprocessing import ProcessPool
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib
import math

def setDir(tmp_dir):
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.mkdir(tmp_dir)

def cleanOutlier(data,column,mul=3):
    data = data[data[:,column].argsort()]
    l = len(data)
    low = int(l/4)
    high = int(l/4*3)
    lowValue = data[low,column]
    highValue = data[high,column]
    if lowValue - mul * (highValue - lowValue) < data[0,column]:
        delLowValue = data[0,column]
    else:
        delLowValue = lowValue - mul * (highValue - lowValue)
    if highValue + mul * (highValue - lowValue) > data[-1,column]:
        delHighValue = data[-1,column]
    else:
        delHighValue = highValue + mul * (highValue - lowValue)
    for i in range(low):
        if data[i,column] >= delLowValue:
            recordLow = i
            break
    for i in range(len(data)-1,high,-1):
        if data[i,column] <= delHighValue:
            recordHigh = i
            break

    print("origin total row:{}".format(len(data)))
    print("retain:{}-{}row".format(recordLow,recordHigh))
    data = data[recordLow:recordHigh+1]
    print("delete column:{},reamining column:{}".format(column,\
          recordHigh+1-recordLow))
    print("-------------------------------------------------------------------")
    return data

def extractFunc_map2(predict_extrChrom,num,row,total):
    if int(predict_extrChrom.iloc[num][2]) <= int(predict_extrChrom.iloc[row][1]):
        distance = int(predict_extrChrom.iloc[row][1]) - int(predict_extrChrom.iloc[num][2])
        feature_list = predict_extrChrom.iloc[num][0:total].tolist() + predict_extrChrom.iloc[row][0:total].tolist()
        feature_list.append(distance)
    else:
        feature_list=[]
    return feature_list

def extracFunc_map(predict_extrChrom,num,total):
    list_predict_extrChrom = [predict_extrChrom for row in range(num+1,total)]
    list_num=[num for row in range(num+1,total)]
    list_total=[total for row in range(num+1,total)]
    list_row=[row for row in range(num+1,total)]
    if num < total:
        extract_loop_fitst = list(map(extractFunc_map2, list_predict_extrChrom, list_num, list_row,list_total))
    else:
        print("The End")
    extract_loop_df=pd.DataFrame(extract_loop_fitst)
    return extract_loop_df


def scaleAndPredict_map(rootdir,list_path,scaler_x,scaler_y,clf,column_num,output_name,cutoff):
    path = os.path.join(rootdir, list_path)
    if os.path.isfile(path):
        if path.find("feature_")>-1:
            df_tmp = pd.read_csv(path, delimiter='\t', header=None, low_memory=False)
            df_tmp_backup=df_tmp[[0, 1, 2,column_num, column_num + 1, column_num + 2]]
            df_tmp.drop(columns=[0, 1, 2,column_num, column_num + 1, column_num + 2],inplace=True)            
            print(path+": "+"Start to scale the feature...")
            X_predict = scaler_x.transform(df_tmp)

            print(path+": "+"Start to predict...")
            Y_predict = clf.predict(X_predict)
            Y_scaleback = scaler_y.inverse_transform(Y_predict)
            for i in range(len(Y_scaleback)):
                Y_scaleback[i]=math.exp(Y_scaleback[i])
            df_tmp_backup["predict"]=Y_scaleback
            df_tmp_backup = df_tmp_backup.loc[df_tmp_backup['predict']>int(cutoff)]

            list_name=os.path.splitext(list_path)[0]
            df_tmp_backup.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
            df_tmp_backup.to_csv(output_name+"/predict_results/predict_"+list_name, index=False, sep=" ",header=False)
            print(path+" "+"predict success!")
        else:
            print(path+" "+"feature file dosen't exist!")
    else:
        print(path+" "+"predict failed!")

def scaleAndPredict(df_tmp,scaler_x,scaler_y,clf,column_num,output_name,cutoff):
        df_tmp_backup=df_tmp[["V1","V2","V3","V4","V5","V6","type"]]
        df_tmp.drop(["V1","V2","V3","V4","V5","V6","type"],inplace=True,axis=1) 
         
        print("---------------------Start to scale the feature-----------------")
        X_predict = scaler_x.transform(df_tmp)

        print("---------------------Start to predict---------------------------")
        Y_predict = clf.predict(X_predict)
        print("number of predicting loops:",len(Y_predict))

        Y_scaleback = scaler_y.inverse_transform(Y_predict)
        for i in range(len(Y_scaleback)):
            Y_scaleback[i]=math.exp(Y_scaleback[i])
        df_tmp_backup["predict"]=Y_scaleback
        df_tmp_backup = df_tmp_backup.loc[df_tmp_backup['predict']>int(cutoff)]
        return df_tmp_backup
    

##Write the features into new files according to chromasomes
def extractFunc(df_predict,chromName,output_name):
    predict_extrChrom = df_predict.loc[chromName]
    predict_extrChrom = predict_extrChrom[predict_extrChrom["V2"].notnull()].copy()
    predict_extrChrom = predict_extrChrom[predict_extrChrom["V3"].notnull()].copy()
    predict_extrChrom.loc[:,["V2"]] = predict_extrChrom.loc[:,["V2"]].astype('int')
    predict_extrChrom.loc[:,["V3"]] = predict_extrChrom.loc[:,["V3"]].astype('int')
    predict_extrChrom=predict_extrChrom.sort_values(by=['V2'])
    predict_extrChrom_rowNum=predict_extrChrom.shape[0]
    predict_extrChrom_columnNum=predict_extrChrom.shape[1]
    predict_extrChrom.reset_index(drop=True)
    predict_extrChrom.index = [i for i in range(predict_extrChrom_rowNum)]
    print("Extracting features of "+chromName+"...")

    list_predict_extrChrom = [predict_extrChrom for row in range(predict_extrChrom_rowNum)]
    list_num=[row for row in range(predict_extrChrom_rowNum)]
    list_total=[predict_extrChrom_rowNum for row in range(predict_extrChrom_rowNum)]
    extract_loop_fitst = list(map(extracFunc_map, list_predict_extrChrom,list_num,list_total))
    extract_loop_df=pd.DataFrame(columns=[predict_extrChrom_columnNum])
    '''
    for i in range(len(extract_loop_fitst)):
        df_tmp=extract_loop_fitst[i]
        extract_loop_df=extract_loop_df.append(df_tmp)
    '''
    print("Writing features of " + chromName+"...")
    extract_loop_df.to_csv(output_name+'/tmp2/feature_' + str(chromName), index=False, header=False, sep="\t")
    print(extract_loop_df)
    return extract_loop_df

def predict(infile,trainfile,model,cutoff,output):
    ##Read predict sample...
    ##modify the name/order of features
    df_predict = pd.read_csv(infile, delimiter='\t',low_memory=False)
    colnames=df_predict.columns.values.tolist()
    #df_predict=changeName(colnames,df_predict)

    column_num=df_predict.shape[1]

    
    df_predict.rename(columns={colnames[0]:'V1',colnames[1]:'V2',colnames[2]:'V3',colnames[3]:'V4',colnames[4]:'V5',colnames[5]:'V6'},inplace = True)
    
    ##load the scale and model of training set
    df_train = pd.read_csv(trainfile, delimiter='\t', header=None)
    data_train = df_train.values.astype('float')
    X = data_train[:, 1:column_num]
    Y = data_train[:, 0]
    for i in range(len(Y)):
        if Y[i] == 0:
            Y[i] = math.log(Y[i]+1)
        else:
            Y[i] = math.log(Y[i])

    scaler_x = StandardScaler().fit(X)
    scaler_y = StandardScaler().fit(Y.reshape(-1, 1))
    clf = joblib.load(model)
    print("---------------------Loading model success!---------------------")

    df_tmp_backup=scaleAndPredict(df_predict,scaler_x,scaler_y,clf,column_num,output,cutoff)
    df_tmp_backup.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
    df_tmp_backup.to_csv(output+"/predicted_result.bedpe", index=False, sep="\t",header=False)
    print("---------------------predict success!---------------------------")
