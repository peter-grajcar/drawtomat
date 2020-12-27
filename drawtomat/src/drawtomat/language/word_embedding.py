import fasttext
import numpy as np

class WordEmbedding:
    """

    """
    def __init__(self, word_list: 'list'):
        self.word_list = word_list
        self.model = fasttext.load_model("resources/fasttext/conceptual-captions-fasttext.model")

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
            score = cos_sim(self.model[w], self.model[word])
            if maximum is None or maximum["score"] < score:
                maximum = {"word": w, "score": score}
        return maximum["word"]


def cos_sim(a: 'np.ndarray', b: 'np.ndarray') -> 'float':
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
