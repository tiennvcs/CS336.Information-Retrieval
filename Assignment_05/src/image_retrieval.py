# Usage:
"""
	python image_retrieval.py --data_path ..\data --model VGG16 
				--query_path ..\queries\ngoctrinh.jpg 
"""

from utils import load_image_from_directory, load_model, cosin_similarity, display_results
import argparse
import os
import numpy as np
import cv2
from config import IMAGE_SIZE


def main(args):

	# Load model
	print("[INFO] Loading model {}".format(args['model']))
	model = load_model(args['model'])
	model.summary()

	# Load image from the directory
	images, file_paths = load_image_from_directory(args['data_path'])

	if not os.path.exists(os.path.join('../extracted_features', args['model'] + '.npy')):
		if not os.path.exists('../extracted_features'):
			os.mkdir('../extracted_features')

		# Extract feature
		print("[INFO] Extracting feature from image using {}".format(args['model']))
		feature_vectors = model.predict(images[0])

		# Store feature to disk	
		file_features = os.path.join('../extracted_features', '{}'.format(args['model']))
		np.save(file_features, feature_vectors)

	# Testing load feature from saving local
	print("[INFO] Loading extracted features from disk ...")
	with open(os.path.join('../extracted_features', args['model']) + '.npy', 'rb') as f:
		feature_vectors = np.load(f)

	# Load query image
	try:
		qimage = cv2.imread(args['query_path'])
		cv2.imshow('Query image', qimage)
		cv2.waitKey(0)
	except:
		print("!!! Invalid path.")
		exit(0)

	# Extract feature of query image
	qimage = np.expand_dims(cv2.resize(qimage, IMAGE_SIZE, cv2.INTER_AREA), axis=0)
	qvector = model.predict(qimage)[0]


	# Get the similarities between feature vectors and query
	print("[INFO] Calculating the similarities between feature vectors and query vector ...")
	similarities = cosin_similarity(feature_vectors, qvector)

	# Ranking base on similarities
	indices = np.argsort(similarities)[::-1]

	# Display results
	display_results(qimage[0], args['query_path'], file_paths, args['model'], indices, args['number'])



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Image retrieval with Deep feature')
	parser.add_argument('--data_path', '-d', default='../data', help='The path contain image data')
	parser.add_argument('--model', '-m', default='VGG16', 
						choices=['VGG16', 'VGG19', 'DenseNet201', 'ResNet50'], 
						help='The path contain image data')
	parser.add_argument('--query_path', '-q', default='../queries/ngoctrinh.jpg', help='The path contain image data')
	parser.add_argument('--number', '-n', type=int, default=5, help='The number of image display')

	args = vars(parser.parse_args())

	main(args)

