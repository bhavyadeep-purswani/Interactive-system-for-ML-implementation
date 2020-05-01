import json

#constants
#UPLOAD_FOLDER = '.\data' #For windows
UPLOAD_FOLDER='data' #Ubuntu
ALLOWED_EXTENSIONS = {'csv'}
GRAPH_URL = 'http://127.0.0.1:5001/loadGraphData'
HYPERPARAMETERSFILE="resources/hyperparamters.json"


class Algorithms:
    Random_Forrest_Classifier="Random Forrest Classifier"
    KNeighbors_Classifier="KNeighbors Classifier"
    SVM_Classification="SVM Classification"
    Gaussian_Naive_Bayes="Gaussian Naive Bayes"
    Neural_Network_Classification="Neural Network Classification"
    Neural_Network_Regression = "Neural Network Regression"
    Random_Forrest_Regressor = "Random Forrest Regressor"
    SVM_Regression = "SVM Regression"
    Linear_Regression = "Linear Regression"
    @staticmethod
    def getClassificationAlgorithms():
        CALGORITHMS = ["Random Forrest Classifier", "KNeighbors Classifier", "SVM Classification",
                       "Gaussian Naive Bayes", "Neural Network Classification"]
        return CALGORITHMS
    @staticmethod
    def getRegressionAlgorithms():
        RALGORITHMS = ["Random Forrest Regressor", "Linear Regression", "SVM Regression", "Neural Network Regression"]
        return RALGORITHMS



class NullValuePredictions:
    DROP_ROWS = "dropRows"
    DROP_COLUMN = "dropColumn"
    FILL_MEAN = "fillMean"
    FILL_MEDIAN = "fillMedian"
    FILL_CUSTOM = "fillCustom"
    NO_PREDICTION = "noPrediction"


class ProblemType:
    CLASSIFICATION = "Classification"
    REGRESSION = "Regression"

