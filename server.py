
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 19:33:27 2020
@author: lekha
"""

from flask import Flask, request, make_response, send_file
import pandas as pd
from flask_cors import CORS
import json
import requests
from sklearn.model_selection import train_test_split
from modules.MLModelProcessing import createModel, createModelFit, evaluateModel
from modules.constants import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, GRAPH_URL, HYPERPARAMETERS, CALGORITHMS, RALGORITHMS
from modules.fileprocessing import loadData, fileHead, uploadFile
from modules.preprocess import standardizeData, containsNull, fillCustom, fillMean, fillMedian, fillMostCommon, dropNullRows, fillForward, fillBackward, labelEncode, oneHotEncode
from modules.utilities import strToBool, checkForStrings, fetchPreProcessData, appendAllNulls

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
global preprocessingActions
global params

#params={}
#preprocessingActions = "from modules.preprocess import *\nimport server\nimport pandas as pd\ndef preprocess(params):\n\tdataset=params['dataset']"


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
    global dataset,params,preprocessingActions
    headerFlag= strToBool(request.form["headerFlag"])
    responseData,fileName= uploadFile(ALLOWED_EXTENSIONS, app.config['UPLOAD_FOLDER'])
    if fileName!=None:
        trainFileName=fileName
        dataset= loadData(trainFileName, headerFlag)
        params={}
        preprocessingActions = "from modules.preprocess import *\nimport server\nimport pandas as pd\ndef preprocess(params):\n\tdataset=params['dataset']"
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
    global preprocessingActions,params
    removeColumns=request.form['removeColumns']
    removeColumns=removeColumns.split(',')
    removeColumns=[x.strip() for x in removeColumns]
    if(isinstance(dataset.columns[0],str)==False):
        removeColumns = list(map(int, removeColumns))
    dataset.drop(removeColumns, axis=1, inplace=True)
    preprocessingActions+="\n\tdataset.drop({0},axis=1,inplace=True)".format(str(removeColumns))
    return "successfully removed columns"
    
#Function for handling null value removal requests
@app.route('/removeNullValue',methods=['POST'])
def removeNullValues():
    global dataset,preprocessingActions,params

    if request.method == "POST":
        columnName = request.form['columnName']
        nullHandler = request.form['nullHandler']
        if(isinstance(dataset.columns[0],str)==False):
            columnName=int(columnName) 
        column = dataset[columnName]
        if nullHandler == "fillForward":
            dataset[columnName] = fillForward(column)
            preprocessingActions += "\n\tdataset['{0}']=fillForward(dataset['{0}'])".format(columnName)
        elif nullHandler == "fillBackward":
            dataset[columnName] = fillBackward(column)
            preprocessingActions += "\n\tdataset['{0}']=fillBackward(dataset['{0}'])".format(columnName)
        elif nullHandler == "fillMostCommon":
            dataset[columnName] = fillMostCommon(column)
            preprocessingActions += "\n\tdataset['{0}']=fillMostCommon(dataset['{0}'])".format(columnName)
        elif nullHandler == "fillMedian":
            dataset[columnName] = fillMedian(column)
            preprocessingActions += "\n\tdataset['{0}']=fillMedian(dataset['{0}'])".format(columnName)
        elif nullHandler == "fillMean":
            dataset[columnName] = fillMean(column)
            preprocessingActions += "\n\tdataset['{0}']=fillMean(dataset['{0}'])".format(columnName)
        elif nullHandler == "fillCustom":
            if(str(dataset.dtypes[columnName])=='object'):
                dataset[columnName] = fillCustom(column, str(request.form['customValue']))
                preprocessingActions += "\n\tdataset['{0}']=fillCustom(dataset['{0}'],'{1}')".format(columnName,request.form['customValue'])
            else:
                dataset[columnName] = fillCustom(column, request.form['customValue'])
                preprocessingActions += "\n\tdataset['{0}']=fillCustom(dataset['{0}'],{1})".format(columnName, request.form['customValue'])
        elif nullHandler == "dropNullRows":
            dataset = dropNullRows(dataset, columnName)
            preprocessingActions += "\n\tdataset=dropNullRows(dataset,'{0}')".format(columnName)

    return "Success"

#Api to one hot encode
@app.route('/oneHotEncodeColumns',methods=['POST'])
def oneHotEncodeColumns():
    global dataset,preprocessingActions,params
    preprocessingActions= appendAllNulls(preprocessingActions)
    columnNames = request.form['columnNames'].split(",")
    for col in columnNames:
        df,enc= oneHotEncode(dataset[[col]],None)
        params['one'+col]=enc
        preprocessingActions += "\n\tdf=oneHotEncode(dataset[['{0}']],params['one'+'{0}'])".format(col)
        dataset = dataset.drop(columns=col)
        preprocessingActions += "\n\tdataset = dataset.drop(columns='{0}')".format(col)
        dataset = pd.concat([dataset, df], axis=1)
        preprocessingActions += "\n\tdataset = pd.concat([dataset, df], axis=1)"
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
    global dataset,preprocessingActions,params
    preprocessingActions = appendAllNulls(preprocessingActions)
    columnNames = checkForStrings(dataset)
    for col in columnNames:
        data,labelEncoder= labelEncode(dataset[[col]],None)
        params['lab'+col]=labelEncoder
        preprocessingActions += "\n\tdata = labelEncode(dataset[['{0}']],params['lab'+'{0}'])".format(col)
        dataset[col]=data
        preprocessingActions += "\n\tdataset['{0}']=data".format(col)
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
    global dataset,params,preprocessingActions
    standardizeType=request.form['standardizeType']
    columnNames=request.form['columnNames'].split(",")
    individualColumn=request.form['individualColumn']
    if (strToBool(individualColumn)):
        for col in columnNames:
            dataset[col],enc= standardizeData(dataset[[col]], standardizeType,None)
            params['stan' + col] = enc
            preprocessingActions += "\n\tdataset['{0}'] = standardizeData(dataset[['{0}']],'{1}',params['stan'+'{0}'])".format(col,standardizeType)
    else:
        columns=dataset.columns
        dataset,enc=standardizeData(dataset,standardizeType,None)
        dataset=pd.DataFrame(dataset,columns=columns)
        params['stan'] = enc
        preprocessingActions += "\n\tdataset = standardizeData(dataset,'{0}',params['stan'])".format(standardizeType)
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
    global params,preprocessingActions
    headerFlag= strToBool(request.form["headerFlag"])
    responseData,fileName= uploadFile(ALLOWED_EXTENSIONS, app.config['UPLOAD_FOLDER'])
    if fileName!=None:
        testDataset= loadData(fileName, headerFlag)
        params['dataset']=testDataset
        predictedData= fetchPreProcessData(params, preprocessingActions)
        #predictedData= predict(modFit, preprocessedData)
    return "success"

@app.route('/downloadPrediction')
def downloadPrediction():
    global predictedData
    #pd.DataFrame(predictedData).to_csv(".\generated\predictions.csv") #Windows
    #return send_file(".\generated\\predictions.csv", as_attachment=True) #For windows
    pd.DataFrame(predictedData).to_csv("generated/predictions.csv")
    return send_file("generated/predictions.csv", as_attachment=True)

    
   

if __name__ == '__main__':
   app.run()



