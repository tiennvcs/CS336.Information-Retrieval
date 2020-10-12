from utils import get_argument, load_data_from_directory, build_dictionary
import numpy as np


def calculate_tf_weights(lst_contents, words):

	rows = len(words)
	columns = len(lst_contents)

	TF_matrix = np.zeros((rows, columns), dtype=np.float32)

	for i, word in enumerate(words):
		for j, content in enumerate(lst_contents):
			TF_matrix[i, j] = content.count(word) / len(content)

	return TF_matrix


def calculate_idf_weights(TF):

	IDF = 1 + np.log(TF.shape[1]/np.sum(TF != 0, axis=1))

	return np.array([IDF]).T


def main(args):

	# Bước 1: Load data from directory
	lst_contents, file_paths = load_data_from_directory	(args['data_path'])

	# Bước 2: Build dictionary
	vocal = build_dictionary(lst_contents)

	# Bước 3: Calculate the TF weights for each document.
	TF_matrix = calculate_tf_weights(lst_contents, vocal)

	# Bước 4: Calculate the IDF weights
	IDF = calculate_idf_weights(TF_matrix)

	# Bước 5: Calculate the TF-IDF
	TF_IDF = TF_matrix * IDF

	# Bước 6: Make query
	qwords = args['query'].split()
	qTF = calculate_tf_weights([qwords], vocal)
	qTF_IDF = qTF * IDF

	# Bước 6: Calculate the similarity between qTF_IDF and TF_IDF
	dists = np.linalg.norm(TF_IDF - qTF_IDF, axis=0)

	# Bước 7: Ranking and display result
	ranked_result = np.argsort(dists)

	print("The ranking result matching with query "{}"".format(args['query']))

	N = int(args['numbers'])
	for index in ranked_result[0: N]:
		print(file_paths[index])

if __name__ == '__main__':
	args = get_argument()
	main(args)