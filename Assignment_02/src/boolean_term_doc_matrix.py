# Usage: python 
import os
import glob
import numpy as np
import re
import argparse


def parse_query(query: str):
    words = None
    operators = None
    return (words, operators)


def load_data_from_directory(path: str):

    file_paths = os.listdir(path)
    for file in file_paths:
        print(file)
        
    lst_contents = None
    return lst_contents, file_paths


def build_dictionary(data):
    dictionary = None
    return dictionary


def build_term_document_matrix(dictionary, data):
    term_document_matrix = None
    return term_document_matrix


def query():
    answers = None
    return answers


def main(args):

    # Load data from the directory
    print(args['data_path'])

    lst_contents, file_paths = load_data_from_directory(path=args['data_path'])



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Boolean Retrieval using Term-Document Matrix method.')
    parser.add_argument('--data_path', '-d', required=True, help="The directory store documents")
    parser.add_argument('--query', '-q', required=True, help="The query need processing.")
    parser.add_argument('--number_display', '-n', default=10, help="The max number of document display.")
    args = vars(parser.parse_args())

    main(args)