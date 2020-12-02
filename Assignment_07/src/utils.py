import glob2
import os
import numpy as np
from nltk.tokenize import regexp_tokenize 



def load_data_from_directory(path):
    
    X = []
    y = []

    labels = os.listdir(path)
    LABEL2CATEGORY = dict()
    file_paths = []

    for i, label in enumerate(labels):
        LABEL2CATEGORY[i] = label
        basedir = os.path.join(path, label)
        doc_files = os.listdir(basedir)
        file_paths += [os.path.join(basedir, doc_file) for doc_file in doc_files]
        for doc_file in doc_files[:10]:
            with open(os.path.join(basedir, doc_file), 'r') as f:
                content = f.read()
            words = [word.lower() for word in set(regexp_tokenize(content, "[\w']+"))]
            X.append(words)

        y += [i]*len(doc_files[:10])

    return np.array(X), np.array(y), LABEL2CATEGORY, file_paths


def build_dictionary(docs, dict_size):

    word_lst = list()
    vocabulary = list()

    for words in docs:
        for word in words:
            word_lst.append(word)
            if vocabulary.count(word) == 0:
                vocabulary.append(word)
    return set(np.random.choice(vocabulary, dict_size))


def matrix_term_document(args):

	def calculate_tf_weights(lst_contents, vocab):

		rows = len(vocab)
		columns = len(lst_contents)

		TF_matrix = np.zeros((rows, columns), dtype=np.float32)

		for i, term in enumerate(vocab):
			for j, content in enumerate(lst_contents):
				TF_matrix[i, j] = content.count(term) / len(content)

		return TF_matrix


	def calculate_idf_weights(TF):

		IDF = 1 + np.log(TF.shape[1]/np.sum(TF != 0, axis=1))

		return np.array([IDF]).T


	# Bước 1: Load data from directory
	print("[Step 1] Loading data from directory {}".format(args['data_path']))
	lst_contents, labels, LABEL2CATEGORY, file_paths = load_data_from_directory(args['data_path'])

	# Bước 2: Build dictionary
	print("[Step 2] Build dictionary from word documents ...")
	vocab = build_dictionary(lst_contents, dict_size=2000)

	# Bước 3: Calculate the TF weights for each document.
	print("[Step 3] Calculate the TF weighting...")
	TF_matrix = calculate_tf_weights(lst_contents, vocab)

	# Bước 4: Calculate the IDF weights
	print("[Step 4] Calculate IDF weighting ...")
	IDF = calculate_idf_weights(TF_matrix)

	# Bước 5: Calculate the TF-IDF
	print("[Step 5] Calculate TF-IDF weighting ...")
	TF_IDF = TF_matrix * IDF

	return IDF, TF_IDF, labels, LABEL2CATEGORY, file_paths