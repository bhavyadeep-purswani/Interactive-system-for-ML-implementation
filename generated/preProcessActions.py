from modules.preprocess import *
import server
import pandas as pd
def preprocess(params):
	dataset=params['dataset']
	dataset['target']=targetData.values
	dataset=dropNullRows(dataset,'MSZoning')
	targetData = dataset['target']
	dataset.drop(['target'], axis = 1, inplace = True)
	dataset['LotFrontage']=fillMedian(dataset['LotFrontage'])
	dataset.drop([Alley],axis=1,inplace=True)
	dataset['target']=targetData.values
	dataset=dropNullRows(dataset,'MasVnrType')
	targetData = dataset['target']
	dataset.drop(['target'], axis = 1, inplace = True)
	dataset['target']=targetData.values
	dataset=dropNullRows(dataset,'BsmtQual')
	targetData = dataset['target']
	dataset.drop(['target'], axis = 1, inplace = True)
	dataset['target']=targetData.values
	dataset=dropNullRows(dataset,'BsmtExposure')
	targetData = dataset['target']
	dataset.drop(['target'], axis = 1, inplace = True)
	dataset['target']=targetData.values
	dataset=dropNullRows(dataset,'BsmtFinType2')
	targetData = dataset['target']
	dataset.drop(['target'], axis = 1, inplace = True)
	dataset['target']=targetData.values
	dataset=dropNullRows(dataset,'Electrical')
	targetData = dataset['target']
	dataset.drop(['target'], axis = 1, inplace = True)
	dataset['FireplaceQu']=fillCustom(dataset['FireplaceQu'],'TA')
	dataset['GarageType']=fillForward(dataset['GarageType'])
	dataset['GarageYrBlt']=fillMedian(dataset['GarageYrBlt'])
	dataset['GarageFinish']=fillForward(dataset['GarageFinish'])
	dataset['GarageQual']=fillForward(dataset['GarageQual'])
	dataset['GarageCond']=fillForward(dataset['GarageCond'])
	dataset.drop([PoolQC],axis=1,inplace=True)
	dataset.drop([Fence],axis=1,inplace=True)
	dataset.drop([MiscFeature],axis=1,inplace=True)
	for x in dataset.columns:
		dataset[x]=fillMostCommon(dataset[x])
	data = labelEncode(dataset[['MSZoning']],params['lab'+'MSZoning'])
	dataset['MSZoning']=data
	data = labelEncode(dataset[['Street']],params['lab'+'Street'])
	dataset['Street']=data
	data = labelEncode(dataset[['LotShape']],params['lab'+'LotShape'])
	dataset['LotShape']=data
	data = labelEncode(dataset[['LandContour']],params['lab'+'LandContour'])
	dataset['LandContour']=data
	data = labelEncode(dataset[['Utilities']],params['lab'+'Utilities'])
	dataset['Utilities']=data
	data = labelEncode(dataset[['LotConfig']],params['lab'+'LotConfig'])
	dataset['LotConfig']=data
	data = labelEncode(dataset[['LandSlope']],params['lab'+'LandSlope'])
	dataset['LandSlope']=data
	data = labelEncode(dataset[['Neighborhood']],params['lab'+'Neighborhood'])
	dataset['Neighborhood']=data
	data = labelEncode(dataset[['Condition1']],params['lab'+'Condition1'])
	dataset['Condition1']=data
	data = labelEncode(dataset[['Condition2']],params['lab'+'Condition2'])
	dataset['Condition2']=data
	data = labelEncode(dataset[['BldgType']],params['lab'+'BldgType'])
	dataset['BldgType']=data
	data = labelEncode(dataset[['HouseStyle']],params['lab'+'HouseStyle'])
	dataset['HouseStyle']=data
	data = labelEncode(dataset[['RoofStyle']],params['lab'+'RoofStyle'])
	dataset['RoofStyle']=data
	data = labelEncode(dataset[['RoofMatl']],params['lab'+'RoofMatl'])
	dataset['RoofMatl']=data
	data = labelEncode(dataset[['Exterior1st']],params['lab'+'Exterior1st'])
	dataset['Exterior1st']=data
	data = labelEncode(dataset[['Exterior2nd']],params['lab'+'Exterior2nd'])
	dataset['Exterior2nd']=data
	data = labelEncode(dataset[['MasVnrType']],params['lab'+'MasVnrType'])
	dataset['MasVnrType']=data
	data = labelEncode(dataset[['ExterQual']],params['lab'+'ExterQual'])
	dataset['ExterQual']=data
	data = labelEncode(dataset[['ExterCond']],params['lab'+'ExterCond'])
	dataset['ExterCond']=data
	data = labelEncode(dataset[['Foundation']],params['lab'+'Foundation'])
	dataset['Foundation']=data
	data = labelEncode(dataset[['BsmtQual']],params['lab'+'BsmtQual'])
	dataset['BsmtQual']=data
	data = labelEncode(dataset[['BsmtCond']],params['lab'+'BsmtCond'])
	dataset['BsmtCond']=data
	data = labelEncode(dataset[['BsmtExposure']],params['lab'+'BsmtExposure'])
	dataset['BsmtExposure']=data
	data = labelEncode(dataset[['BsmtFinType1']],params['lab'+'BsmtFinType1'])
	dataset['BsmtFinType1']=data
	data = labelEncode(dataset[['BsmtFinType2']],params['lab'+'BsmtFinType2'])
	dataset['BsmtFinType2']=data
	data = labelEncode(dataset[['Heating']],params['lab'+'Heating'])
	dataset['Heating']=data
	data = labelEncode(dataset[['HeatingQC']],params['lab'+'HeatingQC'])
	dataset['HeatingQC']=data
	data = labelEncode(dataset[['CentralAir']],params['lab'+'CentralAir'])
	dataset['CentralAir']=data
	data = labelEncode(dataset[['Electrical']],params['lab'+'Electrical'])
	dataset['Electrical']=data
	data = labelEncode(dataset[['KitchenQual']],params['lab'+'KitchenQual'])
	dataset['KitchenQual']=data
	data = labelEncode(dataset[['Functiol']],params['lab'+'Functiol'])
	dataset['Functiol']=data
	data = labelEncode(dataset[['FireplaceQu']],params['lab'+'FireplaceQu'])
	dataset['FireplaceQu']=data
	data = labelEncode(dataset[['GarageType']],params['lab'+'GarageType'])
	dataset['GarageType']=data
	data = labelEncode(dataset[['GarageFinish']],params['lab'+'GarageFinish'])
	dataset['GarageFinish']=data
	data = labelEncode(dataset[['GarageQual']],params['lab'+'GarageQual'])
	dataset['GarageQual']=data
	data = labelEncode(dataset[['GarageCond']],params['lab'+'GarageCond'])
	dataset['GarageCond']=data
	data = labelEncode(dataset[['PavedDrive']],params['lab'+'PavedDrive'])
	dataset['PavedDrive']=data
	data = labelEncode(dataset[['SaleType']],params['lab'+'SaleType'])
	dataset['SaleType']=data
	data = labelEncode(dataset[['SaleCondition']],params['lab'+'SaleCondition'])
	dataset['SaleCondition']=data
	dataset = standardizeData(dataset,'standard',params['stan'])
	return dataset