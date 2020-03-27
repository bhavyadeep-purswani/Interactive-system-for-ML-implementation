
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 19:33:27 2020
@author: lekha
"""


from flask import Flask,request,make_response,send_file
import pandas as pd
from flask_cors import CORS
import json
import requests
from sklearn.model_selection import train_test_split
from modules.MLModelProcessing import createModel, createModelFit, evaluateModel, predict
from modules.constants import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, GRAPH_URL, HYPERPARAMETERS, CALGORITHMS, RALGORITHMS
from modules.fileprocessing import uploadFile, loadData, fileHead
from modules.preprocessing import standardizeData, containsNull, fillCustom, fillMean, fillMedian, fillMostCommon, \
    dropNullRows, fillForward, fillBackward, labelEncode, oneHotEncode
from modules.utilities import strToBool, checkForStrings




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

#Flask Code
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

#Function to return the head of dataframe
@app.route('/trainHead',methods=['GET'])
def trainHead():
    global dataset
    r= fileHead(dataset)
    return r   

#Function for uploading and loading the file into dataframe               
@app.route('/trainUpload',methods=['POST'])
def trainUpload():
    global trainFileName
    global dataset
    headerFlag= strToBool(request.form["headerFlag"])
    responseData,fileName= uploadFile(ALLOWED_EXTENSIONS)
    if fileName!=None:
        trainFileName=fileName
        dataset= loadData(trainFileName, headerFlag)
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
            dataset = dropNullRows(dataset, columnName)

    return "Success"

#Api to one hot encode
@app.route('/oneHotEncodeColumns',methods=['POST'])
def oneHotEncodeColumns():
    global dataset
    columnNames = request.form['columnNames'].split(",")
    for col in columnNames:
        df,enc= oneHotEncode(dataset[[col]])
        dataset = dataset.drop(columns=col)
        dataset = pd.concat([dataset, df], axis=1)
    return "Success"

#Api to get string
@app.route('/getStringColumns',methods=['GET'])
def getStringColumns():
    global dataset
    columnNames = checkForStrings(dataset)
    return json.dumps({'columnList':columnNames},ensure_ascii=True, allow_nan=True)

#Api to label encode
@app.route('/labelEncodeColumns',methods=['GET'])
def labelEncodeColumns():
    global dataset
    columnNames = checkForStrings(dataset)
    for col in columnNames:
        data,labelEncoder= labelEncode(dataset[[col]])
        dataset[col]=data
    return "Success"



#Function to return if any column contains null
@app.route('/getNullValue',methods=['POST'])
def getNullValue():
    global dataset
    column = request.form['columnName']
    if containsNull(dataset[column]):
        return "True"
    else:
        return "False"


@app.route('/getColumnsWithNullValues')
def columnsWithNullVaues():
    global dataset
    columns = []
    for column in dataset.columns:
        if containsNull(dataset[column]):
            columns.append(column)
    return json.dumps({'columnList':columns},ensure_ascii=True, allow_nan=True)
#function to display global variables
@app.route('/data')
def data():
    global dataset
    global targetData


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
    
    shuffle= strToBool(request.form['shuffle'])
    testSize=float(request.form['testSize'])
    randomSeed=int(request.form['randomSeed'])
    X_train, X_test, y_train, y_test=train_test_split(dataset, targetData, test_size=testSize, random_state=randomSeed,shuffle=shuffle)
    return "Success"

#Function to split data
@app.route('/standardizeData',methods=['POST'])
def sendStandardizeData():  
    global dataset
    standardizeType=request.form['standardizeType']
    columnNames=request.form['columnNames'].split(",")
    individualColumn=request.form['individualColumn']
    dataset= standardizeData(dataset, standardizeType, columnNames, individualColumn)
    return "success"
        
#Function to return list of algorithms based on type of algorithm
@app.route('/getAlgorithms',methods=['POST'])
def getAlgorithms(): 
    typeAlgorithm=request.form['typeAlgorithm']
    if(typeAlgorithm=="classification"):
         responseData= {"algorithms": CALGORITHMS}
    else:
        responseData= {"algorithms": RALGORITHMS}
    r = make_response(responseData)
    r.mimetype = 'text/plain'
    return r

#Function to return list of hyperparameters based on algorithm
@app.route('/getHyperparameters',methods=['POST'])            
def getHyperparameters(): 
    algorithm=request.form['algorithm']
    responseData= {"hyperparameters": HYPERPARAMETERS[algorithm]}
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
    mod= createModel(algorithm, hyperparams)
    modFit= createModelFit(mod, X_train, y_train)
    return "success"

@app.route('/evaluateModel')     
def evaluate():
   global mod,modFit
   global X_test, y_test
   responseData= evaluateModel(modFit, X_test, y_test)
   r = make_response(responseData)
   r.mimetype = 'text/plain'
   return r

@app.route('/predictFile',methods=['POST'])     
def predictFile():
    global modFit,predictedData
    headerFlag= strToBool(request.form["headerFlag"])
    responseData,fileName= uploadFile(ALLOWED_EXTENSIONS)
    if fileName!=None:
        testDataset= loadData(fileName, headerFlag)
        predictedData= predict(modFit, testDataset)
    return "success"

@app.route('/downloadPrediction')
def downloadPrediction():
    global predictedData
    print(predictedData)
    pd.DataFrame(predictedData).to_csv(".\data\predictions.csv")
    return send_file(".\data\\predictions.csv", as_attachment=True)

    
   

if __name__ == '__main__':
   app.run()
   preprocessingActions = ""

    
