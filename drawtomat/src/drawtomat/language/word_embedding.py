import gensim


class WordEmbedding:
    """

    """
    def __init__(self, word_list: 'list'):
        self.word_list = word_list
        self.model = gensim.models.KeyedVectors.load("resources/conceptualcaptions/train.wv.model")
        # self.model = gensim.models.KeyedVectors.load_word2vec_format("resources/fasttext/wiki-news-300d-1M.vec")

    def get_similarity(self, word1: 'str', word2: 'str') -> 'float':
        try:
            return self.model.similarity(w1=word1, w2=word2)
        except KeyError:
            return 0

    def most_similar_word(self, word: 'str') -> 'str':
        """
        Finds most similar word from the word_list.

        Parameters
        ----------
        word

        Returns
        -------
        str
            most similar word
        """
        maximum = None
        for w in self.word_list:
            score = max([self.get_similarity(word, v) for v in w.split()])
            if maximum is None or maximum["score"] < score:
                maximum = {"word": w, "score": score}
        return maximum["word"]
