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
        for doc_file in doc_files[:]:
            with open(os.path.join(basedir, doc_file), 'r') as f:
                content = f.read()
            words = [word.lower() for word in set(regexp_tokenize(content, "[\w']+"))]
            X.append(words)

        y += [i]*len(doc_files[:])

    return np.array(X), np.array(y), LABEL2CATEGORY, file_paths


if __name__ == '__main__':
