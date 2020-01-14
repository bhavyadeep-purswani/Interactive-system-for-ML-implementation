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
from werkzeug.utils import secure_filename
from sklearn import preprocessing
#constants
UPLOAD_FOLDER = '.\data'
ALLOWED_EXTENSIONS = {'csv', 'xls', 'txt', 'xlsx'}

#global variables
global trainFileName
global trainData
global trainDataDisplay
global targetData
global preprocessingActions

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
        if nullHandler == "fillForward":
            trainData[columnName] = fillForward(columnName)
        elif nullHandler == "fillBackward":
            trainData[columnName] = fillBackward(columnName)
        elif nullHandler == "fillMostCommon":
            trainData[columnName] = fillMostCommon(columnName)
    
#function to display global variables
@app.route('/data')
def data():
    global trainData
    global targetData
    print(trainData)
    print(targetData)
    
    
   
if __name__ == '__main__':
   app.run()
   preprocessingActions = dict()