import logging
import random

from drawtomat.language.word_embedding import WordEmbedding
from drawtomat.model.physical import PhysicalObject
from drawtomat.model.physical.physical_object_factory import PhysicalObjectFactory
from drawtomat.model.relational.object import Object
from drawtomat.quickdraw import QuickDrawDataset


class QuickDrawObjectFactory(PhysicalObjectFactory):
    def __init__(self, word_embedding: 'WordEmbedding' = None):
        if not word_embedding:
            self.word_embedding = WordEmbedding(QuickDrawDataset.words())
        else:
            self.word_embedding = word_embedding
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_physical_object(self, obj: 'Object', default_size: int = 100, unit: float = 1) -> 'PhysicalObject':
        """
        Loads a drawing from the Quick, Draw! dataset, crops the drawing and sets the strokes and
        the boundary attributes of the physical object (width, height) and adjusted strokes
        (in Quick, Draw! format).

        Returns
        -------
        PhysicalObject
            newly created object
        """
        phys_obj = PhysicalObject(obj)

        word = obj.word

        if not obj.word in QuickDrawDataset.words():
            word = self.word_embedding.most_similar_word(word)
            self.logger.debug(f"unknown word {obj.word} changed to {word}")

        data = QuickDrawDataset.images(word)
        drawing = random.choice(data)["drawing"]

        min_x = min([min(stroke[0]) for stroke in drawing])
        max_x = max([max(stroke[0]) for stroke in drawing])
        min_y = min([min(stroke[1]) for stroke in drawing])
        max_y = max([max(stroke[1]) for stroke in drawing])

        width = max_x - min_x
        height = max_y - min_y

        q = unit * default_size / max(width, height)

        phys_obj.strokes = [
            [
                [(x - min_x - width / 2) * q for x in stroke[0]],  # x-axis
                [(y - min_y - height / 2) * q for y in stroke[1]],  # y-axis
                stroke[2],  # time
            ]
            for stroke in drawing
        ]

        phys_obj._width = width * q
        phys_obj._height = height * q

        return phys_obj
