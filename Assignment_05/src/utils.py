import os
import cv2
import numpy as np
from config import MODELS, IMAGE_SIZE
import matplotlib.pyplot as plt


os.environ['TF_CPP_MIN_LOG_LEVEL'] = "3"


def load_image_from_directory(path):
	
	file_paths = [os.path.join(path, file_path) for file_path in os.listdir(path)]

	images = list()

	for image_path in file_paths:
		image = cv2.imread(image_path)
		images.append(cv2.resize(image, IMAGE_SIZE, cv2.INTER_AREA))

	images = np.expand_dims(images, axis=0)
	return images, file_paths


def load_model(name:str):

	try:
		model = MODELS[name]
	except:
		print("The invalid model")
		exit(0)

	return model


def cosin_similarity(feature_vectors, query_vector):

	# calculate the magnitude of query vector
	len_query_vector = np.linalg.norm(query_vector)

	# Calculate the similarity between feature vectors and query vector
	similarities = []

	for feature_vector in feature_vectors:
		# Calculate the similarity of two vector
		similar = np.dot(feature_vector, query_vector)/np.linalg.norm(feature_vector)/len_query_vector
		similarities.append(similar)

	return np.array(similarities)


def display_results(query_image, file_paths, indices, number):
	
	rows = 1
	cols = number + 1

	axes = []
	fig = plt.figure(figsize=(10, 6))

	# Display the query image
	axes.append(fig.add_subplot(rows, cols, 1))
	axes[-1].set_title("Query image", fontsize=8)
	plt.axis('off')
	plt.imshow(query_image)

	for i in range(1, number+1):
		path = file_paths[indices[i-1]]
		image = cv2.imread(path)
		axes.append(fig.add_subplot(rows, cols, i+1))
		axes[-1].set_title(r"Top {} - {}".format(i, os.path.split(path)[1]), fontsize=8)
		plt.imshow(image)
		plt.axis('off')

	fig.tight_layout()
	plt.show()