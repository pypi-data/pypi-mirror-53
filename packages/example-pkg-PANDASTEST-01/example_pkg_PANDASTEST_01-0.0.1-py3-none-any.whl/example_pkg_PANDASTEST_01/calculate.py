import pandas as pd

def create_pandas_table():
	data = {'col_1': [3, 2, 1, 0], 'col_2': ['a', 'b', 'c', 'd']}
	data_table = pd.DataFrame.from_dict(data)
	return (data_table)
