from modules.preprocess import *
import server
import pandas as pd
def preprocess(params):
	dataset=params['dataset']
	for x in dataset.columns:
		dataset[x]=fillMostCommon(dataset[x])
	dataset['Formatted Date'] = fix_unknown_values(dataset['Formatted Date'],params['lab_dict'+'Formatted Date'],params['lab'+'Formatted Date'])
	dataset['Summary'] = fix_unknown_values(dataset['Summary'],params['lab_dict'+'Summary'],params['lab'+'Summary'])
	dataset['Precip Type'] = fix_unknown_values(dataset['Precip Type'],params['lab_dict'+'Precip Type'],params['lab'+'Precip Type'])
	dataset = standardizeData(dataset,'standard',params['stan'])
	return dataset