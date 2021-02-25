import csv

import numpy as np

from drawtomat.model.composition import PhysicalObject
from drawtomat.model.composition.physical_object_scaler import PhysicalObjectScaler
from drawtomat.processor.word_embedding import WordEmbedding
from drawtomat.quickdraw import QuickDrawDataset


class QuickDrawAbsoluteObjectScaler(PhysicalObjectScaler):
    """
    A scaler which uses absolute size data.
    """

    def __init__(self, word_embedding: 'WordEmbedding' = None):
        if not word_embedding:
            self.word_embedding = WordEmbedding(QuickDrawDataset.words())
        else:
            self.word_embedding = word_embedding
        self.attrs = dict()
        with open(f"resources/quickdraw/attributes.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.attrs[row["category"]] = {
                    "default_width": float("0" + row["default_width"]),
                    "default_height": float("0" + row["default_height"]),
                }

    def scale(self, sub: 'PhysicalObject', obj: 'PhysicalObject', pred: 'str') -> 'float':
        width, height = sub.get_size()
        word = self.word_embedding.most_similar_word(sub.entity.word)
        attrs = self.attrs[word]

        if not attrs:
            return 1.0
        elif attrs["default_width"] and attrs["default_height"]:
            if attrs["default_width"] > attrs["default_height"]:
                return attrs["default_width"] / width
            else:
                return attrs["default_height"] / height
        elif attrs["default_width"]:
            return attrs["default_width"] / width
        elif attrs["default_height"]:
            return attrs["default_height"] / height

        return 1.0


class QuickDrawRelativeObjectScaler(PhysicalObjectScaler):
    """
    A scaler which sets the size relative to other object.
    """

    def __init__(self, word_embedding: 'WordEmbedding' = None):
        if not word_embedding:
            self.word_embedding = WordEmbedding(QuickDrawDataset.words())
        else:
            self.word_embedding = word_embedding

        self.words = list(QuickDrawDataset.words())
        self.indices = {}
        for i, word in enumerate(QuickDrawDataset.words()):
            self.indices[word] = i

        n = len(self.words)
        self.ratio = np.zeros(shape=(n, n, 2))
        with open(f"resources/quickdraw/attributes_relative.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                i = self.indices[row["subject"]]
                j = self.indices[row["object"]]
                self.ratio[i, j, 0] = float("0" + row["width_ratio"])
                self.ratio[i, j, 1] = float("0" + row["height_ratio"])

    def scale(self, sub: 'PhysicalObject', obj: 'PhysicalObject', pred: 'str') -> 'float':
        w1 = self.word_embedding.most_similar_word(sub.entity.word)
        w2 = self.word_embedding.most_similar_word(obj.entity.word)

        i = self.indices[w1]
        j = self.indices[w2]

        ratio_w, ratio_h = self.ratio[i, j]
        sub_w, sub_h = sub.get_size()
        obj_w, obj_h = obj.get_size()

        if obj_w > obj_h:
            return (obj_w * ratio_w) / sub_w
        else:
            return (obj_h * ratio_h) / sub_h
