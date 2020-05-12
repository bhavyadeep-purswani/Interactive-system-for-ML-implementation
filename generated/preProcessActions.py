from modules.preprocess import *
import server
import pandas as pd
def preprocess(params):
	dataset=params['dataset']
	dataset=dropNullRows(dataset,'Geography')
	dataset['Balance']=fillMean(dataset['Balance'])
	dataset.drop(['RowNumber', 'CustomerId', 'Surname'],axis=1,inplace=True)
	for x in dataset.columns:
		dataset[x]=fillMostCommon(dataset[x])
	df=oneHotEncode(dataset[['Geography']],params['one'+'Geography'])
	dataset = dataset.drop(columns='Geography')
	dataset = pd.concat([dataset, df], axis=1)
	df=oneHotEncode(dataset[['Gender']],params['one'+'Gender'])
	dataset = dataset.drop(columns='Gender')
	dataset = pd.concat([dataset, df], axis=1)
	for x in dataset.columns:
		dataset[x]=fillMostCommon(dataset[x])
	dataset = standardizeData(dataset,'standard',params['stan'])
	dataset = standardizeData(dataset,'standard',params['stan'])
	return dataset