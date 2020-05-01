##
# Stores constants used throughout Package
##

PACKAGE_RESOURCE_PATH = "PredictionLayer"


class DataFile:
    NAME = "/../data/data.csv"
    TYPE_COLUMN = "Type"
    MEAN_COLUMN = "Mean"


LOG_TAG = "PredictionLayerPackage: "


class ProblemType:
    CLASSIFICATION = "Classification"
    REGRESSION = "Regression"


class ProblemTypePredictor:
    NEIGHBOUR_HYPERPARAMETER = 3
    DEFAULT_MEAN_RATIO_FOR_SMALL_DATASET = 0.2
    DEFAULT_MEAN_RATIO_FOR_MEDIUM_DATASET = 0.1
    DEFAULT_MEAN_RATIO_FOR_LARGE_DATASET = 0.1
    SMALL_DATASET_THRESHOLD = 10
    MEDIUM_DATASET_THRESHOLD = 50


class NullValuePredictor:
    DROP_ROW_BENCHMARK_PERCENTAGE = 4
    DROP_COLUMN_BENCHMARK_PERCENTAGE = 70
    FILL_CUSTOM_BENCHMARK_PERCENTAGE = 20


class NullValuePredictions:
    DROP_ROWS = "dropNullRows"
    DROP_COLUMN = "dropColumn"
    FILL_MEAN = "fillMean"
    FILL_MEDIAN = "fillMedian"
    FILL_CUSTOM = "fillCustom"
    NO_PREDICTION = "noPrediction"


class AlgorithmPredictor:
    CALGORITHMS = ["Random Forrest Classifier", "KNeighbors Classifier", "SVM Classification",
                   "Gaussian Naive Bayes", "Neural Network Classification"]
    RALGORITHMS = ["Random Forrest Regressor", "Linear Regression", "SVM Regression", "Neural Network Regression"]
    HYPERPARAMTERES_FILE = "PredictionLayer/data/hyperparamters.json"
