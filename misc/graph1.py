# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 12:17:07 2020

@author: lekha
"""
from flask import Flask,request,make_response
from flask_cors import CORS
from bokeh.plotting import figure, output_notebook, show 
import plotly.express as px
import pandas as pd
import json
import random
import numpy 
import pandas as pd
import matplotlib.pyplot as plt,mpld3

import math

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval
from bokeh.palettes import Spectral8

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
    if graph=="scatter":
        y_attr2=list()
        x_attr2=list()
        y_attr=list(data.columns)
        x_attr=list(data.columns)
        for x in x_attr:
            #print(x)
            #print(data[x][0])
            print(type(data[x][0]))
            if(type(data[x][0])==numpy.int64):
                print("NOT STRING")
                y_attr2.append(x)
                x_attr2.append(x)
        
        
        responseData={"X":x_attr2,"Y":y_attr2}
    if graph=="line":
        y_attr2=list()
        y_attr=list(data.columns)
        x_attr=list(data.columns)
        for x in x_attr:
            #print(x)
            #print(data[x][0])
            print(type(data[x][0]))
            if(type(data[x][0])==numpy.int64):
                print("INTEGER")
                y_attr2.append(x)
              
        
        
        responseData={"X":y_attr2,"Y":y_attr2}
    if graph=="box":
        y_attr2=list()
        x_attr2=list()
        y_attr=list(data.columns)
        x_attr=list(data.columns)
        for x in x_attr:
            #print(x)
            #print(data[x][0])
            print(type(data[x][0]))
            if(type(data[x][0])==numpy.int64 or data[x][0]==float):
                print("NOT STRING")
                y_attr2.append(x)
                x_attr2.append(x)
        
        
        responseData={"X":x_attr2,"Y":y_attr2}
    if graph=="correlation":
        y_attr2=list()
        y_attr=list(data.columns)
        x_attr=list(data.columns)
        for x in x_attr:
            #print(x)
            #print(data[x][0])
            print(type(data[x][0]))
            if(type(data[x][0])==numpy.int64):
                print("INTEGER")
                y_attr2.append(x)
              
        
        
        responseData={"X":x_attr,"Y":y_attr2}
    
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
        df=data
        output_file("graph2.html")
        p = figure(plot_width=1000, plot_height=1000)
        xlabel=""
        for attr in range(len(x_attr)):
            p.vbar(x=data[x_attr[attr]], width=1.5, bottom=0,top=data[y_attr],color=hexColour(),legend=x_attr[attr])
            xlabel+=" "
            xlabel+=x_attr[attr]
        p.xaxis.axis_label =xlabel
        p.yaxis.axis_label = y_attr
        show(p)
    if graph=="scatter":
        df=data
        output_file("graph2.html")
        p = figure(plot_width=600, plot_height=600)
        print(x_attr[0])
        print(y_attr)
        print(data[x_attr[0]])
        print(data[y_attr])
        p.square(data[x_attr[0]], data[y_attr], size=20, color=hexColour(),legend=x_attr[0])
        p.xaxis.axis_label =x_attr[0]
        p.yaxis.axis_label = y_attr
        show(p)
    if graph=="line":
        df=data
        output_file("graph2.html")
        p = figure(plot_width=600, plot_height=600)
        p.line(data[x_attr[0]], data[y_attr],color=hexColour(),legend=x_attr[0])
        p.xaxis.axis_label =x_attr[0]
        p.yaxis.axis_label = y_attr
        show(p)
    if graph=="box":
        df=data
        output_file("graph2.html")
        p = figure(plot_width=600, plot_height=600)
        p.line(data[x_attr[0]], data[y_attr],color=hexColour(),legend=x_attr[0])
        show(p)
    if graph=="correlation":
        df=data
        output_file("graph2.html")
        p = figure(plot_width=600, plot_height=600)
        xlabel=""
        for attr in range(len(x_attr)):
            p.line(data[x_attr[attr]], data[y_attr],color=hexColour(),legend=x_attr[attr])
            xlabel+=" "
            xlabel+=x_attr[attr]
        p.xaxis.axis_label =xlabel
        p.yaxis.axis_label = y_attr
        show(p)
    return r                
    
        
        
        
        
    
app.run(host='127.0.0.1', port= 5001)

