# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 12:17:07 2020

@author: lekha
"""
from flask import Flask,request,make_response
from flask_cors import CORS
import pandas as pd
import json
import random
import matplotlib.pyplot as plt,mpld3
#Global data
global data
global graph

#Other Functions

#Function to generate random colours
def hexColour():
    r = lambda: random.randint(0,255)
    s='#%02X%02X%02X' % (r(),r(),r())
    return s


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
        fig,ax = plt.subplots()
        for i in range(len(x_attr)):
            xColName=x_attr[i]
            ax.bar(data[xColName].values.tolist(),data[y_attr].values.tolist(), width=0.8, color=hexColour(),label=xColName)
        plt.legend(loc="upper right")
        plt.ylabel(y_attr)
        #plt.savefig("temp.png")
        html=mpld3.fig_to_html(fig,figid='displayGraphOutput')
        #print(html)
        r = make_response(html)
        r.mimetype = 'text/plain'
    return r                
    
        
        
        
        
    
app.run(host='127.0.0.1', port= 5001)

