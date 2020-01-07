# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 19:33:27 2020

@author: lekha
"""


from flask import Flask,request,jsonify,make_response,flash,redirect, url_for
import pandas as pd
from flask_cors import CORS, cross_origin
import json
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import csv

#constants
UPLOAD_FOLDER = '.\data'
ALLOWED_EXTENSIONS = {'csv', 'xls', 'txt', 'xlsx'}

#global variables
global trainFileName
global trainData

#Function to display the data in tabular form 
def displayData(trainData,testData):
    displayTrainData=trainData.values.tolist()[0:5]
    displayTestData=testData.values.tolist()[0:5]
    return displayTrainData,displayTestData

#Function to check for valid extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Function to upload a file
def uploadFile():
    responseData=""
    
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            responseData,fileName="No file part",None
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
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
    with open(fileURL, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count==0:
                df=pd.DataFrame(columns=row)
            else:
                df.loc[line_count]=row
            line_count += 1
    return df

#Function to create file head and send it to front end
def fileHead(df):
    displayData=df.values.tolist()[0:5]
    metadata=list(df.columns)
    responseData={"data":displayData,"metaData":metadata}
    responseData=json.dumps(responseData)
    #print(displayTrainData)
    r = make_response(responseData)
    r.mimetype = 'text/plain'
    return r
    

#Flask Code
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

@app.route('/trainHead',methods=['GET'])
def trainHead():
    global trainData
    r=fileHead(trainData)
    return r   
    #return jsonify(trainData=displayTrainData,
                   #testData=displayTestData,
                   #trainMetaData=trainMetaData)
                   
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

@app.route('/data')
def data():
    global trainData
    print(trainData)
    
    
if __name__ == '__main__':
   app.run()