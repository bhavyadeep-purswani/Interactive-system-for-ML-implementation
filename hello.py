# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 19:33:27 2020

@author: lekha
"""


from flask import Flask,request,jsonify,make_response
import pandas as pd
from flask_cors import CORS, cross_origin
import json


#Function to display the data in tabular form 
def displayData(trainData,testData):
    displayTrainData=trainData.values.tolist()[0:5]
    displayTestData=testData.values.tolist()[0:5]
    return displayTrainData,displayTestData



#Flask Code
app = Flask(__name__)
CORS(app)
@app.route('/loadData',methods=['POST'])
def loadData():
    data = request.get_json()
    #print(data)
    trainURL=data.get('train')
    testURL=data.get('test')
    trainData=pd.read_csv(trainURL, delimiter = ',')
    #print(trainData)
    trainMetaData=list(trainData.columns)
    testData=pd.read_csv(testURL, delimiter = ',')
    testMetaData=list(trainData.columns)
    displayTrainData,displayTestData=displayData(trainData,testData)
    responseData={"trainData":displayTrainData,"testData":displayTestData,"metaData":trainMetaData}
    responseData=json.dumps(responseData)
    print(displayTrainData)
    r = make_response(responseData)
    r.mimetype = 'text/plain'
    return r
    #return jsonify(trainData=displayTrainData,
                   #testData=displayTestData,
                   #trainMetaData=trainMetaData)
    
    
@app.route('/h2')
def hello_world2():
   print ("hello")
   return data+"dd"

if __name__ == '__main__':
   app.run()