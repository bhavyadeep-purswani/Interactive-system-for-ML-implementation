# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 12:17:07 2020

@author: lekha
"""
from flask import Flask,request,make_response
from flask_cors import CORS
import pandas as pd
import json

#Global data
global data
global graph

#Flask Code
app = Flask(__name__)
CORS(app)

#Function to set graph data
@app.route('/loadGraphData',methods=['POST'])
def loadGraphData():
    global data
    graphData=request.json['graphData']
    graphMetaData=request.json['graphMetaData']
    data=pd.DataFrame(graphData,columns=graphMetaData)
    #print(data)
    return "Yes"

#Function to return columns
@app.route('/graphType',methods=['POST'])
def graphType():
    global data
    global graph
    y_attr=[]
    x_attr=[]
    graph=request.form['graph']
    #print(graph)
    if graph=="bar":
        y_attr=list(data.columns)
        x_attr=list(data.columns)
        responseData={"X":x_attr,"Y":y_attr}
    
    responseData=json.dumps(responseData,ensure_ascii=True,allow_nan=True)
    r = make_response(responseData)
    r.mimetype = 'text/plain'
    return r
        
#Function to recieve attributes and plot graph
@app.route('/plotGraph',methods=['POST'])
def plotGraph():
    global data
    global graph
    y_attr=request.form['y_attr']
    x_attr=request.form['x_attr']
    x_attr=x_attr.split(',')
    if graph=="bar":
        if len(x_attr):
    return "Yes"
        
        
        
        
    
app.run(host='127.0.0.1', port= 5001)

