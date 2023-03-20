import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score 
import sys
import pickle
from sklearn.model_selection import train_test_split
import os

base_path = 'data/'
output_path = 'rforest.pkl'
initialized_model = RandomForestClassifier() # Change parameters if you like. make sure any pkl files are deleted


def convert_decision_to_digit(decision):
	if decision == 'NO':
		return 0 
	elif decision == 'SELL':
		return 2
	else: 
		return 1 


def convert_digit_to_execute(execute_num):
	if execute_num == 0:
		return 'NO'
	else:
		return 'EXECUTE'


def convert_execute_to_digit(execute): 
	if (execute == 'NO'): 
		return 0 
	else: 
		return 1 

def convert_digit_to_execute(execute_num):
	if execute_num == 0:
		return 'NO'
	else:
		return 'EXECUTE'

def tesla_increase(dataframe): 
	dataframe['delta_Tesla63'] = dataframe['Tesla6'] - dataframe['Tesla3']
	dataframe['delta_Tesla96'] = dataframe['Tesla9'] - dataframe['Tesla6']
	dataframe.loc[dataframe['delta_Tesla63'] > 0, 'delta_Tesla63'] = 1 
	dataframe.loc[dataframe['delta_Tesla63'] < 0, 'delta_Tesla63'] = -1 
	dataframe.loc[dataframe['delta_Tesla96'] > 0, 'delta_Tesla96'] = 1 
	dataframe.loc[dataframe['delta_Tesla96'] < 0, 'delta_Tesla96'] = -1 
	return dataframe [['Value5', 'Value6', 'Minute','Day', 'delta_Tesla63', 'delta_Tesla96', 'Decision', 'EXECUTE']]

# columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'WAP', 'Count', 'Minute', 'Day', 'Month', 'Tesla3', 'Tesla6', 'Tesla9', 'Value5', 'Value6', 'Decision']
def tesla_increase_np(np_array):
	row = np_array[0]
	# 11th index - Tesla6
	# 10th index - Tesla3
	# 12th index - Tesla9 
	# 13th index - Value5 
	# 14th index - Value6 
	# 15th index - Decision
	# 7th index - Minute 
	# 8th index - Day 
	delta_tesla63 = float(row[11]) - float(row[10])
	delta_tesla96 = float(row[12]) - float(row[11])
	return np.array([[row[13], row[14], row[7],row[8], delta_tesla63, delta_tesla96, row[15]]])


def train_and_evaluate(currency):
	model = initialized_model


	data_train = pd.read_csv(base_path+currency+'_train.csv')
	data_test = pd.read_csv(base_path+currency+'_test.csv')


	data_train = pd.concat([data_train, data_test])

	# Resampling with EXECUTE
	execute = data_train[data_train['EXECUTE'] == 'EXECUTE']
	no = data_train[data_train['EXECUTE'] == 'NO']
	class_execute_over = execute.sample(int(no.shape[0]), replace=True)
	data_train = pd.concat([class_execute_over, no], axis=0)
	data_train['EXECUTE'] = data_train['EXECUTE'].apply(lambda x: convert_execute_to_digit(x))
	data_train['Decision'] = data_train['Decision'].apply(lambda x: convert_decision_to_digit(x))
	data_train = tesla_increase(data_train)


	data_train_numpy = data_train.to_numpy()
	train_x, train_y = data_train_numpy[:, :-1], data_train_numpy[:,-1]
	model.fit(train_x, train_y)

	# Test data 
	data_test['EXECUTE'] = data_test['EXECUTE'].apply(lambda x: convert_execute_to_digit(x))
	data_test['Decision'] = data_test['Decision'].apply(lambda x: convert_decision_to_digit(x))
	data_test = tesla_increase(data_test)
	data_test_numpy = data_test.to_numpy()
	test_x, test_y = data_test_numpy[:, :-1], data_test_numpy[:, -1]
	y_pred = model.predict(test_x)
	tn, fp, fn, tp = confusion_matrix(test_y, y_pred).ravel()

	print("***** Training Dataset *****")
	print("true negative: ", tn)
	print("false positive: ", fp)
	print("false negative: ", fn)
	print("true positive: ", tp)
	print("accuracy_score: ", accuracy_score(test_y, y_pred, normalize=True))
	with open(output_path, 'wb') as output_file:
		pickle.dump(model, output_file)


if __name__ == '__main__':
	function_name = sys.argv[1]
	if function_name == 'train':
		currency = sys.argv[2]
		train_and_evaluate(currency)
	elif function_name == 'predict':
		model = None 
		with open(output_path, 'rb') as file:
			model = pickle.load(file)
		open_val = sys.argv[2]
		high = sys.argv[3]
		low = sys.argv[4]
		close = sys.argv[5]
		volume = sys.argv[6]
		wap = sys.argv[7]
		count = sys.argv[8]
		minute = sys.argv[9]
		day = sys.argv[10]
		month = sys.argv[11]
		tesla3 = sys.argv[12]
		tesla6 = sys.argv[13]
		tesla9 = sys.argv[14]
		value5 = sys.argv[15]
		value6 = sys.argv[16]
		decision = sys.argv[17]
		row_vector = [[open_val, high, low, close, volume, wap, count, minute, day, month, tesla3, tesla6, tesla9, value5, value6, decision]]
		row_vector[0][-1] = convert_decision_to_digit(row_vector[0][-1])
		np_row = np.array(row_vector)
		np_row = tesla_increase_np(np_row)
		decision_execution_num = model.predict(np_row)
		decision_execution = convert_digit_to_execute(decision_execution_num[0])
		print(decision_execution)
	elif function_name == 'model_performance':
		currency = sys.argv[2]
		model = None 
		with open(output_path, 'rb') as file:
			model = pickle.load(file)
		data_test = pd.read_csv(base_path+currency+'_test.csv')
		data_test['EXECUTE'] = data_test['EXECUTE'].apply(lambda x: convert_execute_to_digit(x))
		data_test['Decision'] = data_test['Decision'].apply(lambda x: convert_decision_to_digit(x))
		data_test_numpy = data_test.to_numpy()
		test_x, test_y = data_test_numpy[:, :-1], data_test_numpy[:, -1]
		y_pred = model.predict(test_x)
		tn, fp, fn, tp = confusion_matrix(test_y, y_pred).ravel()
		print("***** Performance *****")
		print("true negative: ", tn)
		print("false positive: ", fp)
		print("false negative: ", fn)
		print("true positive: ", tp)
		print("accuracy_score: ", accuracy_score(test_y, y_pred, normalize=True))