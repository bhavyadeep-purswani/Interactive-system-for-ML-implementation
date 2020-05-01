import pandas as pd
import PredictionLayer

dataset = pd.read_csv("../datasets/weatherww2/Summary of Weather.csv")
print(PredictionLayer.getPredictedProblemType(dataset['MaxTemp']))
print(len(dataset['MaxTemp'].unique()), len(dataset))
print(len(dataset['MaxTemp'].unique())/len(dataset))
#
# data = pd.DataFrame([1, 0, 1, 0, 0, 1, 1, 1, None])
# print(PredictionLayer.getPredictedNullValueHandler(data[0]))