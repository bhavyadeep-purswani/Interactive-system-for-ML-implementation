import json

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.svm import SVC, SVR

from modules.constants import HYPERPARAMETERSFILE, Algorithms, ProblemType
from modules.utilities import strToBool


#function to create MachineLearning Model
def createModel(algorithm,hyperparameters):
    HYPERPARAMETERS = json.loads(open(HYPERPARAMETERSFILE, "r").read())
    if algorithm==Algorithms.Linear_Regression:
        fit_intercept= strToBool(hyperparameters["fit_intercept"])
        mod=LinearRegression(fit_intercept=fit_intercept)
    if algorithm==Algorithms.Random_Forrest_Classifier:
        n_estimators=int(float(hyperparameters["n_estimators"]))
        if hyperparameters["max_depth"] == "None" or hyperparameters["max_depth"] =="none":
            max_depth=None
        else:
            max_depth=int(float(hyperparameters["max_depth"]))
        min_samples_split=int(float(hyperparameters["min_samples_split"]))
        min_samples_leaf=int(float(hyperparameters["min_samples_leaf"]))
        max_features=hyperparameters["max_features"]
        if(max_features not in HYPERPARAMETERS[Algorithms.Random_Forrest_Classifier]["max_features"]["options"]  ):
            max_features=int(float(max_features))
        if hyperparameters["max_leaf_nodes"] == "None" or hyperparameters["max_leaf_nodes"] =="none":
            max_leaf_nodes = None
        else:
            max_leaf_nodes = int(float(hyperparameters["max_leaf_nodes"]))
        mod=RandomForestClassifier(n_estimators=n_estimators,max_depth=max_depth,min_samples_split=min_samples_split,min_samples_leaf=min_samples_leaf,max_features=max_features,max_leaf_nodes=max_leaf_nodes)
    if algorithm==Algorithms.Random_Forrest_Regressor:
        n_estimators=int(float(hyperparameters["n_estimators"]))
        if hyperparameters["max_depth"] == "None" or hyperparameters["max_depth"] == "none":
            max_depth = None
        else:
            max_depth = int(float(hyperparameters["max_depth"]))
        min_samples_leaf=int(float(hyperparameters["min_samples_leaf"]))
        if min_samples_leaf == int(min_samples_leaf):
            min_samples_leaf = int(min_samples_leaf)
        max_features=hyperparameters["max_features"]
        if max_features not in HYPERPARAMETERS[Algorithms.Random_Forrest_Regressor]["max_features"]["options"]:
            max_features=int(float(max_features))
        if hyperparameters["max_leaf_nodes"] == "None" or hyperparameters["max_leaf_nodes"] == "none":
            max_leaf_nodes = None
        else:
            max_leaf_nodes = int(float(hyperparameters["max_leaf_nodes"]))
        mod=RandomForestRegressor(n_estimators=n_estimators,max_depth=max_depth,min_samples_leaf=min_samples_leaf,max_features=max_features,max_leaf_nodes=max_leaf_nodes)
    if algorithm==Algorithms.KNeighbors_Classifier:
        n_neighbors=int(float(hyperparameters["n_neighbors"]))
        weights=hyperparameters["weights"]
        algorithmK=hyperparameters["nearest neighbors algorithm"]
        leaf_size=int(float(hyperparameters["leaf_size"]))
        mod=KNeighborsClassifier(n_neighbors=n_neighbors,weights=weights,algorithm=algorithmK,leaf_size=leaf_size)
    if algorithm==Algorithms.SVM_Classification:
        C=int(float(hyperparameters["C"]))
        kernel=hyperparameters["kernel"]
        degree=int(float(hyperparameters["degree"]))
        gamma=hyperparameters["gamma"]
        if gamma not in HYPERPARAMETERS[Algorithms.SVM_Classification]["gamma"]["options"]:
            gamma=int(float(hyperparameters["gamma"]))
        max_iter=int(float(hyperparameters["max_iter"]))
        mod=SVC(C=C,degree=degree,kernel=kernel,gamma=gamma,max_iter=max_iter)
    if algorithm==Algorithms.SVM_Regression:
        C=int(float(hyperparameters["C"]))
        kernel=hyperparameters["kernel"]
        degree=int(float(hyperparameters["degree"]))
        gamma=hyperparameters["gamma"]
        if gamma not in HYPERPARAMETERS[Algorithms.SVM_Regression]["gamma"]["options"]:
            gamma=int(float(hyperparameters["gamma"]))
        max_iter=int(float(hyperparameters["max_iter"]))
        mod=SVR(C=C,degree=degree,kernel=kernel,gamma=gamma,max_iter=max_iter)
    if algorithm==Algorithms.Gaussian_Naive_Bayes:
        var_smoothing=float(hyperparameters["var_smoothing"])
        mod=GaussianNB(var_smoothing=var_smoothing)
    if algorithm==Algorithms.Neural_Network_Classification:
        print(hyperparameters["hidden_layer_sizes"],type(hyperparameters["hidden_layer_sizes"]))
        hidden_layer_sizes=int(float(hyperparameters["hidden_layer_sizes"]))
        hidden_layer_sizes=tuple((hidden_layer_sizes,))
        activation=hyperparameters["activation"]
        alpha=float(hyperparameters["alpha"])
        learning_rate=hyperparameters["learning_rate"]
        max_iter=int(float(hyperparameters["max_iter"]))
        mod=MLPClassifier(hidden_layer_sizes=hidden_layer_sizes,activation=activation,alpha=alpha,learning_rate=learning_rate,max_iter=max_iter)
    if algorithm==Algorithms.Neural_Network_Regression:
        hidden_layer_sizes=int(float(hyperparameters["hidden_layer_sizes"]))
        hidden_layer_sizes=tuple((hidden_layer_sizes,))
        activation=hyperparameters["activation"]
        alpha=float(hyperparameters["alpha"])
        learning_rate=hyperparameters["learning_rate"]
        max_iter=int(float(hyperparameters["max_iter"]))
        mod=MLPRegressor(hidden_layer_sizes=hidden_layer_sizes,activation=activation,alpha=alpha,learning_rate=learning_rate,max_iter=max_iter)
    return mod

#Function to fit and evaluate model
def createModelFit(mod,X,y):
    modFit=mod.fit(X,y)
    return modFit

#Function to evaluate model
def evaluateModel(modFit,X,y, problemType):
    y_pred=modFit.predict(X)
    if problemType == ProblemType.CLASSIFICATION:
        accuracy = accuracy_score(y, y_pred)*100
    else:
        accuracy = mean_squared_error(y, y_pred)
    return accuracy


#Function to predict the prediction File
def predict(modFit,testData):
    predictedData=modFit.predict(testData)
    return predictedData