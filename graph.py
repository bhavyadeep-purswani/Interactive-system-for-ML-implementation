# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 12:17:07 2020

@author: lekha
"""
import json
import random
import webbrowser
import pandas as pd
from bokeh.io import show, output_file
import matplotlib.pyplot as plt
from bokeh.plotting import figure
from flask import Flask, request, make_response
from flask_cors import CORS
from bokeh.models.annotations import Title
from bokeh.layouts import gridplot
from sklearn import preprocessing
import base64
from io import BytesIO
import seaborn as sn
#Global data
global data
global graph

#Other Functions

#Function to generate random colours
def hexColour():
    r = lambda: random.randint(0,255)
    s='#%02X%02X%02X' % (r(),r(),r())
    return s
#Function to create file head and send it to front end
def fileHead(df):
    df=df.fillna("null")
    displayData=df.values.tolist()[0:5]
    metadata=list(df.columns)
    responseData={"data":displayData,"metaData":metadata}
    responseData=json.dumps(responseData,ensure_ascii=True,allow_nan=True)
    return responseData
def organizePlots(l):
    colslist=[]
    rowslist=[]
    k=0
    for x in l:
        if k%2==0:
            if len(rowslist) !=0:
                colslist.append(rowslist)
            rowslist=[]
        rowslist.append(x)
        k=k+1
    colslist.append(rowslist)
    return colslist
#Flask Code
app = Flask(__name__)
CORS(app)

@app.route('/trainHead', methods=['GET'])
def trainHead():
    global data
    return fileHead(data)


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
@app.route('/getAttributes',methods=['GET'])
def graphType():
    global data
    global graph
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
    graph = request.form['graph']
    y_attr=request.form['y_attr']
    x_attr=request.form['x_attr']
    x_attr=x_attr.split(',')
    mapping=""
    if(str(data[y_attr].dtype)=="object"):
        le = preprocessing.LabelEncoder()
        data[y_attr]=le.fit_transform(data[y_attr])
        le_name_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
        mapping+="\tMAPPING"
        for x in le_name_mapping:
            mapping+=" "+x+":"+str(le_name_mapping[x])



    if graph=="bar":
        p = figure(plot_width=1000, plot_height=1000)
        xlabel=""
        for x in x_attr:
            p.vbar(x=data[x], width=1.5, bottom=0,top=data[y_attr],color=hexColour(),legend=x)
            xlabel+=" "
            xlabel+=x
        p.xaxis.axis_label =xlabel
        p.yaxis.axis_label = y_attr
        t = Title()
        t.text = "graph:" + graph + " x:" + x + mapping
        p.title = t
        show(p)
        return "SUCCESS"
    if graph=="scatter":
        p = figure(plot_width=600, plot_height=600)
        for x in x_attr:
            p.scatter(data[x], data[y_attr], marker="x",line_color=hexColour(), fill_color=hexColour(), fill_alpha=0.5, size=12,legend=x)
        t = Title()
        t.text = "graph:" + graph + " x:" + str(x_attr)+mapping
        p.title = t
        show(p)
        return "SUCCESS"
    if graph=="line":
        l=[]
        for x in x_attr:
            p = figure(plot_width=600, plot_height=600)
            p.line(data[x], data[y_attr],color=hexColour(),legend=x)
            p.xaxis.axis_label =x
            p.yaxis.axis_label = y_attr
            #title = graph + " " + xlabel + " " + y_attr
            t=Title()
            t.text ="graph:"+graph+" x:"+x+ mapping
            p.title = t
            l.append(p)
        print(organizePlots(l))
        show(gridplot(organizePlots(l)))
        return "SUCCESS"
    if graph=="correlation":

        plt.figure()
        ax=sn.heatmap(data.corr(), square=True, cmap='RdYlGn')
        plt.subplots_adjust(bottom=0.30)
        fig=ax.get_figure()
        tmpfile = BytesIO()
        plt.savefig(tmpfile, format='png')

        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        html = '<html><body> '+ '<img src=\'data:image/png;base64,{}\'>'.format(encoded) + '</body></html>'
        with open('correlation map.html', 'w') as f:
            f.write(html)
        webbrowser.open_new_tab('correlation map.html')
        return "SUCCESS"
    
        
        
        



    
app.run(host='127.0.0.1', port= 5001)

