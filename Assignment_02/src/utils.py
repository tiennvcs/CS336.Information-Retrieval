import numpy as np


OPERATORS = {
    'AND': np.logical_and,
    'OR': np.logical_or,
    'NOT': np.logical_not,
    'XOR': np.logical_xor,
}


def isOperator(term: str):
	if term in OPERATORS:
		return True
	return False 