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


def getNumberOfNullValues(column: pd.Series) -> int:
    return pd.isnull(column).values.tolist().count(True)


def getQ1(column: pd.Series) -> float:
    return column.describe()["25%"]


def getQ3(column: pd.Series) -> float:
    return column.describe()["75%"]