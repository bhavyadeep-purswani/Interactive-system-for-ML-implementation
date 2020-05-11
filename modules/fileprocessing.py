#Function to check for valid extensions
import json
import os

import pandas as pd
from flask import make_response, request
from werkzeug.utils import secure_filename

from modules.constants import UPLOAD_FOLDER


def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Function to upload a file

#Load data and convert it into dataframe
def loadData(filename,headerFlag):
    fileURL=UPLOAD_FOLDER+"/"+filename #Ubuntu
    #fileURL=UPLOAD_FOLDER+"\\"+filename #Windows
    if headerFlag == True:
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


def fullFile(df, td):
    df=df.fillna("null")
    df["Target"] = td.values
    displayData=df.values.tolist()
    metadata=list(df.columns)
    df.drop(['Target'], axis=1, inplace=True)
    responseData={"data":displayData,"metaData":metadata}
    responseData=json.dumps(responseData,ensure_ascii=True,allow_nan=True)
    r = make_response(responseData)
    r.mimetype = 'text/plain'
    return r


def fileHeadFiltered(df, columnNames):
    df=df.fillna("null")
    columns = columnNames.split(",")
    displayData=df[columns].values.tolist()[0:5]
    metadata=list(df[columns].columns)
    responseData={"data":displayData,"metaData":metadata}
    responseData=json.dumps(responseData,ensure_ascii=True,allow_nan=True)
    r = make_response(responseData)
    r.mimetype = 'text/plain'
    return r


def uploadFile(ALLOWED_EXTENSIONS,PATH):
    responseData=""
    fileName=None
    if request.method == 'POST':
        if 'file' not in request.files:
            responseData,fileName="No file part",None
        file = request.files['file']
        if file.filename == '':
            responseData,fileName="No selected file",None
        if file:
            if allowed_file(file.filename, ALLOWED_EXTENSIONS):
                filename = secure_filename(file.filename)
                file.save(os.path.join(PATH, filename))
                responseData,fileName="File uploaded successfully",filename
            else:
                responseData,fileName="Invalid Extension",None
        else:
            responseData,fileName="Error in uploading file",None
    return responseData,fileName