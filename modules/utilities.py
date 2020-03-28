#Function to convert strToBool
from importlib import reload


def strToBool(s):
    if(s=="True" or s=="true" or s==True):
        return True
    else:
        return False

#function which returns if function contains a list
def checkForStrings(data):
    dtype=data.dtypes
    columns=[]
    for col in data.columns.values:
        val=str(dtype[col])
        if val=="string" or val=="object":
            columns.append(col)
    return columns


def fetchPreProcessData(params,preprocessingActions):
    preprocessingActions+="\n\treturn dataset"
    f=open('generated/preProcessActions.py','w+')
    f.write(preprocessingActions)
    f.close()
    #TODO: Might produce Null Pointer Exception, handle the case if Null.
    import generated.preProcessActions
    generated.preProcessActions = reload(generated.preProcessActions)
    return generated.preProcessActions.preprocess(params)


def appendAllNulls(preprocessingActions):
    preprocessingActions += "\n\tfor x in dataset.columns:\n\t\tdataset[x]=fillMostCommon(dataset[x])"
    return preprocessingActions