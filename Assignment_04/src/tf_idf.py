from utils import get_argument, load_data_from_directory, build_dictionary
import numpy as np
import time


def matrix_term_document(args):

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

	print("The ranking result matching with query {}".format(args['query']))

	N = int(args['numbers'])
	for index in ranked_result[0: N]:
		print(file_paths[index])


def inverted_index(args):

	def calculate_tf_weights(lst_contents, words):

		rows = len(words)
		columns = len(lst_contents)

		TF_word_dict = dict()

		for word in words:
			docs = list()
			for j, content in enumerate(lst_contents):
				count = content.count(word)
				if count != 0:
					docs.append((j, count/len(content)))

			TF_word_dict[word] = docs

		return TF_word_dict


	def calculate_idf_weights(TF_word_dict, file_paths):

		number_of_docs = len(file_paths)

		IDF = np.zeros(len(TF_word_dict))

		# IDF = 1 + np.log(len(file_paths)/np.sum(TF_word_dict != 0, axis=1))
		i = 0
		for word, docs in TF_word_dict.items():
			idf = 1 + np.log(number_of_docs/len(docs))
			IDF[i] = idf
			i += 1

		return np.array([IDF]).T


	def calculate_TF_IDF(TF_word_dict, IDF, file_paths):
				
		TF_matrix = np.zeros((len(TF_word_dict), len(file_paths)), dtype=np.float32)

		for i, word in enumerate(TF_word_dict):
			for i, pair in enumerate(TF_word_dict[word]):
				TF_matrix[i, pair[0]] = pair[1]
		
		return TF_matrix * IDF


	# Bước 1: Load data from directory
	lst_contents, file_paths = load_data_from_directory	(args['data_path'])

	# Bước 2: Build dictionary
	vocal = build_dictionary(lst_contents)

	# Bước 3: Calculate the TF weights for each document.
	TF_word_dict = calculate_tf_weights(lst_contents, vocal)

	# Bước 4: Calculate the IDF weights
	IDF = calculate_idf_weights(TF_word_dict, file_paths)

	# Bước 5: Calculate the TF-IDF
	TF_IDF = calculate_TF_IDF(TF_word_dict, IDF, file_paths)
	
	# Bước 6: Make query
	qwords = args['query'].split()
	qTF = calculate_tf_weights([qwords], vocal)
	qTF_IDF = calculate_TF_IDF(qTF, IDF, file_paths)

	# Bước 6: Calculate the similarity between qTF_IDF and TF_IDF
	dists = np.linalg.norm(TF_IDF - qTF_IDF, axis=0)

	# Bước 7: Ranking and display result
	ranked_result = np.argsort(dists)

	print("The ranking result matching with query {}".format(args['query']))

	N = int(args['numbers'])
	for index in ranked_result[0: N]:
		print(file_paths[index])


if __name__ == '__main__':
	args = get_argument()
	

	start_time = time.time()

	if args['method'] == 'matrix':
		matrix_term_document(args)
		print("\nThe execution time of query is {}".format(time.time() - start_time))
	elif args['method'] == 'inverted':
		inverted_index(args)
		print("\nThe execution time of query is {}".format(time.time() - start_time))
	else:
		print("The invalid method ! Let try again !")
		exit(0)