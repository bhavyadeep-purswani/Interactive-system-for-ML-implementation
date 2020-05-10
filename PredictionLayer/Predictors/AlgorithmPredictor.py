import json
import os
import threading

import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.svm import SVC, SVR

from PredictionLayer import Constants
from PredictionLayer import Utils


def predictAlgorithm(X_train: pd.DataFrame, X_test: pd.DataFrame, Y_train: pd.DataFrame, Y_test: pd.DataFrame,  problemType: str) -> str:
    hyperparameterList = json.loads(
        open(str(os.path.abspath(Constants.AlgorithmPredictor.HYPERPARAMTERES_FILE)), "r").read())
    accuracies = {}
    threads = []
    if problemType == Constants.ProblemType.CLASSIFICATION:
        algorithmList = Constants.AlgorithmPredictor.CALGORITHMS
    else:
        algorithmList = Constants.AlgorithmPredictor.RALGORITHMS
    for algorithm in algorithmList:
        thread = threading.Thread(target=getAccuracy,
                                  args=(algorithm, hyperparameterList, X_train, X_test, Y_train, Y_test, accuracies, problemType))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    maxAccuracy = None
    algorithmMaxAccuracy = ""
    if problemType == Constants.ProblemType.CLASSIFICATION:
        for algorithm in accuracies:
            print(algorithm, accuracies[algorithm])
            if maxAccuracy is None or accuracies[algorithm] >= maxAccuracy:
                maxAccuracy = accuracies[algorithm]
                algorithmMaxAccuracy = algorithm
    else:
        for algorithm in accuracies:
            print(algorithm, accuracies[algorithm])
            if maxAccuracy is None or accuracies[algorithm] <= maxAccuracy:
                maxAccuracy = accuracies[algorithm]
                algorithmMaxAccuracy = algorithm
    return algorithmMaxAccuracy


def getAccuracy(algorithm, hyperparameterList, X_train, X_test, Y_train, Y_test, accuracies, problemType):
    hyperparams = getHyperParamsForAlgorithm(algorithm, hyperparameterList)
    mod = createModel(algorithm, hyperparams, hyperparameterList)
    modFit = createModelFit(mod, X_train, Y_train)
    accuracy = evaluateModel(modFit, X_test, Y_test, problemType)
    accuracies[algorithm] = accuracy


# function to create MachineLearning Model
def createModel(algorithm, hyperparameters, HYPERPARAMETERS):
    if algorithm == Algorithms.Linear_Regression:
        fit_intercept = Utils.strToBool(hyperparameters["fit_intercept"])
        mod = LinearRegression(fit_intercept=fit_intercept)
    if algorithm == Algorithms.Random_Forrest_Classifier:
        n_estimators = int(float(hyperparameters["n_estimators"]))
        if hyperparameters["max_depth"] == "None" or hyperparameters["max_depth"] == "none":
            max_depth = None
        else:
            max_depth = int(float(hyperparameters["max_depth"]))
        min_samples_split = int(float(hyperparameters["min_samples_split"]))
        min_samples_leaf = int(float(hyperparameters["min_samples_leaf"]))
        max_features = hyperparameters["max_features"]
        if (max_features not in HYPERPARAMETERS[Algorithms.Random_Forrest_Classifier]["max_features"]["options"]):
            max_features = int(float(max_features))
        if hyperparameters["max_leaf_nodes"] == "None" or hyperparameters["max_leaf_nodes"] == "none":
            max_leaf_nodes = None
        else:
            max_leaf_nodes = int(float(hyperparameters["max_leaf_nodes"]))
        mod = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth,
                                     min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf,
                                     max_features=max_features, max_leaf_nodes=max_leaf_nodes)
    if algorithm == Algorithms.Random_Forrest_Regressor:
        n_estimators = int(float(hyperparameters["n_estimators"]))
        if hyperparameters["max_depth"] == "None" or hyperparameters["max_depth"] == "none":
            max_depth = None
        else:
            max_depth = int(float(hyperparameters["max_depth"]))
        min_samples_leaf = int(float(hyperparameters["min_samples_leaf"]))
        if min_samples_leaf == int(min_samples_leaf):
            min_samples_leaf = int(min_samples_leaf)
        max_features = hyperparameters["max_features"]
        if max_features not in HYPERPARAMETERS[Algorithms.Random_Forrest_Regressor]["max_features"]["options"]:
            max_features = int(float(max_features))
        if hyperparameters["max_leaf_nodes"] == "None" or hyperparameters["max_leaf_nodes"] == "none":
            max_leaf_nodes = None
        else:
            max_leaf_nodes = int(float(hyperparameters["max_leaf_nodes"]))
        mod = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, min_samples_leaf=min_samples_leaf,
                                    max_features=max_features, max_leaf_nodes=max_leaf_nodes)
    if algorithm == Algorithms.KNeighbors_Classifier:
        n_neighbors = int(float(hyperparameters["n_neighbors"]))
        weights = hyperparameters["weights"]
        algorithmK = hyperparameters["nearest neighbors algorithm"]
        leaf_size = int(float(hyperparameters["leaf_size"]))
        mod = KNeighborsClassifier(n_neighbors=n_neighbors, weights=weights, algorithm=algorithmK, leaf_size=leaf_size)
    if algorithm == Algorithms.SVM_Classification:
        C = int(float(hyperparameters["C"]))
        kernel = hyperparameters["kernel"]
        degree = int(float(hyperparameters["degree"]))
        gamma = hyperparameters["gamma"]
        if gamma not in HYPERPARAMETERS[Algorithms.SVM_Classification]["gamma"]["options"]:
            gamma = int(float(hyperparameters["gamma"]))
        max_iter = int(float(hyperparameters["max_iter"]))
        mod = SVC(C=C, degree=degree, kernel=kernel, gamma=gamma, max_iter=max_iter)
    if algorithm == Algorithms.SVM_Regression:
        C = int(float(hyperparameters["C"]))
        kernel = hyperparameters["kernel"]
        degree = int(float(hyperparameters["degree"]))
        gamma = hyperparameters["gamma"]
        if gamma not in HYPERPARAMETERS[Algorithms.SVM_Regression]["gamma"]["options"]:
            gamma = int(float(hyperparameters["gamma"]))
        max_iter = int(float(hyperparameters["max_iter"]))
        mod = SVR(C=C, degree=degree, kernel=kernel, gamma=gamma, max_iter=max_iter)
    if algorithm == Algorithms.Gaussian_Naive_Bayes:
        var_smoothing = float(hyperparameters["var_smoothing"])
        mod = GaussianNB(var_smoothing=var_smoothing)
    if algorithm == Algorithms.Neural_Network_Classification:
        hidden_layer_sizes = int(float(hyperparameters["hidden_layer_sizes"]))
        hidden_layer_sizes = tuple((hidden_layer_sizes,))
        activation = hyperparameters["activation"]
        alpha = float(hyperparameters["alpha"])
        learning_rate = hyperparameters["learning_rate"]
        max_iter = int(float(hyperparameters["max_iter"]))
        mod = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, activation=activation, alpha=alpha,
                            learning_rate=learning_rate, max_iter=max_iter)
    if algorithm == Algorithms.Neural_Network_Regression:
        hidden_layer_sizes = int(float(hyperparameters["hidden_layer_sizes"]))
        hidden_layer_sizes = tuple((hidden_layer_sizes,))
        activation = hyperparameters["activation"]
        alpha = float(hyperparameters["alpha"])
        learning_rate = hyperparameters["learning_rate"]
        max_iter = int(float(hyperparameters["max_iter"]))
        mod = MLPRegressor(hidden_layer_sizes=hidden_layer_sizes, activation=activation, alpha=alpha,
                           learning_rate=learning_rate, max_iter=max_iter)
    return mod


# Function to fit and evaluate model
def createModelFit(mod, X, y):
    modFit = mod.fit(X, y)
    return modFit


def evaluateModel(modFit,X,y, problemType):
    y_pred=modFit.predict(X)
    if problemType == Constants.ProblemType.CLASSIFICATION:
        accuracy=accuracy_score(y, y_pred)*100
    else:
        accuracy = mean_squared_error(y, y_pred)
    return accuracy


def getHyperParamsForAlgorithm(algorithm: str, hyperparameterList: dict) -> dict:
    defaultParams = {}
    for param in hyperparameterList[algorithm]:
        defaultParams[param] = hyperparameterList[algorithm][param]["default"]
    return defaultParams


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