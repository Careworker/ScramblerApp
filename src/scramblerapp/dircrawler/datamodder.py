import csv

class DataModder:

	@classmethod
	def parsecsv(self, filepath: str, colnames: list) -> dict:
		# returns {'column_name1': ['item1','item2','item3'], ...}
		if len(colnames) <= 0: return {}
		result = {}
		for col in colnames: result[col] = []

		try:
			with open(filepath, 'r') as f:
				file = csv.DictReader(f)
				keys = file.fieldnames
				for line in file:
					for col in colnames:
						if col in keys: result[col].append(line[col])
			return result
		except:
			return {}

	@classmethod
	def createcsv(self, data: dict, outpath: str) -> dict:
		# data = {'column_name1': ['item1','item2','item3'], ...}
		keys = list(data.keys()); values = list(data.values())
		if len(keys) == 0 or len(values) == 0:
			return {'status': 400, 'message': 'Error: Input keys/values cannot be empty.'}
		max_key = max(data, key= lambda x: len(set(data[x])))
		new_data = [keys]
		try:
			for i, _ in enumerate(data[max_key]):
				row = []
				for j, _ in enumerate(keys):
					try:
						key = keys[j]
						row.append(data[key][i])
					except:
						row.append('')
				new_data.append(row)
		except:
			return {'status': 400, 'message': 'Error: Failed to parse data from input.'}

		try:
			with open(outpath, mode='w', newline='') as f:
				csv.writer(f).writerows(new_data)
			return {'status': 200, 'message': 'File created: {}'.format(outpath)}
		except:
			return {'status': 400, 'message': 'Error: Failed to write data to csv.'}

	@classmethod
	def append_col(self, column: list, filepath: str, outpath: str) -> dict:
		# column = ['column_name1','item1','item2','item3']
		new_data = []

		try:
			with open(filepath, mode='r') as f:
				file = csv.reader(f)
				for i, item in enumerate(file):
					try:
						item.append(column[i])
					except IndexError:
						item.append('N/A')
					new_data.append(item)
		except:
			return {'status': 400, 'message': 'Error: Failed to parse data from input.'}

		try:
			with open(outpath, mode='w', newline='') as f:
				csv.writer(f).writerows(new_data)
			return {'status': 200, 'message': 'File created: {}'.format(outpath)}
		except:
			return {'status': 400, 'message': 'Error: Failed to write data to csv.'}
