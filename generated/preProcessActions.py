from modules.preprocess import *
import server
import pandas as pd
def preprocess(params):
	dataset=params['dataset']
	dataset['GarageType']=fillForward(dataset['GarageType'])
	dataset['GarageFinish']=fillForward(dataset['GarageFinish'])
	dataset['GarageQual']=fillForward(dataset['GarageQual'])
	for x in dataset.columns:
		dataset[x]=fillMostCommon(dataset[x])
	dataset['Neighborhood'] = fix_unknown_values(dataset['Neighborhood'],params['lab_dict'+'Neighborhood'],params['lab'+'Neighborhood'])
	dataset['HouseStyle'] = fix_unknown_values(dataset['HouseStyle'],params['lab_dict'+'HouseStyle'],params['lab'+'HouseStyle'])
	dataset['RoofStyle'] = fix_unknown_values(dataset['RoofStyle'],params['lab_dict'+'RoofStyle'],params['lab'+'RoofStyle'])
	dataset['Foundation'] = fix_unknown_values(dataset['Foundation'],params['lab_dict'+'Foundation'],params['lab'+'Foundation'])
	dataset['CentralAir'] = fix_unknown_values(dataset['CentralAir'],params['lab_dict'+'CentralAir'],params['lab'+'CentralAir'])
	dataset['LandContour'] = fix_unknown_values(dataset['LandContour'],params['lab_dict'+'LandContour'],params['lab'+'LandContour'])
	dataset['Utilities'] = fix_unknown_values(dataset['Utilities'],params['lab_dict'+'Utilities'],params['lab'+'Utilities'])
	dataset['Condition1'] = fix_unknown_values(dataset['Condition1'],params['lab_dict'+'Condition1'],params['lab'+'Condition1'])
	dataset['SaleType'] = fix_unknown_values(dataset['SaleType'],params['lab_dict'+'SaleType'],params['lab'+'SaleType'])
	dataset['KitchenQual'] = fix_unknown_values(dataset['KitchenQual'],params['lab_dict'+'KitchenQual'],params['lab'+'KitchenQual'])
	dataset['Heating'] = fix_unknown_values(dataset['Heating'],params['lab_dict'+'Heating'],params['lab'+'Heating'])
	dataset['GarageType'] = fix_unknown_values(dataset['GarageType'],params['lab_dict'+'GarageType'],params['lab'+'GarageType'])
	dataset['GarageFinish'] = fix_unknown_values(dataset['GarageFinish'],params['lab_dict'+'GarageFinish'],params['lab'+'GarageFinish'])
	dataset['GarageQual'] = fix_unknown_values(dataset['GarageQual'],params['lab_dict'+'GarageQual'],params['lab'+'GarageQual'])
	dataset = standardizeData(dataset,'standard',params['stan'])
	return dataset