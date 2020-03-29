##
# Predicts the Null Value Handler for given column
##


import pandas as pd
from PredictionLayer import Constants, Utils, getPredictedProblemType


def getPredictedNullValueHandler(column: pd.Series) -> str:
    problemType = getPredictedProblemType(column)
    nullValuePercentage = getNullValuePercentage(column)
    if nullValuePercentage < Constants.NullValuePredictor.DROP_ROW_BENCHMARK_PERCENTAGE:
        return Constants.NullValuePredictions.DROP_ROWS
    elif nullValuePercentage > Constants.NullValuePredictor.DROP_COLUMN_BENCHMARK_PERCENTAGE:
        return Constants.NullValuePredictions.DROP_COLUMN
    elif problemType == Constants.ProblemType.CLASSIFICATION and nullValuePercentage > Constants.NullValuePredictor.FILL_CUSTOM_BENCHMARK_PERCENTAGE:
        return Constants.NullValuePredictions.FILL_CUSTOM
    elif problemType == Constants.ProblemType.REGRESSION:
        if checkForOutliers(column):
            return Constants.NullValuePredictions.FILL_MEDIAN
        else:
            return Constants.NullValuePredictions.FILL_MEAN
    return Constants.NullValuePredictions.NO_PREDICTION


def getNullValuePercentage(column: pd.Series) -> float:
    return (Utils.getNumberOfNullValues(column)/len(column)) * 100


def checkForOutliers(column: pd.Series) -> bool:
    column = pd.Series.dropna(column, axis=0)
    q1 = Utils.getQ1(column)
    q3 = Utils.getQ3(column)
    iqr = q3 - q1
    return any(((column < (q1 - 1.5 * iqr)) | (column > (q3 + 1.5 * iqr))).values.tolist())

