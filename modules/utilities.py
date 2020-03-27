#Function to convert strToBool
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