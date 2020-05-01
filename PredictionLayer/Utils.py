##
# Stores common Utilities
##
import pandas as pd
from PredictionLayer import Constants


def checkColumnContainsString(column: pd.Series) -> bool:
    return column.dtype == object


def getUniqueValueCount(column: pd.Series) -> int:
    return len(column.unique())


def getUniqueValueRatio(column: pd.Series) -> float:
    column = pd.Series.dropna(column, axis=0)
    return getUniqueValueCount(column)/len(column)


def getDataFile() -> pd.DataFrame:
    try:
        return pd.read_csv(__file__ + Constants.DataFile.NAME).drop_duplicates()
    except IOError as e:
        print(Constants.LOG_TAG + "Exception occurred while reading data file: " + str(e))
        return pd.DataFrame()


def setDataFile(df: pd.DataFrame) -> bool:
    try:
        df.to_csv(__file__ + Constants.DataFile.NAME, index=False, header=True)
        return True
    except IOError as e:
        print(Constants.LOG_TAG + "Exception occurred while writing data file: " + str(e))
        return False


def getNumberOfNullValues(column: pd.Series) -> int:
    print(Constants.LOG_TAG + "Count of null values = " + str(pd.isnull(column).values.tolist().count(True)))
    return pd.isnull(column).values.tolist().count(True)


def getQ1(column: pd.Series) -> float:
    return column.describe()["25%"]


def getQ3(column: pd.Series) -> float:
    return column.describe()["75%"]


def checkForOutliers(column: pd.Series) -> bool:
    column = pd.Series.dropna(column, axis=0)
    q1 = getQ1(column)
    q3 = getQ3(column)
    iqr = q3 - q1
    return any(((column < (q1 - 1.5 * iqr)) | (column > (q3 + 1.5 * iqr))).values.tolist())


def strToBool(s):
    if(s=="True" or s=="true" or s==True):
        return True
    else:
        return False
