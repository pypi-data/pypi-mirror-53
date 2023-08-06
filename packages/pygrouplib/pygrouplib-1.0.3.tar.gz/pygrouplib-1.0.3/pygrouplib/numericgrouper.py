class NumericGrouper:


	def _get_diffs_and_groups(self, entities, groups, key):
		"""Process difference array and calculate groups in not provided"""

		entities_size = len(entities)

		# Calculate entities difference
		diff_list = []
		for i in range(entities_size):
			if i == 0: 
				diff_list.append(0)
				continue

			if key:
				diff = abs(key(entities[i]) - key(entities[i-1]))
			else:
				diff = abs(entities[i] - entities[i-1])

			diff_list.append(diff)
		
		# If groups number is provided, return diff_list and groups
		if groups:
			return diff_list, groups

		# Calculate number of groups based on entites difference
		else:
			groups = 1
			last_diff = 0

			for i in range(len(diff_list)):
				if i < 2: continue
				
				if diff_list[i] > diff_list[i-1]:
					groups += 1

			return diff_list, groups


	def group(self, entities, groups=None, key=None):
		"""Groups elements in groups subgroups
		
		Arguments:

			entities -- List of elements to be divided into groups.
			
			groups -- Number of resulting subgroups. The default 
				value is None, in which case it is calculated based on
				provided values.

			key -- Function of one argument that is used to extract comparison 
				key from each element in iterable (for example, key=lambda x: x['value']). 
				The default value is None (compare the elements directly).
		"""

		# Pre-check number of elements in entities
		entities_size = len(entities)

		if entities_size == 0 or entities_size == 1:
			return [entities]
		if entities_size == 2:
			if key:
				if key(entities[0]) == key(entities[1]):
					return [entities]
				else:
					return [[v] for v in entities]
			elif entities[0] == entities[1]:
				return [entities]
			else:
				return [[v] for v in entities]


		# Sort values so they can be compared quickly
		values = sorted(entities, key=key)

		diff_list, groups = self._get_diffs_and_groups(values, groups, key)

		# Pre-check groups
		if groups > entities_size:
			raise ValueError("Groups number must be less then or equal to size of values_list")
		elif groups < 1:
			raise ValueError("Groups number must be greater than or equal to 1")
		elif groups == 1:
			return [entities]
		elif groups == entities_size:
			return [[k] for k in entities]
		
	
		# Init empty result list		
		subgroups = []

		# Init dict for storing info about elements that are the most
		# different from their predecessor
		split_data = [{'index':-1, 'diff':0}] * (groups - 1)

		# Update split data for every element using difference from its predecessor
		for i in range(len(diff_list)):
			diff = diff_list[i]
			split_data = self._update_split_data(split_data, i, diff)
		
		# split_data is sorted by diff value
		# Sort it by index to form subgroups
		split_data = sorted(split_data, key=lambda k :k['index'])
		
		# Split into subgroups - split_data contains indexes that mark 
		# starting position of each subgroup.
		# last_index is next subgroup start index
		last_index = split_data[0]['index']
		
		# Append first subgroup
		subgroups.append(values[:last_index]) 	

		for split_index in range(len(split_data)):

			if split_index == 0: continue
			
			next_index  = split_data[split_index]['index']	
			# Append subgroup
			subgroups.append(values[last_index:next_index])	
			last_index = next_index

		# Append last subgroup
		subgroups.append(values[last_index:]) 

		return subgroups


	def _update_split_data(self, data, index, diff):
		"""Updates info about subgroup starting indexes

		If diff is larger than smallest diff in data - delete 
		element with smallest diff, append new one and return 
		elements sorted by diff ascending
		"""

		if data[0]['diff'] <= diff:
			del data[0]
			data.append({'index':index, 'diff':diff})

		return sorted(data, key=lambda k :k['diff'])

