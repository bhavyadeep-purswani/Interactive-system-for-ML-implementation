from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.svm import SVC, SVR

from modules.utilities import strToBool

#function to create MachineLearning Model
def createModel(algorithm,hyperparameters):
    # TODO: You already have the alogrithm names stored in a list in Constants reference from that rather than using String literals
    if algorithm=="Linear Regression":
        fit_intercept= strToBool(hyperparameters["fit_intercept"])
        mod=LinearRegression(fit_intercept=fit_intercept)
    if algorithm=="Random Forrest Classifier":
        n_estimators=int(float(hyperparameters["n_estimators"]))
        max_depth=int(float(hyperparameters["max_depth"]))
        min_samples_split=float(hyperparameters["min_samples_split"])
        min_samples_leaf=float(hyperparameters["min_samples_leaf"])
        max_features=hyperparameters["max_features"]
        if(max_features not in ["auto" ,"log2" ,"sqrt"] ):
            max_features=int(float(max_features))
        max_leaf_nodes=int(float(hyperparameters["max_leaf_nodes"]))
        mod=RandomForestClassifier(n_estimators=n_estimators,max_depth=max_depth,min_samples_split=min_samples_split,min_samples_leaf=min_samples_leaf,max_features=max_features,max_leaf_nodes=max_leaf_nodes)
    if algorithm=="Random Forrest Regressor":
        n_estimators=int(float(hyperparameters["n_estimators"]))
        max_depth=int(float(hyperparameters["max_depth"]))
        min_samples_leaf=float(hyperparameters["min_samples_leaf"])
        max_features=hyperparameters["max_features"]
        if(max_features not in ["auto" ,"log2" ,"sqrt"] ):
            max_features=int(float(max_features))
        max_leaf_nodes=int(float(hyperparameters["max_leaf_nodes"]))
        mod=RandomForestRegressor(n_estimators=n_estimators,max_depth=max_depth,min_samples_leaf=min_samples_leaf,max_features=max_features,max_leaf_nodes=max_leaf_nodes)
    if algorithm=="KNeighbors Classifier":
        n_neighbors=int(float(hyperparameters["n_neighbors"]))
        weights=hyperparameters["weights"]
        algorithmK=hyperparameters["algorithm"]
        leaf_size=int(float(hyperparameters["leaf_size"]))
        mod=KNeighborsClassifier(n_neighbors=n_neighbors,weights=weights,algorithm=algorithmK,leaf_size=leaf_size)
    if algorithm=="Logistic Regression":
        penalty=hyperparameters["penalty"]
        dual= strToBool(hyperparameters["dual"])
        c=float(hyperparameters["c"])
        max_iter=int(float(hyperparameters["max_iter"]))
        mod=LogisticRegression(penalty=penalty,dual=dual,c=c,max_iter=max_iter)
    if algorithm=="SVM Classification":
        C=int(float(hyperparameters["C"]))
        kernel=hyperparameters["kernel"]
        degree=int(float(hyperparameters["degree"]))
        gamma=hyperparameters["gamma"]
        max_iter=int(float(hyperparameters["max_iter"]))
        mod=SVC(C=C,degree=degree,kernel=kernel,gamma=gamma,max_iter=max_iter)
    if algorithm=="SVM Regression":
        C=int(float(hyperparameters["C"]))
        kernel=hyperparameters["kernel"]
        degree=int(float(hyperparameters["degree"]))
        gamma=hyperparameters["gamma"]
        max_iter=int(float(hyperparameters["max_iter"]))
        mod=SVR(C=C,degree=degree,kernel=kernel,gamma=gamma,max_iter=max_iter)
    if algorithm=="Gaussian Naive Bayes":
        var_smoothing=float(hyperparameters["var_smoothing"])
        mod=GaussianNB(var_smoothing=var_smoothing)
    if algorithm=="Neural Network Classification":
        hidden_layer_sizes=int(float(hyperparameters["hidden_layer_sizes"]))
        hidden_layer_sizes=tuple((hidden_layer_sizes,))
        activation=hyperparameters["activation"]
        alpha=float(hyperparameters["alpha"])
        learning_rate=hyperparameters["learning_rate"]
        max_iter=int(float(hyperparameters["max_iter"]))
        mod=MLPClassifier(hidden_layer_sizes=hidden_layer_sizes,activation=activation,alpha=alpha,learning_rate=learning_rate,max_iter=max_iter)
    if algorithm=="Neural Network Regression":
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
def evaluateModel(modFit,X,y):
    y_pred=modFit.predict(X)
    accuracy=accuracy_score(y, y_pred)*100
    tup=list(precision_recall_fscore_support(y, y_pred,average="micro"))
    result={
            "accuracy":accuracy,
            "precision_recall_fscore_support":tup}
    return result

#Function to predict the prediction File
def predict(modFit,testData):
    predictedData=modFit.predict(testData)
    return predictedData