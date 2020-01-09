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

#constants
UPLOAD_FOLDER = '.\data'
ALLOWED_EXTENSIONS = {'csv', 'xls', 'txt', 'xlsx'}

#global variables
global trainFileName
global trainData
global trainDataDisplay
global targetData


#Function to check for valid extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Function to upload a file
def uploadFile():
    responseData=""
    
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
    print(df.iloc[0])
    return df

#Function to create file head and send it to front end
def fileHead(df):
    df.fillna("null",inplace=True)
    displayData=df.values.tolist()[0:5]
    metadata=list(df.columns)
    responseData={"data":displayData,"metaData":metadata}
    responseData=json.dumps(responseData,ensure_ascii=True,allow_nan=True)
    r = make_response(responseData)
    r.mimetype = 'text/plain'
    return r
    

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
    trainData.drop(removeColumns, axis=1, inplace=True)
    return "successfully removed columns"
    
    
    
#function to display global variables
@app.route('/data')
def data():
    global traintData
    global targetData
    print(trainData)
    print(targetData)
    
    
   
if __name__ == '__main__':
   app.run()