import fasttext
import numpy as np

def cos_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

class Embedding:
    def __init__(self, model_file):
        self.model = fasttext.load_model(model_file)
        self.categories = []
        with open("../../quickdraw-dataset/categories.txt") as f:
            for category in f:
                word = category.strip()
                self.categories.append((word, self.model[word]))

    def most_similar(self, word, include_similarity=False):
        sim = [(w, cos_sim(vec, self.model[word])) for (w, vec) in self.categories]
        if include_similarity:
            max(sim, key=lambda x: x[1])
        return max(sim, key=lambda x: x[1])[0]


