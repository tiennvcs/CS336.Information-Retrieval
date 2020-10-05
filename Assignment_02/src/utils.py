import numpy as np
import argparse
import re


OPERATORS = {
    'AND': np.logical_and,
    'OR': np.logical_or,
    'NOT': np.logical_not,
    'XOR': np.logical_xor,
}


def pre_processUnaryOperation(matrix, index_documents, index_words, terms):

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
	
	print("[INFO] Preprocess unary operator ...")
	new_terms = []
	vector_length = len(index_documents)
	n = len(terms)

	i = 0
	while i < n:
		print("\t", i, end=" ")
		if terms[i] == "NOT":
			j = i # j = 6
			while terms[j] == "NOT":
				j += 1
			j -= 1 # j = 6
			if (j - i + 1) % 2 == 0:
				vector = matrix[index_words[terms[j+1]]]
			else:
				try:
					vector = np.logical_not(matrix[index_words[terms[j+1]]]).astype(int)   
				except:
					vector = np.ones(vector_length, dtype=np.int32)

			new_terms.append(vector)

			print("The representation of {} word is {}".format(terms[i:j+2], vector))

			i = j + 1
		else:
			if terms[i] not in OPERATORS:
				try:
					vector = matrix[index_words[terms[i]]]
				except:
					vector = np.zeros(vector_length, dtype=np.int32)
				new_terms.append(vector)
				print(vector)
			else:
				new_terms.append(terms[i])
				print(terms[i])
		i += 1

	return new_terms
