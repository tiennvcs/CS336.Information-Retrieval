import glob
import numpy as np
import re


def load_data_in_a_directory(data_path):
    file_paths = glob.glob(data_path)
    lst_contents = []
    for file_path in file_paths:
        f = open(file_path, 'r', encoding='utf-8')
        str = f.read()
        
        words = str.replace('"', '').replace('.', '').replace("'","").split()
        
        words = set(words)
        lst_contents.append(words)
    return (lst_contents, file_paths)

# Doc noi dung cua tung file txt
# va xay dung tap "dictionary" chua danh sach cac tu
def build_dictionary(contents):
    dictionary = set()
    for content in contents:
        dictionary.update(content)
    return dictionary

def build_term_document_matrix(dictionary, contents):
    term_doc = np.zeros((len(dictionary), len(contents)))
    for k,word in enumerate(dictionary):
        for i,content in enumerate(contents):
            if word in content:
                term_doc[k,i] = 1
    return term_doc

def process_query(term_doc, query):
    query_words = re.findall(r'"(\w+)"', query)
    # BUOC 4: Tra từng từ trong ma trận term-document
    # để lấy vector biểu diễn của từng từ
    for query_word in query_words:
        # tra vi tri cua query_word trong dictionary
        try:
            k = dictionary.index(query_word)
            word_vec = term_doc[k,:]
            print('Vector bieu dien cua ', query_word, ' la: ', word_vec)
        except:
            pass
    # BUOC 5: thực hiện phép biến đổi luận lý: AND, OR, XOR, NOT...

    # BUOC 6: hiển thị kết quả sau khi biến đổi
    return None

# MAIN

# BUOC 1: Đọc file text trong thư mục 'data'
contents, paths = load_data_in_a_directory('data/*.txt')
dictionary = build_dictionary(contents)
print('Tap cac tu: ', dictionary)
dictionary = list(dictionary)
# BUOC 2: Xây dựng ma trận term-document
term_doc_mat = build_term_document_matrix(dictionary, contents)
# BUOC 4: Nhập câu truy vấn và xử lý
query = '"Suarez" AND "Messi" OR NOT "Barcelona"'
result = process_query(term_doc_mat, query)



