from modules.preprocess import *
import server
import pandas as pd
def preprocess(params):
	dataset=params['dataset']
	dataset.drop(['Name', 'Pclass', 'PassengerId', 'Ticket'],axis=1,inplace=True)
	return dataset