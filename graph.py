# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 12:17:07 2020

@author: lekha
"""
from flask import Flask,request
from flask_cors import CORS
import pandas as pd

global data

#Flask Code
app = Flask(__name__)
CORS(app)

#Function to set graph data
@app.route('/loadGraphData',methods=['POST'])
def loadGraphData():
    global data
    responseData=request.json['graphData']
    data=pd.DataFrame(responseData)
    #print(data)
    return "Yes"

#Function to return columns
@app.route('/graphFunc',methods=['POST'])
def graphFunc():
    graph=request.form['graph']
        
    
app.run(host='127.0.0.1', port= 5001)

