import csv

from drawtomat.composer.scaler.physical_object_scaler import PhysicalObjectScaler
from drawtomat.model.composition import PhysicalObject
from drawtomat.processor.word_embedding import WordEmbedding
from drawtomat.quickdraw import QuickDrawDataset


class AbsoluteObjectScaler(PhysicalObjectScaler):
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
