# Usage: 
#  python boolean_term_doc_matrix.py --data_path ..\data\ --query "'Suarez' AND 'Messi' OR 'Barcelona'" 


import os
import numpy as np
import re
import argparse
import time
from collections import deque
from utils import OPERATORS, isOperator


def load_data_from_directory(path: str):

    lst_contents = []
    file_paths = os.listdir(path)
    
    print("[INFO] Loading content from documents ...")
    for file in file_paths:
        path_file = os.path.join(path, file)
        with open(path_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lst_contents.append(content)
    
    print(" ---> Loaded {} documents".format(len(file_paths)))

    return lst_contents, file_paths


def build_dictionary(data):
    
    dictionary = set()

    print("[INFO] Extracting terms from the documents ...")
    # Loop through all documents
    for document in data:

        lst_words = document.split()
        # Loop through all words in the document
        for word in lst_words:
            dictionary.add(word)

    print(" ---> The size of dictionary is {}".format(len(dictionary)))
    return dictionary


def build_term_document_matrix(dictionary, data, file_paths):
    
    term_document_matrix = []
    index_documents = dict()
    index_words = dict()

    print("[INFO] Building term-document matrix ...")
    # Loop through all documents
    i = 0
    for document in data:

        vector = []        
        j = 0

        # Loop through all words
        for word in dictionary:
            if word in document:
                vector.append(1)
            else:
                vector.append(0)
            
            index_words[word] = j
            j += 1

        term_document_matrix.append(np.array(vector))

        index_documents[i] = file_paths[i]
        i += 1

    print(" ---> Done building the matrix !")

    return np.array(term_document_matrix).T, index_documents, index_words


def process_query(matrix, index_documents, index_words, query: str):
    
    number_documents = len(index_documents)

    # Tokenizing the input query, the archived result are terms
    query_words = re.findall(r"'(\w+)'", query)
    operators = [term for term in query.split() if term in OPERATORS]

    lst_vectors = []
    # Loop through all words to get its representation vector 
    for word in query_words:
        try:
            representation_vector = matrix[index_words[word], :]
        except: # If the word is not exsit on the dictionary
            representation_vector = np.zeros(number_documents, dtype=np.int32)   # Assign the zero vector    
        
        lst_vectors.append(representation_vector)
        print(" \t---> The representation of {:12s} is {}".format(word, representation_vector))



    i = 0
    result = lst_vectors[0]
    for vector in lst_vectors[1:]:
        if operators[i] == "NOT":
            # Process unary operator
        else:
            # Process binary operators
            result = OPERATORS[operators[i]](result, vector)
        i += 1

    # i = 0
    # previous_operator = None
    # result = lst_vectors[0]
    # for operator in operators:
    #     if operator == "NOT":
    #         # Process unary operator
    #         current_result = OPERATORS[]
    #     else:
    #         # Process binary operators
    #         result = OPERATORS[operators[i]](result, vector)
    #     i += 1


    # Retrieval the indices of documents
    indices = np.where(result)
    
    # Display the query result 
    print("[INFO] Query result ...")
    for index in indices:
        print(" - {}".format(index_documents[i]))

    return indices


def main(args):

    # Load data from the directory
    lst_contents, file_paths = load_data_from_directory(path=args['data_path'])
    
    # Build word dictionary from loaded data
    dictionary = build_dictionary(lst_contents)

    # Build term-document matrix
    matrix, index_documents, index_words = build_term_document_matrix(dictionary=dictionary, data=lst_contents, file_paths=file_paths)

    # Process the query 
    indices = process_query(matrix=matrix, index_documents=index_documents, index_words=index_words, query=args["query"])
    


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Boolean Retrieval using Term-Document Matrix method.')
    parser.add_argument('--data_path', '-d', required=True, help="The directory store documents")
    parser.add_argument('--query', '-q', required=True, help="The query need processing.")
    parser.add_argument('--number_display', '-n', default=10, help="The max number of document display.")
    args = vars(parser.parse_args())

    main(args)