class CountVectorizer:
    def __init__(self, lowercase=True):
        self._vocabulary: list[str] = []
        self.lowercase = lowercase

    def get_feature_names(self) -> list[str]:
        """
        Безопасный геттер словаря уникальных слов для переданного массива.

        :return: list(self._vocabulary)
        """
        return list(self._vocabulary)

    def fit_transform(self, corpus) -> list[list[int]]:
        """
        Преобразует полученные строки из массива в вектор.

        :param corpus: массив передаваемых строк.
        :return: преобразованные векторы подсчета слов по индексам словаря.
        """
        for line in corpus:
            for word in line.split():
                if self.lowercase:
                    word = word.lower()
                if word not in self._vocabulary:
                    self._vocabulary.append(word)

        lines_transform = []
        for line in corpus:
            words = line.split()
            if self.lowercase:
                words = [word.lower() for word in words]
            words_transform = [0] * len(self._vocabulary)
            for word in words:
                words_transform[self._vocabulary.index(word)] += 1
            lines_transform.append(words_transform)
        return lines_transform
