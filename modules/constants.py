import json

#constants
#UPLOAD_FOLDER = '.\data' #For windows
UPLOAD_FOLDER='data' #Ubuntu
ALLOWED_EXTENSIONS = {'csv'}
GRAPH_URL = 'http://127.0.0.1:5001/loadGraphData'
# TODO: Do not load files in constants file, rather just store the file name and using this file name load the file wherever required
HYPERPARAMETERS=json.loads(open("resources/hyperparamters.json","r").read())
CALGORITHMS=["Random Forrest Classifier","KNeighbors Classifier","Logistic Regression","SVM Classification","Gaussian Naive Bayes","Neural Network Classification"]
RALGORITHMS=["Random Forrest Regressor","Linear Regression","SVM Regression","Gaussian Naive Bayes","Neural Network Regression"]