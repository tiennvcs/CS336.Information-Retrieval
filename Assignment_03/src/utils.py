import numpy as np
import argparse
import re


OPERATORS = {
    'AND': set.intersection,
    'OR': set.union,
    'XOR': set.symmetric_difference,
    'NOT': None,
}


def findUniversalSet(dictionaries, terms):

	universal = set()
	for term in terms:
		if term not in OPERATORS:
			try:
				current_set = dictionaries[term] 
			except:
				current_set = set()
			universal.update(current_set)

	#print(universal)
	return universal

def pre_processUnaryOperation(dictionaries, file_paths, terms):

	"""
	- Description: Convert the query terms into binary operators, without unary operator.

	- Arguments:
		+ matrix (np.ndarray): the term-document matrix 
		+ index_documents (dict): the dictionary container key related to the number of column of document in the term-document matrix
		+ index_words (dict): the dictionary container key related to the number of row of document in the term-document matrix
		+ terms (list): the list contains OPERATORs and OPERANDS.

	- Return values:
		+ A list container the elements contain vector and binary operators. 

	For example: 
		INPUT: ['Suarez', 'OR', 'Messi', 'AND', 'NOT, 'Barcelona']
		OUTPUT ['Suarez', 'OR', 'Messi', 'AND', 'X']
	"""
	
	vector_length = len(file_paths)
	n = len(terms)

	universalset = findUniversalSet(dictionaries=dictionaries, terms=terms)

	print("[INFO] Preprocess unary operator ...")
	new_terms = []
	
	i = 0
	while i < n:
		print("\t", i, end=" ")
		if terms[i] == "NOT":
			j = i # j = 6
			while terms[j] == "NOT":
				j += 1
			j -= 1 # j = 6
			if (j - i + 1) % 2 == 0:
				try:
					vector = dictionaries[terms[j+1]]
				except:
					vector = set()
			else:
				try:
					vector = universalset.difference(dictionaries[terms[j+1]])
				except:
					vector = universalset.copy()

			new_terms.append(vector)

			print("The representation of {} word is {}".format(terms[i:j+2], vector))

			i = j + 1
		else:
			if terms[i] not in OPERATORS:
				try:
					vector = dictionaries[terms[i]]
				except:
					vector = set()
				new_terms.append(vector)
				print(vector)
			else:
				new_terms.append(terms[i])
				print(terms[i])
		i += 1

	return new_terms
