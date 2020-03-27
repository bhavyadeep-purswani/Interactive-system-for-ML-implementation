import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from modules.utilities import strToBool


#function to standardize data
def standardizeData(data, standardizeType,scaler=None):
    if scaler==None:
        if(standardizeType=="standard"):
            scaler = StandardScaler()
            data=scaler.fit_transform(data)
        else:
            scaler = MinMaxScaler()
            data = scaler.fit_transform(data)
        return data,scaler
    else:
        if (standardizeType == "standard"):
            scaler = StandardScaler()
            data = scaler.fit_transform(data)
        else:
            scaler = MinMaxScaler()
            data = scaler.fit_transform(data)
        return data


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
def labelEncode(data, enc):

    #data=[str(x) for x in data]
    data = data.applymap(str)
    if enc==None:
        enc = preprocessing.LabelEncoder()
        data = enc.fit_transform(data)
        return data,enc
    else:
        data = enc.fit_transform(data)
        return data


#Function to One hot Encode Column
def oneHotEncode(data, enc):
    data = data.applymap(str)
    if enc==None:
        enc = OneHotEncoder(handle_unknown='ignore')
        enc.fit(data)
        data=enc.transform(data).toarray()
        df=pd.DataFrame(data,columns=enc.categories_)
        return df, enc
    else:
        enc.fit(data)
        data = enc.transform(data).toarray()
        df = pd.DataFrame(data, columns=enc.categories_)
        return df
