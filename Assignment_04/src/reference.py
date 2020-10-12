import glob
import numpy as np

# Buoc 1: Doc du lieu tu thu muc 'data'
def load_data_in_a_directory(data_path):
    file_paths = glob.glob(data_path)
    lst_contents = []
    for file_path in file_paths:
        f = open(file_path, 'r')
        str = f.read()
        words = str.replace('"', '').replace('.', '').replace("'","").split()
        #words = set(words)
        lst_contents.append(words)
    return (lst_contents, file_paths)

# Doc noi dung cua tung file txt
# va xay dung tap "dictionary" chua danh sach cac tu
def build_dictionary(contents):
    dictionary = set()
    for content in contents:
        dictionary.update(content)
    return dictionary

# Buoc 2: Tinh trong so TF cho tung van ban
# trong thu muc 'data'

def compute_tf_weighting(contents, vocab):
    TF = np.zeros((len(vocab), len(contents)))
    for i, word in enumerate(vocab):
        for j, content in enumerate(contents):
            # Dem xem word xuat hien bao nhieu lan trong content
            TF[i, j] = content.count(word)
    TF_norm = TF / np.sum(TF, axis=0)
    return TF_norm

# Buoc 3: Tinh trong IDF (toan cuc)
def compute_idf_weighting(TF):
    IDF = 1 + np.log(TF.shape[1]/np.sum(TF != 0, axis=1))
    return np.array([IDF]).T

#### MAIN #####
contents, paths = load_data_in_a_directory('../data/*.txt')
vocab = build_dictionary(contents)
TF = compute_tf_weighting(contents, vocab)
IDF = compute_idf_weighting(TF)

# Buoc 4: Tinh trong so TF-IDF
TF_IDF = TF*IDF

# Buoc 5: Nhap query va tinh trong so TF-IDF
query = "Barca"
qwords = query.split()
qTF = compute_tf_weighting([qwords], vocab)
qTF_IDF = qTF * IDF

# Buoc 6: Tinh khoang cach / do tuong dong
# Giua TF-IDF cua query va tap du lieu
dists = np.linalg.norm(TF_IDF - qTF_IDF, axis=0)

# Buoc 7: Sap xep va hien thi ket qua
print(paths)
rank = np.argsort(dists)
print(rank)
print('Van ban gan nhat voi query la: ', ' '.join(contents[rank[0]]))
print('Van ban gan thu nhi voi query la: ', ' '.join(contents[rank[1]]))
print('Van ban gan thu ba voi query la: ', ' '.join(contents[rank[2]]))