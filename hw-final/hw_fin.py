import math as m

testcase = [
    '',
    ',',
    'Crock Pot Pasta Never boil pasta again',
    'Pasta Pomodoro Fresh ingredients Parmesan to taste'
]

class CountVectorizer:
    def __init__(self):
        self._vocab = {}
        self._count_matrix = []

    def get_feature_names(self):
        features = [''] * len(self._vocab)
        for word, ind in self._vocab.items():
            features[ind] = word
        return features

    def fit(self, corpus):
        index = 0
        for text in corpus:
            words = text.split()
            for word in words:
                word = word.lower()
                if word not in self._vocab:
                    self._vocab[word] = index
                    index += 1
        return self

    def transform(self, corpus):
        self._count_matrix = []
        for text in corpus:
            words = text.split()
            count = [0] * len(self._vocab)
            for word in words:
                word = word.lower()
                if word in self._vocab:
                    count[self._vocab[word]] += 1
            self._count_matrix.append(count)
        return self._count_matrix

    def fit_transform(self, corpus):
        self.fit(corpus)
        return self.transform(corpus)


class TfIdfTransformer:
    def __init__(self):
        self._idf_vector = []

    def tf_transform(self, _count_matrix):
        tf_matrix = []
        for i in range(len(_count_matrix)):
            matrix = [0] * len(_count_matrix[i])
            total = sum(_count_matrix[i])
            if total == 0:
                tf_matrix.append([0] * len(_count_matrix[i]))
                continue
            for j in range(len(matrix)):
                matrix[j] = round(_count_matrix[i][j] / total, 3)
            tf_matrix.append(matrix)
        return tf_matrix


    def idf_transform(self, count_matrix):
        n_docs = len(count_matrix)
        n_features = len(count_matrix[0])
        df_j = [0] * n_features

        for i in range(n_docs):
            for j in range(n_features):
                if count_matrix[i][j] > 0:
                    df_j[j] += 1

        self._idf_vector = []
        for df in df_j:
            idf_value = m.log((n_docs + 1) / (df + 1)) + 1
            self._idf_vector.append(round(idf_value, 1))

        return self._idf_vector

    def fit_transform(self, count_matrix):
        self.idf_transform(count_matrix)
        tf = self.tf_transform(count_matrix)
        tf_idf = []
        for i in range(len(count_matrix)):
            vec = [0] * len(count_matrix[0])
            for j in range(len(count_matrix[0])):
                vec[j] = round(tf[i][j] * self._idf_vector[j], 3)
            tf_idf.append(vec)

        return tf_idf

class TfIdfVectorizer(CountVectorizer):
    def __init__(self):
        super().__init__()
        self.transformer = TfIdfTransformer()

    def fit_transform(self, corpus):
        count_matrix = super().fit_transform(corpus)
        tfidf_matrix = self.transformer.fit_transform(count_matrix)
        return tfidf_matrix
