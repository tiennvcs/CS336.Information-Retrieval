import os
import glob2
import argparse

import pickle
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

from utils import matrix_term_document
        


def main(args):
    
    # set fixed random seed
    np.random.seed(18521489)

    # Convert the data to vector space
    IDF, X, y, LABEL2CATEGORY, file_paths = matrix_term_document(args)

    # Spliting data for training and evaluating
    print("[Step 6] Spliting data into training data and testing data")
    X_train, X_test, y_train, y_test = train_test_split(
                                        X.T, y, train_size=args['train_size'], 
                                        test_size=args['test_size'], 
                                        random_state=18521489)
    # Create model for training classification
    if args['method'] == 'knn':
        model = KNeighborsClassifier(n_neighbors=len(LABEL2CATEGORY))
    else:
        model = GaussianNB()
    # Training model
    print("[Step 6] Training {} model ...".format(args['method']))
    model.fit(X_train, y_train)

    # Evaluation
    print("[Step 7] Evaluating trained model")
    acc = model.score(X_test, y_test)
    print(" --> The accuracy of model is {}".format(acc))
    
    # Store model and log file
    saving_model = os.path.join('models', args['method'], str(args['train_size'])+'.pl')
    with open(saving_model, 'wb') as f:
        pickle.dump(model, f)
    saving_log = os.path.join('log', args['method'], str(args['train_size'])+'.txt')
    with open(saving_log, 'w') as f:
        f.write(str(acc)+'\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Classify documents by kNN and Naive Bayes.')
    parser.add_argument('--data_path', default='./../data/', required=True,
                        help='The data path contain documents.')
    parser.add_argument('--method', default='knn', required=True, 
                        choices=['knn', 'bayes'],
                        help='The method using classification.')
    parser.add_argument('--train_size', default=1000, type=int,
                        choices=[100, 1000, 3000, 5000, 7000, 9000, 11000, 13000, 15000],
                        help='The training size.')
    parser.add_argument('--test_size', default=5000, choices=[100, 5000], type=int,
                        help='The test size.')
    parser.add_argument('--dict_size', default=2000, type=int,
                        help='The dictionary size.')
    args = vars(parser.parse_args())

    main(args)