import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder


# function to standardize data
def standardizeData(data, standardizeType, scaler=None):
    if scaler == None:
        if (standardizeType == "standard"):
            scaler = StandardScaler()
            data = scaler.fit_transform(data)
        else:
            scaler = MinMaxScaler()
            data = scaler.fit_transform(data)
        return data, scaler
    else:
        if (standardizeType == "standard"):
            data = scaler.transform(data)
        else:
            data = scaler.transform(data)
        return data


# Function to check if data contains Null values
def containsNull(data):
    return any(data.isnull())


def getNumberOfNullValues(column: pd.Series) -> int:
    return pd.isnull(column).values.tolist().count(True)


# Function to fill the data with custom value
def fillCustom(data, value):
    data.fillna(value, inplace=True)
    return data


# Function to fill the data with Mean Value
def fillMean(data):
    data.fillna(data.mean(), inplace=True)
    return data


# Function to fill the data with Median Value
def fillMedian(data):
    data.fillna(data.median(), inplace=True)
    return data


# Function to fill the data with most common value
def fillMostCommon(data):
    data.fillna(data.mode().iloc[0], inplace=True)
    return data


# Function to drop rows that have null value corresponding to a column
def dropNullRows(data, referenceColumn):
    data.dropna(subset=[referenceColumn], inplace=True)
    return data


# Function to forward fill the data
def fillForward(data):
    data.fillna(method="ffill", inplace=True)
    return data


# Function to backward fill the data
def fillBackward(data):
    data.fillna(method="bfill", inplace=True)
    return data


# Function to Label Encode Column
def labelEncode(data, enc):
    data = data.applymap(str)
    if enc == None:
        enc = preprocessing.LabelEncoder()
        data = enc.fit_transform(data)
        return data, enc
    else:
        data = enc.transform(data)
        return data


def fix_unknown_values(data, le_dict,labelEncoder):
    unique = list(set(data))
    maxval= max(list(le_dict.values()))
    for x in unique:
        if x not in le_dict:
            maxval = maxval + 1
            le_dict[x] = maxval
    return [le_dict[k] for k in data]

# Function to One hot Encode Column
def oneHotEncode(data, enc):
    data = data.applymap(str)
    if enc == None:
        enc = OneHotEncoder(handle_unknown='ignore')
        enc.fit(data)
        data = enc.transform(data).toarray()
        df = pd.DataFrame(data, columns=enc.categories_)
        return df, enc
    else:
        enc.fit(data)
        data = enc.transform(data).toarray()
        df = pd.DataFrame(data, columns=enc.categories_)
        return df
