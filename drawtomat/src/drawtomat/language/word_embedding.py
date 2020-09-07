import gensim


class WordEmbedding:
    """

    """
    def __init__(self, word_list: 'list'):
        self.word_list = word_list
        self.model = gensim.models.KeyedVectors.load("resources/conceptualcaptions/train.wv.model")

    def most_similar_word(self, word: 'str') -> str:
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
            score = max([self.model.similarity(w1=word, w2=v) for v in w.split()])
            if maximum is None or maximum["score"] < score:
                maximum = {"word": w, "score": score}
        return maximum["word"]
