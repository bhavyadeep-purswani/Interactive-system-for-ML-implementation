##
# Predicts the type of Problem, Classification or Regression
##

from PredictionLayer import Utils
import pandas as pd
from PredictionLayer import Constants
from sklearn.neighbors import KNeighborsClassifier


def getPredictedProblemType(column: pd.Series) -> str:
    if Utils.checkColumnContainsString(column):
        return Constants.ProblemType.CLASSIFICATION
    uniqueRatio = Utils.getUniqueValueRatio(column)
    if len(column) <= Constants.ProblemTypePredictor.SMALL_DATASET_THRESHOLD:
        return \
            Constants.ProblemType.CLASSIFICATION if uniqueRatio <= Constants.ProblemTypePredictor.DEFAULT_MEAN_RATIO_FOR_SMALL_DATASET \
                else Constants.ProblemType.REGRESSION
    elif len(column) <= Constants.ProblemTypePredictor.MEDIUM_DATASET_THRESHOLD:
        return \
            Constants.ProblemType.CLASSIFICATION if uniqueRatio <= Constants.ProblemTypePredictor.DEFAULT_MEAN_RATIO_FOR_MEDIUM_DATASET \
                else Constants.ProblemType.REGRESSION
    dataFile = Utils.getDataFile()
    if len(dataFile) == 0:
        return \
            Constants.ProblemType.CLASSIFICATION if uniqueRatio <= Constants.ProblemTypePredictor.DEFAULT_MEAN_RATIO_FOR_LARGE_DATASET \
                else Constants.ProblemType.REGRESSION
    else:
        return predictProblemType(dataFile, uniqueRatio)


def predictProblemType(dataFile: pd.DataFrame, uniqueRatio: float) -> str:
    knn = KNeighborsClassifier(n_neighbors=Constants.ProblemTypePredictor.NEIGHBOUR_HYPERPARAMETER)
    knn.fit(pd.DataFrame(dataFile[Constants.DataFile.MEAN_COLUMN]), dataFile[Constants.DataFile.TYPE_COLUMN])
    return knn.predict([[uniqueRatio]])[0]


def trainProblemTypePredictor(targetColumn: pd.Series, problemType: str) -> bool:
    dataFile = Utils.getDataFile()
    row_df = pd.DataFrame({
        "Mean": round(Utils.getUniqueValueRatio(targetColumn), 5),
        "Type": problemType
    }, index=[0])
    dataFile = dataFile.append(row_df, ignore_index=True)
    dataFile = dataFile.round(decimals=5).drop_duplicates()
    return Utils.setDataFile(dataFile)
