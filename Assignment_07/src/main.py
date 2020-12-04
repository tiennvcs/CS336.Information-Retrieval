import os
import glob2
import argparse

import pickle
import numpy as np
from matplotlib import pyplot as plt
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
    train_sizes = [1000, 3000, 5000, 7000, 9000, 11000, 13000, 14997]

    acc_knn_lst = []
    acc_bayes_lst = []

    print(str("Training kNN and bayes model with different training sizes").center(100))
    print(str("|{:^20}|{:^20}|{:^20}|".format("training size", "knn acc", "bayes acc")).center(100))
    print(str("-"*100).center(100))

    for train_size in train_sizes:
        
        X_train, X_test, y_train, y_test = train_test_split(
                                            X.T, y, train_size=train_size, 
                                            test_size=args['test_size'], 
                                            random_state=18521489)
        # Create model for training classification
        knn_model = KNeighborsClassifier(n_neighbors=len(LABEL2CATEGORY))
        bayes_model = GaussianNB()
        
        # Training model
        knn_model.fit(X_train, y_train)
        bayes_model.fit(X_train, y_train)
        
        # Evaluation
        knn_acc = knn_model.score(X_test, y_test)
        bayes_acc = bayes_model.score(X_test, y_test)
        acc_knn_lst.append(knn_acc)
        acc_bayes_lst.append(bayes_acc)

        print(str("|{:^20}|{:^20}|{:^20}|".format(train_size, knn_acc, bayes_acc)).center(100))

    print(str("-"*100).center(100))

    fig, ax = plt.subplots(1, 1)
    ax.plot(train_sizes, acc_knn_lst, 'r--', label='KNN')
    ax.plot(train_sizes, acc_bayes_lst, 'b--', label='Bayes')

    ax.set_title("kNN and Bayes for document classification", fontsize=14)
    ax.set_xlabel("Training size", fontsize=12)
    ax.set_ylabel("Accuracy", fontsize=12)
    ax.set_xscale('log')
    ax.set_xticks(train_sizes)
    ax.set_xticklabels([str(int(train_size/1000)) for train_size in train_sizes])
    ax.legend()
    ax.legend(loc='best')
    plt.savefig(os.path.join('result', 'result.png'))
    #plt.show()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Classify documents by kNN and Naive Bayes.')
    parser.add_argument('--data_path', default='./../data/', required=True,
                        help='The data path contain documents.')
    #parser.add_argument('--method', default='knn', required=True, 
    #                    choices=['knn', 'bayes'],
    #                    help='The method using classification.')
    parser.add_argument('--train_size', default=1000, type=int,
                        #choices=[100, 1000, 3000, 5000, 7000, 9000, 11000, 13000, 15000],
                        help='The training size.')
    parser.add_argument('--test_size', default=5000, type=int,
                        #choices=[100, 5000],
                        help='The test size.')
    parser.add_argument('--vocab_size', default=2000, type=int,
                        help='The dictionary size.')
    args = vars(parser.parse_args())

    main(args)