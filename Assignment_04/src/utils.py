import os
import argparse
import numpy as np



def get_argument():
	parser = argparse.ArgumentParser(description='TF - IDF method for vector space model.')
	parser.add_argument('--data_path', '-d', default='../data/', help='The path of all documents.')
	parser.add_argument('--query', '-q', default='Barca Messi', help='The query question from user.')
	parser.add_argument('--numbers', '-N', default=5, help='The number of results display.')
	return vars(parser.parse_args())


def load_data_from_directory(path):
	
	file_paths = os.listdir(path)
	data = []

	# Loop through all files in directory
	for file in file_paths:
		with open(os.path.join(path, file), 'r', encoding='utf8') as f:
			data.append(f.read().split())

	return np.array(data), file_paths


def build_dictionary(lst_contents):

	dictionary = set()
	for content in lst_contents:
		dictionary.update(content)

	return dictionary



