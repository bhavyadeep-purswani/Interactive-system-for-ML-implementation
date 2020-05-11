from modules.preprocess import *
import server
import pandas as pd
def preprocess(params):
	dataset=params['dataset']
	dataset = standardizeData(dataset,'standard',params['stan'])
	return dataset