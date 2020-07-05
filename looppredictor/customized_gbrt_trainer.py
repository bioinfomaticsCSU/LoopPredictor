import sys
import os
import pandas as pd
import numpy as np
import getopt

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler,Normalizer
from sklearn.feature_selection import VarianceThreshold
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import RFE
from sklearn.feature_selection import f_regression, mutual_info_regression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.feature_selection import SelectKBest, f_regression, chi2

from sklearn.externals import joblib
import math


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

def main():
    argv=sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "t:f:g:o:n:",["trainfile=","feature=","genome=","output=","name="])
    except getopt.GetoptError:
        print ('Customized_GBRT_trainer.py -t <trainfile> -f <feature> -g <genome> -o <output_path> -n <output_name>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('Customized_GBRT_trainer.py -t <trainfile> -f <feature> -g <genome> -o <output_path> -n <output_name>')
            sys.exit()
        elif opt in ("-t", "--trainfile"):
            trainfile = arg
        elif opt in ("-f", "--feature"):
            feature = arg
        elif opt in ("-g", "--genome"):
            genome = arg
        elif opt in ("-o", "--output_path"):
            output_path =arg
        elif opt in ("-n", "--output_name"):
            output_name =arg

    ##extracing features
    flag=False
    work_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    commandline=work_path+"/looppredictor/Bash/FeatureGenerator_custom.sh " +trainfile+" "+feature+" "+output_path+" "+genome
    print ("commandline: "+commandline)
    flag=os.system(commandline)
    #flag=0
    if flag==0:
        print ("----------------------------FeatureGenerator success!--------------------\n")

        ##Read training sample...
        df_train = pd.read_csv(output_path+"/feature_out.txt", delimiter='\t', header=None)
        print(df_train.iloc[:,[0,1,2,3,4,5,6,7,8]])
        df_train=df_train.drop([0,1,2,3,4,5,6], axis=1)
        df_train=df_train.drop(0, axis=0)
        print(df_train)
        

        column_num=df_train.shape[1]+10

        data_train = df_train.values.astype('float')
        print(df_train)

        X = data_train[:, 1:column_num]
        Y = data_train[:, 0]

        scaler_x = StandardScaler().fit(X)
        X = scaler_x.transform(X)

        X_train_raw1, X_test_raw1, Y_train1, Y_test1 = train_test_split(X,Y,test_size=0.3, random_state=2)

        print(Y_test1)
    
        for i in range(len(Y)):
            if Y[i] == 0:
                Y[i] = math.log(Y[i]+1)
            else:
                Y[i] = math.log(Y[i])

        scaler_y = StandardScaler().fit(Y.reshape(-1, 1))
        Y = scaler_y.transform(Y.reshape(-1, 1))

        param_test3={
        "min_samples_leaf":[30,35,40,45,50],
        "min_samples_split":[350,400,500,550,600],
        "n_estimators":range(2000,8000,1000)
        }
    
        gbr=GradientBoostingRegressor(max_depth=20,min_samples_leaf=40,min_samples_split=500,loss='ls',max_features= 'auto', subsample= 1.0)
        sfm = SelectFromModel(gbr, threshold=1e-3)
        X=sfm.fit_transform(X, Y)
        X_train_raw, X_test_raw, Y_train, Y_test = train_test_split(X,Y,test_size=0.3, random_state=2)
    
        est = GridSearchCV(gbr, param_test3, n_jobs=-1, cv=3)
        est.fit(X_train_raw, Y_train)
        print('Best parameters found:\n', str(est.best_params_))

        Y_test_predict = est.predict(X_test_raw)
        Y_train_predict = est.predict(X_train_raw)
    
        print ("model_socre:")
        print ("test set:" + str(r2_score(Y_test, Y_test_predict)))
        print ("training set:" + str(r2_score(Y_train, Y_train_predict)))
        print ("----------------------------------------")
        print ("mean_squared_error:")
        print ("test set:" + str(mean_squared_error(Y_test, Y_test_predict)))
        print ("training set:" + str(mean_squared_error(Y_train, Y_train_predict)))


        Y_scaleback = scaler_y.inverse_transform(Y_test_predict)
        for i in range(len(Y_scaleback)):
            Y_scaleback[i]=math.exp(Y_scaleback[i])

        save_path_name = output_path + "/"+output_name + ".m"
        joblib.dump(est, save_path_name)
    

if __name__ == "__main__":
    main ()