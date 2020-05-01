import json
import os
import threading

import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
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
    mod = createModel(algorithm, hyperparams)
    modFit = createModelFit(mod, X_train, Y_train)
    accuracy = evaluateModel(modFit, X_test, Y_test, problemType)
    accuracies[algorithm] = accuracy


# function to create MachineLearning Model
def createModel(algorithm, hyperparameters):
    for param in hyperparameters:
        if hyperparameters[param] == "None" or hyperparameters[param] == "none":
            hyperparameters[param] = None
    if algorithm == "Linear Regression":
        fit_intercept = Utils.strToBool(hyperparameters["fit_intercept"])
        mod = LinearRegression(fit_intercept=fit_intercept)
    if algorithm == "Random Forrest Classifier":
        n_estimators = hyperparameters["n_estimators"]
        max_depth = hyperparameters["max_depth"]
        min_samples_split = hyperparameters["min_samples_split"]
        min_samples_leaf = hyperparameters["min_samples_leaf"]
        max_features = hyperparameters["max_features"]
        max_leaf_nodes = hyperparameters["max_leaf_nodes"]
        mod = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth,
                                     min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf,
                                     max_features=max_features, max_leaf_nodes=max_leaf_nodes)
    if algorithm == "Random Forrest Regressor":
        n_estimators = hyperparameters["n_estimators"]
        max_depth = hyperparameters["max_depth"]
        min_samples_leaf = hyperparameters["min_samples_leaf"]
        max_features = hyperparameters["max_features"]
        max_leaf_nodes = hyperparameters["max_leaf_nodes"]
        mod = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, min_samples_leaf=min_samples_leaf,
                                    max_features=max_features, max_leaf_nodes=max_leaf_nodes)
    if algorithm == "KNeighbors Classifier":
        n_neighbors = hyperparameters["n_neighbors"]
        weights = hyperparameters["weights"]
        algorithmK = hyperparameters["algorithm"]
        leaf_size = hyperparameters["leaf_size"]
        mod = KNeighborsClassifier(n_neighbors=n_neighbors, weights=weights, algorithm=algorithmK, leaf_size=leaf_size)
    if algorithm == "SVM Classification":
        C = hyperparameters["C"]
        kernel = hyperparameters["kernel"]
        degree = hyperparameters["degree"]
        gamma = hyperparameters["gamma"]
        max_iter = hyperparameters["max_iter"]
        mod = SVC(C=C, degree=degree, kernel=kernel, gamma=gamma, max_iter=max_iter)
    if algorithm == "SVM Regression":
        C = hyperparameters["C"]
        kernel = hyperparameters["kernel"]
        degree = hyperparameters["degree"]
        gamma = hyperparameters["gamma"]
        max_iter = hyperparameters["max_iter"]
        mod = SVR(C=C, degree=degree, kernel=kernel, gamma=gamma, max_iter=max_iter)
    if algorithm == "Gaussian Naive Bayes":
        var_smoothing = hyperparameters["var_smoothing"]
        mod = GaussianNB(var_smoothing=var_smoothing)
    if algorithm == "Neural Network Classification":
        hidden_layer_sizes = tuple(hyperparameters["hidden_layer_sizes"])
        activation = hyperparameters["activation"]
        alpha = hyperparameters["alpha"]
        learning_rate = hyperparameters["learning_rate"]
        max_iter = hyperparameters["max_iter"]
        mod = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, activation=activation, alpha=alpha,
                            learning_rate=learning_rate, max_iter=max_iter)
    if algorithm == "Neural Network Regression":
        hidden_layer_sizes = tuple(hyperparameters["hidden_layer_sizes"])
        activation = hyperparameters["activation"]
        alpha = hyperparameters["alpha"]
        learning_rate = hyperparameters["learning_rate"]
        max_iter = hyperparameters["max_iter"]
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
