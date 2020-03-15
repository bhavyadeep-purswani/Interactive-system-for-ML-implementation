
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 19:33:27 2020
@author: lekha
"""


from flask import Flask,request,make_response,send_file
import pandas as pd
from flask_cors import CORS
import numpy as np
import json
import os
import requests
from werkzeug.utils import secure_filename
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVR
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support

#constants
UPLOAD_FOLDER = '.\data'
ALLOWED_EXTENSIONS = {'csv'}
GRAPH_URL = 'http://127.0.0.1:5001/loadGraphData'
HYPERPARAMETERS=json.loads(open("hyperparamters.json","r").read()) 
CALGORITHMS=["Random Forrest Classifier","KNeighbors Classifier","Logistic Regression","SVM Classification","Gaussian Naive Bayes","Neural Network Classification"]                 
RALGORITHMS=["Random Forrest Regressor","Linear Regression","SVM Regression","Gaussian Naive Bayes","Neural Network Regression"]                 

#global variables
global trainFileName
global dataset
global datasetDisplay
global targetData
global preprocessingActions
global X_train, X_test, y_train, y_test
global mod
global modFit
global predictedData


#hyperparamaeters={'var_smoothing': '1e-09','hidden_layer_sizes': 100,'activation': 'relu','alpha': 0.0001,'max_iter': 200,'learning_rate': 'constant','n_neighbors': 5,'weights': 'uniform','leaf_size': 30,'algorithm': 'auto'}
#Function to convert strToBool
def strToBool(s):
    if(s=="True" or s=="true" or s==True):
        return True
    else:
        return False

#Function to check for valid extensions
def allowed_file(filename,ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#function to create MachineLearning Model
def createModel(algorithm,hyperparameters):
    if algorithm=="Linear Regression":
        fit_intercept=strToBool(hyperparameters["fit_intercept"])
        mod=LinearRegression(fit_intercept=fit_intercept)
    if algorithm=="Random Forrest Classifier":
        n_estimators=int(float(hyperparameters["n_estimators"]))
        max_depth=int(float(hyperparameters["max_depth"]))
        min_samples_split=float(hyperparameters["min_samples_split"])
        min_samples_leaf=float(hyperparameters["min_samples_leaf"])
        max_features=hyperparameters["max_features"]
        if(max_features not in ["auto" ,"log2" ,"sqrt"] ):
            max_features=int(float(max_features))
        max_leaf_nodes=int(float(hyperparameters["max_leaf_nodes"]))
        mod=RandomForestClassifier(n_estimators=n_estimators,max_depth=max_depth,min_samples_split=min_samples_split,min_samples_leaf=min_samples_leaf,max_features=max_features,max_leaf_nodes=max_leaf_nodes)
    if algorithm=="Random Forrest Regressor":
        n_estimators=int(float(hyperparameters["n_estimators"]))
        max_depth=int(float(hyperparameters["max_depth"]))
        min_samples_leaf=float(hyperparameters["min_samples_leaf"])
        max_features=hyperparameters["max_features"]
        if(max_features not in ["auto" ,"log2" ,"sqrt"] ):
            max_features=int(float(max_features))
        max_leaf_nodes=int(float(hyperparameters["max_leaf_nodes"]))
        mod=RandomForestRegressor(n_estimators=n_estimators,max_depth=max_depth,min_samples_leaf=min_samples_leaf,max_features=max_features,max_leaf_nodes=max_leaf_nodes)
    if algorithm=="KNeighbors Classifier":
        n_neighbors=int(float(hyperparameters["n_neighbors"]))
        weights=hyperparameters["weights"]
        algorithmK=hyperparameters["algorithm"]
        leaf_size=int(float(hyperparameters["leaf_size"]))
        mod=KNeighborsClassifier(n_neighbors=n_neighbors,weights=weights,algorithm=algorithmK,leaf_size=leaf_size)
    if algorithm=="Logistic Regression":
        penalty=hyperparameters["penalty"]
        dual=strToBool(hyperparameters["dual"])
        c=float(hyperparameters["c"])
        max_iter=int(float(hyperparameters["max_iter"]))
        mod=LogisticRegression(penalty=penalty,dual=dual,c=c,max_iter=max_iter)
    if algorithm=="SVM Classification":
        C=int(float(hyperparameters["C"]))
        kernel=hyperparameters["kernel"]
        degree=int(float(hyperparameters["degree"]))
        gamma=hyperparameters["gamma"]
        max_iter=int(float(hyperparameters["max_iter"]))
        mod=SVC(C=C,degree=degree,kernel=kernel,gamma=gamma,max_iter=max_iter)
    if algorithm=="SVM Regression":
        C=int(float(hyperparameters["C"]))
        kernel=hyperparameters["kernel"]
        degree=int(float(hyperparameters["degree"]))
        gamma=hyperparameters["gamma"]
        max_iter=int(float(hyperparameters["max_iter"]))
        mod=SVR(C=C,degree=degree,kernel=kernel,gamma=gamma,max_iter=max_iter)
    if algorithm=="Gaussian Naive Bayes":
        var_smoothing=float(hyperparameters["var_smoothing"])
        mod=GaussianNB(var_smoothing=var_smoothing)
    if algorithm=="Neural Network Classification":
        hidden_layer_sizes=int(float(hyperparameters["hidden_layer_sizes"]))
        hidden_layer_sizes=tuple((hidden_layer_sizes,))
        activation=hyperparameters["activation"]
        alpha=float(hyperparameters["alpha"])
        learning_rate=hyperparameters["learning_rate"]
        max_iter=int(float(hyperparameters["max_iter"]))
        mod=MLPClassifier(hidden_layer_sizes=hidden_layer_sizes,activation=activation,alpha=alpha,learning_rate=learning_rate,max_iter=max_iter)
    if algorithm=="Neural Network Regression":
        hidden_layer_sizes=int(float(hyperparameters["hidden_layer_sizes"]))
        hidden_layer_sizes=tuple((hidden_layer_sizes,))
        activation=hyperparameters["activation"]
        alpha=float(hyperparameters["alpha"])
        learning_rate=hyperparameters["learning_rate"]
        max_iter=int(float(hyperparameters["max_iter"]))
        mod=MLPRegressor(hidden_layer_sizes=hidden_layer_sizes,activation=activation,alpha=alpha,learning_rate=learning_rate,max_iter=max_iter)
    return mod
#Function to fit and evaluate model
def createModelFit(mod,X,y):
    modFit=mod.fit(X,y)
    return modFit
    
#Function to evaluate model
def evaluateModel(modFit,X,y):
    y_pred=modFit.predict(X)
    accuracy=accuracy_score(y, y_pred)*100
    tup=list(precision_recall_fscore_support(y, y_pred,average="micro"))
    result={
            "accuracy":accuracy,
            "precision_recall_fscore_support":tup}
    return result

#Function to predict the prediction File
def predict(modFit,testData):
    predictedData=modFit.predict(testData)
    return predictedData
    
    

       
#function to standardize data
def standardizeData(data,standardizeType,columnNames,individualColumn):
    if(standardizeType=="standard"):
        scaler = StandardScaler()
        if(strToBool(individualColumn)):
            for col in columnNames:
                dataset[col]=scaler.fit_transform(dataset[[col]])
        else:
            new = dataset[columnNames].copy()
            scaler=scaler.fit(new)
            dataset[columnNames]=scaler.transform(dataset[columnNames])
    else:
        scaler = MinMaxScaler()
        if(strToBool(individualColumn)):
            for col in columnNames:
                dataset[col]=scaler.fit_transform(dataset[[col]])
        else:
            new = dataset[columnNames].copy()
            scaler=scaler.fit(new)
            dataset[columnNames]=scaler.transform(dataset[columnNames])
    return data
    
                   

#Function to upload a file
def uploadFile(ALLOWED_EXTENSIONS):
    responseData=""
    fileName=None
    if request.method == 'POST':
        if 'file' not in request.files:
            responseData,fileName="No file part",None
        file = request.files['file']
        if file.filename == '':
            responseData,fileName="No selected file",None
        if file: 
            if allowed_file(file.filename,ALLOWED_EXTENSIONS):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                responseData,fileName="File uploaded successfully",filename
            else:
                responseData,fileName="Invalid Extension",None
        else:
            responseData,fileName="Error in uploading file",None
    return responseData,fileName

#Load data and convert it into dataframe
def loadData(filename,headerFlag):
    fileURL=UPLOAD_FOLDER+"\\"+filename
    if headerFlag == True:
        df = pd.read_csv(fileURL)
    else:
        df = pd.read_csv(fileURL,header=None)
    return df

#Function to create file head and send it to front end
def fileHead(df):
    df=df.fillna("null")
    displayData=df.values.tolist()[0:5]
    metadata=list(df.columns)
    responseData={"data":displayData,"metaData":metadata}
    responseData=json.dumps(responseData,ensure_ascii=True,allow_nan=True)
    r = make_response(responseData)
    r.mimetype = 'text/plain'
    return r

#Function to check if data contains Null values
def containsNull(data):
    return any(data.isnull())

#Function to fill the data with custom value
def fillCustom(data,value):
    data.fillna(value,inplace = True)
    return data

#Function to fill the data with Mean Value
def fillMean(data):
    data.fillna(data.mean(),inplace=True)
    return data

#Function to fill the data with Median Value
def fillMedian(data):
    data.fillna(data.median(),inplace=True)
    return data

#Function to fill the data with most common value
def fillMostCommon(data):
    data.fillna(data.mode().iloc[0],inplace = True)
    return data

#Function to drop rows that have null value corresponding to a column
def dropNullRows(data,referenceColumn):
    data.dropna(subset=list(referenceColumn),inplace=True)
    return data

#Function to forward fill the data
def fillForward(data):
    data.fillna(method="ffill",inplace = True)
    return data

#Function to backward fill the data
def fillBackward(data):
    data.fillna(method="bfill",inplace = True)
    return data

#Function to Label Encode Column
def labelEncode(data):
    labelEncoder = preprocessing.LabelEncoder()
    data = labelEncoder.fit_transform(data)
    return data
    


#Flask Code
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

#Function to return the head of dataframe
@app.route('/trainHead',methods=['GET'])
def trainHead():
    global dataset
    r=fileHead(dataset)
    return r   
    
#Function for uploading and loading the file into dataframe               
@app.route('/trainUpload',methods=['POST'])
def trainUpload():
    global trainFileName
    global dataset
    headerFlag=strToBool(request.form["headerFlag"])
    responseData,fileName=uploadFile(ALLOWED_EXTENSIONS)
    if fileName!=None:
        trainFileName=fileName
        dataset=loadData(trainFileName,headerFlag)
    r = make_response(responseData)
    r.mimetype = 'text/plain'
    return r


#Function to select target attribute
@app.route('/selectTargetAttribute',methods=['POST'])
def selectTargetAttribute():
    global dataset
    global targetData
    targetColumn=request.form['targetColumn']
    if(isinstance(dataset.columns[0],str)==False):
        targetColumn=int(targetColumn)    
    targetData=dataset[targetColumn]
    dataset.drop(targetColumn, axis=1, inplace=True)
    return "Target Column Dropped"

#Function to remove columns
@app.route('/removeColumns',methods=['POST'])
def removeColumns():
    global dataset
    removeColumns=request.form['removeColumns']
    removeColumns=removeColumns.split(',')
    if(isinstance(dataset.columns[0],str)==False):
        removeColumns = list(map(int, removeColumns))
    preprocessingActions["removedColumns"]=removeColumns
    dataset.drop(removeColumns, axis=1, inplace=True)
    return "successfully removed columns"
    
#Function for handling null value removal requests
@app.route('/removeNullValue',methods=['POST'])
def removeNullValues():
    global dataset
    if request.method == "POST":
        columnName = request.form['columnName']
        nullHandler = request.form['nullHandler']
        if(isinstance(dataset.columns[0],str)==False):
            columnName=int(columnName) 
        column = dataset[columnName]
        if nullHandler == "fillForward":
            dataset[columnName] = fillForward(column)
        elif nullHandler == "fillBackward":
            dataset[columnName] = fillBackward(column)
        elif nullHandler == "fillMostCommon":
            dataset[columnName] = fillMostCommon(column)
        elif nullHandler == "fillMedian":
            dataset[columnName] = fillMedian(column)
        elif nullHandler == "fillMean":
            dataset[columnName] = fillMean(column)
        elif nullHandler == "fillCustom":
            dataset[columnName] = fillCustom(column, request.form['customValue'])
        elif nullHandler == "dropNullRows":
            dataset[columnName] = dropNullRows(dataset, columnName)
        
    
#function to display global variables
@app.route('/data')
def data():
    global dataset
    global targetData
        
    print(targetData)

#Function to call graph module
@app.route('/callGraph')
def callGraph():
    global dataset
    graphData=dataset.values.tolist()
    graphMetaData=list(dataset.columns)
    requestData= {'graphData':graphData, 'graphMetaData':graphMetaData}
    print(graphMetaData)
    #requestData=json.dumps(requestData,ensure_ascii=True,allow_nan=True)
    r = requests.post(url=GRAPH_URL, json=requestData)
    return "Yes"

#Function to split data
@app.route('/splitData',methods=['POST'])
def splitData():
    global dataset
    global targetData
    global X_train, X_test, y_train, y_test
    
    shuffle=strToBool(request.form['shuffle'])
    testSize=float(request.form['testSize'])
    randomSeed=int(request.form['randomSeed'])
    X_train, X_test, y_train, y_test=train_test_split(dataset, targetData, test_size=testSize, random_state=randomSeed,shuffle=shuffle)   
    #responseData= {"X_train":X_train.values.tolist()[0:5],"X_test": X_test.values.tolist()[0:5], "y_train":y_train.values.tolist()[0:5],"y_test": y_test.values.tolist()[0:5]}
    #responseData=json.dumps(responseData,ensure_ascii=True,allow_nan=True)
    #r = make_response(responseData)
    #r.mimetype = 'text/plain'
    return "success"

#Function to split data
@app.route('/standardizeData',methods=['POST'])
def sendStandardizeData():  
    global dataset
    standardizeType=request.form['standardizeType']
    columnNames=request.form['columnNames'].split(",")
    individualColumn=request.form['individualColumn']
    dataset=standardizeData(dataset,standardizeType,columnNames,individualColumn)
    return "success"
        
#Function to return list of algorithms based on type of algorithm
@app.route('/getAlgorithms',methods=['POST'])
def getAlgorithms(): 
    typeAlgorithm=request.form['typeAlgorithm']
    if(typeAlgorithm=="classification"):
         responseData= {"algorithms":CALGORITHMS}
    else:
        responseData= {"algorithms":RALGORITHMS}
    r = make_response(responseData)
    r.mimetype = 'text/plain'
    return r

#Function to return list of hyperparameters based on algorithm
@app.route('/getHyperparameters',methods=['POST'])            
def getHyperparameters(): 
    algorithm=request.form['algorithm']
    responseData= {"hyperparameters":HYPERPARAMETERS[algorithm]}
    print(request)
    r = make_response(responseData)
    r.mimetype = 'text/plain'
    return r

@app.route('/trainModel',methods=['POST'])            
def trainModel():
    global mod,modFit
    global X_train, y_train
    algorithm=request.form['algorithm']
    hyperparams=json.loads(request.form['hyperparams'])["hyperparameters"]
    mod=createModel(algorithm,hyperparams)
    modFit=createModelFit(mod,X_train,y_train)
    return "success"

@app.route('/evaluateModel')     
def evaluate():
   global mod,modFit
   global X_test, y_test
   responseData=evaluateModel(modFit,X_test,y_test)
   r = make_response(responseData)
   r.mimetype = 'text/plain'
   return r

@app.route('/predictFile',methods=['POST'])     
def predictFile():
    global modFit,predictedData
    headerFlag=strToBool(request.form["headerFlag"])
    responseData,fileName=uploadFile(ALLOWED_EXTENSIONS)
    if fileName!=None:
        testDataset=loadData(fileName,headerFlag)
        predictedData=predict(modFit,testDataset)
    return "success"

@app.route('/downloadPrediction')
def downloadPrediction():
    global predictedData
    print(predictedData)
    pd.DataFrame(predictedData).to_csv(".\data\predictions.csv")
    return send_file(".\data\\predictions.csv", as_attachment=True)

    
   

if __name__ == '__main__':
   app.run()
   preprocessingActions = dict()

    