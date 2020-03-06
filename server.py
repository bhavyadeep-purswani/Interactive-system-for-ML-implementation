
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 19:33:27 2020
@author: lekha
"""


from flask import Flask,request,make_response
import pandas as pd
from flask_cors import CORS
import json
import os
import requests
from werkzeug.utils import secure_filename
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

#constants
UPLOAD_FOLDER = '.\data'
ALLOWED_EXTENSIONS = {'csv', 'xls', 'txt', 'xlsx'}
GRAPH_URL = 'http://127.0.0.1:5001/loadGraphData'
HYPERPARAMETERS={
        "RandomForrestClassifier":{
                "n_estimators":{
                        "paramType":["int"],
                        "options":[],
                        "default":"100"
                        },
                 "max_depth":{
                        "paramType":["int"],
                        "options":[],
                        "default":"None"
                        },
                 "min_samples_split":{
                        "paramType":["float"],
                        "options":[],
                        "default":"2"
                        },
                 "min_samples_leaf":{
                        "paramType":["float"],
                        "options":[],
                        "default":"1"
                        },
                 "max_features":{
                        "paramType":["int","string"],
                        "options":["auto","log2","sqrt"],
                        "default":"auto"
                        },
                   
                 "max_leaf_nodes":{
                        "paramType":["int"],
                        "options":[],
                        "default":"None"
                        }
                 },
        "KNeighborsClassifier":{
                "n_neighbors":{
                        "paramType":["int"],
                        "options":[],
                        "default":"5"
                        },
                   
                "weights":{
                        "paramType":["str"],
                        "options":["uniform","distance"],
                        "default":"uniform"
                        },
                "algorithm":{
                       "paramType":["str"],
                        "options":['auto', 'ball_tree', 'kd_tree', 'brute'],
                        "default":"None"
                        },
                 "leaf_size":{
                        "paramType":["int"],
                        "options":[],
                        "default":"30"
                        }
                 },
            "RandomForrestRegressor":{
                "n_estimators":{
                        "paramType":["int"],
                        "options":[],
                        "default":"10"
                        },
                 "max_depth":{
                        "paramType":["int"],
                        "options":[],
                        "default":"None"
                        },
                 "min_samples_leaf":{
                        "paramType":["float"],
                        "options":[],
                        "default":"1"
                        },
                 "max_features":{
                        "paramType":["int","string"],
                        "options":["auto","log2","sqrt"],
                        "default":"auto"
                        },
                   
                 "max_leaf_nodes":{
                        "paramType":["int"],
                        "options":[],
                        "default":"None"
                        }
                 },
                 
                 "LinearRegression":{
                         "fit_intercept":{
                             "paramType":["bool"],
                             "options":[],
                             "default":"True"
                        }
                    },
                         
                         
       }
                    
                    
                
                
                
                
                #[[],[]]
                
                
                
                }
        
        
        
        }

#global variables
global trainFileName
global trainData
global trainDataDisplay
global targetData
global preprocessingActions
global X_train, X_test, y_train, y_test


#Function to convert strToBool
def strToBool(s):
    if(s=="True" or s=="true"):
        return True
    else:
        return False

#Function to check for valid extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Function to upload a file
def uploadFile():
    responseData=""
    fileName=None
    if request.method == 'POST':
        if 'file' not in request.files:
            responseData,fileName="No file part",None
        file = request.files['file']
        if file.filename == '':
            responseData,fileName="No selected file",None
        if file: 
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                responseData,fileName="File uploaded successfully",filename
            else:
                responseData,fileName="In valid Extension",None
        else:
            responseData,fileName="Error in uploading file",None
    return responseData,fileName

#Load data and convert it into dataframe
def loadData(filename):
    fileURL=UPLOAD_FOLDER+"\\"+filename
    if request.form['headerFlag'] == "True":
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
    global trainData
    r=fileHead(trainData)
    return r   
    
#Function for uploading and loading the file into dataframe               
@app.route('/trainUpload',methods=['POST'])
def trainUpload():
    global trainFileName
    global trainData
    responseData,fileName=uploadFile()
    if fileName!=None:
        trainFileName=fileName
        trainData=loadData(trainFileName)
    r = make_response(responseData)
    r.mimetype = 'text/plain'
    return r


#Function to select target attribute
@app.route('/selectTargetAttribute',methods=['POST'])
def selectTargetAttribute():
    global trainData
    global targetData
    targetColumn=request.form['targetColumn']
    if(isinstance(trainData.columns[0],str)==False):
        targetColumn=int(targetColumn)    
    targetData=trainData[targetColumn]
    trainData.drop(targetColumn, axis=1, inplace=True)
    return "Target Column Dropped"

#Function to remove columns
@app.route('/removeColumns',methods=['POST'])
def removeColumns():
    global trainData
    removeColumns=request.form['removeColumns']
    removeColumns=removeColumns.split(',')
    if(isinstance(trainData.columns[0],str)==False):
        removeColumns = list(map(int, removeColumns))
    preprocessingActions["removedColumns"]=removeColumns
    trainData.drop(removeColumns, axis=1, inplace=True)
    return "successfully removed columns"
    
#Function for handling null value removal requests
@app.route('/removeNullValue',methods=['POST'])
def removeNullValues():
    global trainData
    if request.method == "POST":
        columnName = request.form['columnName']
        nullHandler = request.form['nullHandler']
        if(isinstance(trainData.columns[0],str)==False):
            columnName=int(columnName) 
        column = trainData[columnName]
        if nullHandler == "fillForward":
            trainData[columnName] = fillForward(column)
        elif nullHandler == "fillBackward":
            trainData[columnName] = fillBackward(column)
        elif nullHandler == "fillMostCommon":
            trainData[columnName] = fillMostCommon(column)
        elif nullHandler == "fillMedian":
            trainData[columnName] = fillMedian(column)
        elif nullHandler == "fillMean":
            trainData[columnName] = fillMean(column)
        elif nullHandler == "fillCustom":
            trainData[columnName] = fillCustom(column, request.form['customValue'])
        elif nullHandler == "dropNullRows":
            trainData[columnName] = dropNullRows(trainData, columnName)
        
    
#function to display global variables
@app.route('/data')
def data():
    global trainData
    global targetData
        
    print(targetData)

#Function to call graph module
@app.route('/callGraph')
def callGraph():
    global trainData
    graphData=trainData.values.tolist()
    graphMetaData=list(trainData.columns)
    requestData= {'graphData':graphData, 'graphMetaData':graphMetaData}
    print(graphMetaData)
    #requestData=json.dumps(requestData,ensure_ascii=True,allow_nan=True)
    r = requests.post(url=GRAPH_URL, json=requestData)
    return "Yes"

#Function to split data
@app.route('/splitData',methods=['POST'])
def splitData():
    global trainData
    global targetData
    global X_train, X_test, y_train, y_test
    splitSizeType=request.form['splitSizeType']
    randomSeedType=request.form['randomSeedType']
    shuffleSplit=request.form['shuffleSplit']
    splitSizeNumber=request.form['splitSizeNumber']
    randomSeedNumber=request.form['randomSeedNumber']
    if(splitSizeType=="default"):
        testSize=0.25
    else:
        testSize=float(splitSizeNumber)
    if(randomSeedType=="default"):
        randomSeed=None
    else:
        randomSeed=int(randomSeedNumber)
    if(strToBool(shuffleSplit)):
        shuffle=True
    else:
        shuffle=False
    X_train, X_test, y_train, y_test=train_test_split(trainData, targetData, test_size=testSize, random_state=randomSeed,shuffle=shuffle)   
    responseData= {"X_train":X_train.values.tolist()[0:5],"X_test": X_test.values.tolist()[0:5], "y_train":y_train.values.tolist()[0:5],"y_test": y_test.values.tolist()[0:5]}
    responseData=json.dumps(responseData,ensure_ascii=True,allow_nan=True)
    r = make_response(responseData)
    r.mimetype = 'text/plain'
    return r

#Function to split data
@app.route('/standardizeData',methods=['POST'])
def standardizeData(): 
    global trainData
    standardizeType=request.form['standardizeType']
    columnNames=request.form['columnNames'].split(",")
    individualColumn=request.form['individualColumn']
    if(standardizeType=="standard"):
        scaler = StandardScaler()
        if(strToBool(individualColumn)):
            for col in columnNames:
                trainData[col]=scaler.fit_transform(trainData[[col]])
        else:
            new = trainData[columnNames].copy()
            scaler=scaler.fit(new)
            trainData[columnNames]=scaler.transform(trainData[columnNames])
    else:
        scaler = MinMaxScaler()
        if(strToBool(individualColumn)):
            for col in columnNames:
                trainData[col]=scaler.fit_transform(trainData[[col]])
        else:
            new = trainData[columnNames].copy()
            scaler=scaler.fit(new)
            trainData[columnNames]=scaler.transform(trainData[columnNames])
    new = trainData[columnNames].copy()
    responseData= {"standardData":new.values.tolist()[0:5]}
    r = make_response(responseData)
    r.mimetype = 'text/plain'
    return r
        
    
            
   
if __name__ == '__main__':
   app.run()
   preprocessingActions = dict()

    