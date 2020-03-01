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


def scaleAndPredict(rootdir,list_path,scaler_x,scaler_y,clf,column_num,output_name,cutoff):
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
    for i in range(len(extract_loop_fitst)):
        df_tmp=extract_loop_fitst[i]
        extract_loop_df=extract_loop_df.append(df_tmp)
    print("Writing features of " + chromName+"...")
    extract_loop_df.to_csv(output_name+'/tmp2/feature_' + str(chromName), index=False, header=False, sep="\t")
    print(extract_loop_df)
    return extract_loop_df

##changeName
def changeName(colnames, df_predict):
    for i in range(len(colnames)):
        if colnames[i].upper().find("ATAC")>-1:
            colnames[i]="f1"
        elif colnames[i].upper().find("H3K27AC")>-1:
            colnames[i]="f2"
        elif colnames[i].upper().find("H3K36ME3")>-1:
            colnames[i]="f3"
        elif colnames[i].upper().find("H3K4ME1")>-1:
            colnames[i]="f4"
        elif colnames[i].upper().find("H3K4ME2")>-1:
            colnames[i]="f5"
        elif colnames[i].upper().find("H3K4ME3")>-1:
            colnames[i]="f6"
        elif colnames[i].upper().find("H3K79ME2")>-1:
            colnames[i]="f7"
        elif colnames[i].upper().find("H3K9AC")>-1:
            colnames[i]="f8"
        elif colnames[i].upper().find("H3K9ME3")>-1:
            colnames[i]="f9"
        elif colnames[i].upper().find("RNA")>-1:
            colnames[i]="f10"
        elif colnames[i].upper().find("METHYL")>-1:
            colnames[i]="f11"
        elif colnames[i].upper().find("HOMER")>-1:
            colnames[i]="f12"
        elif colnames[i].upper().find("CTCF")>-1:
            colnames[i]="f13"
        elif colnames[i].upper().find("ELF1")>-1:
            colnames[i]="f14"
        elif colnames[i].upper().find("JUND")>-1:
            colnames[i]="f15"
        elif colnames[i].upper().find("MAX")>-1:
            colnames[i]="f16"
        elif colnames[i].upper().find("YY1")>-1:
            colnames[i]="f17"
        else:
            continue
    df_predict.columns=colnames
    order = ['V1','V2','V3','f1','f2','f3','f4','f5','f6','f7','f8','f9','f10','f11','f12','f13','f14','f15','f16','f17']
    df_predict= df_predict[order]
    return df_predict

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "i:t:m:c:o:p:",["infile=", "trainfile=","model=","cutoff=","output=","pool_num="])
    except getopt.GetoptError:
        print ('TrainingTool.py -i <infile> -t <trainfile> -m <model> -c <cutoff> -o <output_name> -p <pool_num>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('TrainingTool.py -i <infile> -t <trainfile> -m <model> -c <cutoff> -o <output_name> -p <pool_num>')
            sys.exit()
        elif opt in ("-i", "--infile"):
            infile = arg
        elif opt in ("-t", "--trainfile"):
            trainfile = arg
        elif opt in ("-m", "--model"):
            model = arg
        elif opt in ("-c", "--cutoff"):
            cutoff = arg
        elif opt in ("-p", "--pool_num"):
            pool_num = arg
        elif opt in ("-o", "--output_name"):
            output_name =arg

    pool = ProcessPool(int(pool_num))

    ##Read predict sample...
    ##modify the name/order of features
    df_predict = pd.read_csv(infile, delimiter='\t',low_memory=False)
    colnames=df_predict.columns.values.tolist()
    #df_predict=changeName(colnames,df_predict)

    column_num=df_predict.shape[1]

    df_predict.rename(columns={colnames[0]:'V1',colnames[1]:'V2',colnames[2]:'V3'},inplace = True)
    df_predict=df_predict.set_index(["V1"], append=False, drop=False)
    
    chromName_list=df_predict.index.values.tolist()
    chromName_list_new=[]
    extract_out=[]
    for i in chromName_list:
        if i not in chromName_list_new:
            chromName_list_new.append(i)

    ##extract features form the output of Extractfeatures.sh
    setDir(output_name+"/tmp2")
    list_df_predict= [df_predict for row in range(len(chromName_list_new))]
    list_output_name=[output_name for row in range(len(chromName_list_new))]
    extract_out=pool.map(extractFunc,list_df_predict,chromName_list_new,list_output_name)
    
    ##merge features
    feature_num=2*column_num
    df_features=pd.DataFrame(columns=[feature_num])
    rootdir = output_name+'/tmp2' 
    list_path = os.listdir(rootdir)
    list_rootdir=[rootdir for row in range(len(list_path))]
    list_column_num=[column_num for row in range(len(list_path))]
    list_output_name=[output_name for row in range(len(list_path))]

    ##load the scale and model of training set
    df_train = pd.read_csv(trainfile, delimiter='\t', header=None)
    data_train = df_train.values.astype('float')
    X = data_train[:, 1:40]
    Y = data_train[:, 0]
    for i in range(len(Y)):
        if Y[i] == 0:
            Y[i] = math.log(Y[i]+1)
        else:
            Y[i] = math.log(Y[i])

    scaler_x = StandardScaler().fit(X)
    scaler_y = StandardScaler().fit(Y.reshape(-1, 1))
    clf = joblib.load(model)
    print("Loading model success!")

    list_clf=[clf for row in range(len(list_path))]
    list_scaler_x=[scaler_x for row in range(len(list_path))]
    list_scaler_y=[scaler_y for row in range(len(list_path))]
    list_cutoff=[cutoff for row in range(len(list_path))]

    ##scale the features and predict
    setDir(output_name+"/predict_results/")
    pool.map(scaleAndPredict,list_rootdir,list_path,list_scaler_x,list_scaler_y,list_clf,list_column_num,list_output_name,list_cutoff)

    
if __name__ == "__main__":
    main(sys.argv[1:])