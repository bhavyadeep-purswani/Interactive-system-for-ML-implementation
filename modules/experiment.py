import pandas as pd
import PredictionLayer

# dataset = pd.read_csv("../datasets/red-wine-quality/winequality-red.csv")
# print(PredictionLayer.getPredictedProblemType(dataset['quality']))
# print(len(dataset['quality'].unique())/len(dataset))

data = pd.DataFrame([1, 0, 1, 0, 0, 1, 1, 1, None])
print(PredictionLayer.getPredictedNullValueHandler(data[0]))