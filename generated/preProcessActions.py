from modules.preprocess import *
import server
import pandas as pd
def preprocess(params):
	dataset=params['dataset']
	for x in dataset.columns:
		dataset[x]=fillMostCommon(dataset[x])
	return dataset