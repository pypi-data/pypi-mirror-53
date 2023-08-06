import re

class TextGrouper:


	def _calculate_limit(self, text, limit, chars_per_error): 
		"""Calculate max Levenshtein distance based on provided limit. """

		cpe_limit = (1 + len(text) // chars_per_error)
		if limit:
			return min(limit, cpe_limit)
		else:
			return cpe_limit


	def levenshtein_distance(self, s1, s2, ignore_list=[]):
		"""Calculates Leveshtein distance between two strings. 
		
		Levenshtein distance between two words is the minimum number of 
		single-character edits (i.e. insertions, deletions, or substitutions) 
		required to change one word into the other.

		Comparison is case sensitive.
		
		Arguments:

			s1, s2 - Strings to be compared. Leading and trailing spaces are ignored.

		
			ignore_list - List of patterns to be ignored when comparing strings. 
				For example, with ignore_list=['\\d'], distance between 'word123' 
				and '123word45' is 0. Default value is empty list.

		"""

		# Remove irrelevant patterns
		for pattern in ignore_list:
			s1 = re.sub(pattern, '', s1)
			s2 = re.sub(pattern, '', s2)

		# Strip after replace - possible multiple spaces left
		s1 = s1.strip()
		s2 = s2.strip()

		if len(s1) < len(s2):
			return self._levenshtein_distance(s2, s1, [])

		if len(s2) == 0:
			return len(s1)

		previous_row = range(len(s2) + 1)
		for i, c1 in enumerate(s1):
			current_row = [i + 1]
			for j, c2 in enumerate(s2):
				insertions = previous_row[j + 1] + 1 
				deletions = current_row[j] + 1     
				substitutions = previous_row[j] + (c1 != c2)
				current_row.append(min(insertions, deletions, substitutions))
			previous_row = current_row

		return previous_row[-1]

	
	def group(self, entities, similarity_limit=None, chars_per_error=8, ignore_list=[], key=None):
		"""Group entities elements in subgroups.
		
		Arguments:

			entities -- List of elements to be divided into groups.

			similarity_limit -- Maximum Levenshtein distance between words 
				to be consiedered as similar. The default value is calculated 
				as 1 + (1 for each chars_per_error characters).
		
			chars_per_error -- Number of characters per 1 error allowed. Levenshtein distance
				is considered as a number of errors. The default value is 8 (1 error is allowed
				for each 8 characters). 

			ignore_list -- List of patterns to ignore when calculating text similarity
				For example, with ignore_list=['\\d'], 'word123' and '123word45' are 
				considered equal. 

			key -- Function of one argument that is used to extract comparison 
				key from each element in iterable (for example, key=str.lower). 
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

		# Create a matrix of distance between each of the elements. 
		# Each row represent corresponding entities element, with
		# elements as pairs (distance_between_element_x, element_x_index) 
		distance_matrix = [[(0,x) for x in range(entities_size)] for y in range(entities_size)]

		# Create array of relation. Each element represent entities element
		# as a tuple (index, relation_index, similar_elements_count).
		# Array is used to decide subgroup "leads" - elements based on which 
		# are other elements grouped.
		relation_array = []

		# Calculate relation for each two of the entities_elements
		for i in range(entities_size):
			s1 = key(entities[i]) if key else entities[i]

			if i < entities_size-1:
				j = i + 1
				while j < len(entities):
					s2 = key(entities[j]) if key else entities[j]

					# Calculate distance and write distance_matrix row i
					distance = self._levenshtein_distance(s1, s2, ignore_list)
					distance_matrix[i][j] = (distance,j)
					distance_matrix[j][i] = (distance,i)
					j += 1

			# Calculate relation_index for current element as the sum of 
			# distance between its similar elements divided by similar
			# elements count.
			similar_count = 0
			similar_distance_sum = 0
			for k in range(len(entities)):
				word_rel_distance = distance_matrix[i][k][0]

				limit = self._calculate_limit(s1, similarity_limit, chars_per_error)
				if k!=i and word_rel_distance <= limit:
					similar_count += 1
					similar_distance_sum += word_rel_distance

			# If element has similar elements, write it in relation_array to be
			# considered as a "subgroup lead".
			if similar_count != 0:
				relation_index = similar_distance_sum / similar_count
				relation_array.append((i, relation_index, similar_count))


		# Sort relation_array elements by relation_index and similar count respectively.
		# Smaller relation_index represent more similarity to the other elements.
		relation_array = sorted(relation_array, key=lambda x: (x[1], -x[2]))

		# Group elements into groups based on relation_array
		groups = []
		grouped_indexes = []

		for relation_array_element in relation_array:
			new_group = []
			group_lead_index = relation_array_element[0]

			# If element is already grouped, skip to next
			if group_lead_index in grouped_indexes:
				continue

			# Append group lead do a new_group
			grouped_indexes.append(group_lead_index)
			new_group.append(entities[group_lead_index])

			# Append every element similar to the group lead to a new_group
			for distance_matrix_element in distance_matrix[group_lead_index]:
				element_index = distance_matrix_element[1]
				if element_index == group_lead_index or element_index in grouped_indexes:
					continue
				limit = self._calculate_limit(s1, similarity_limit, chars_per_error)
				if distance_matrix_element[0] <= limit:
					new_group.append(entities[element_index])
					grouped_indexes.append(element_index)

			groups.append(new_group)
 	
 		# Append all remaining elements to separate subgroups
		for remaining_element_index in range(entities_size):
			if remaining_element_index not in grouped_indexes:
				groups.append([entities[remaining_element_index]])

		return groups
