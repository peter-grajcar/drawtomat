import csv

import ndjson


class QuickDrawDataset:
    """
    Tris class provides data from the Google's "Quick, Draw!" dataset.
    """
    _words = None
    _images = None
    _attributes = None

    @staticmethod
    def words() -> list:
        """
        Returns a list of words present in the Quick, Draw! dataset.

        Returns
        -------
        list
            A list of words available in the dataset.
        """
        if not QuickDrawDataset._words:
            QuickDrawDataset._words = list()
            with open("resources/quickdraw/categories.txt") as f:
                for word in f.readlines():
                    QuickDrawDataset._words.append(word.strip())

        return QuickDrawDataset._words

    @staticmethod
    def images(word: str = None) -> dict:
        """
        Returns a dictionary of data for each word.

        Returns
        -------
        dict

        """
        if not QuickDrawDataset._images:
            QuickDrawDataset._images = dict()
            for w in QuickDrawDataset.words():
                with open(f"resources/quickdraw/dataset/{w}.ndjson") as f:
                    QuickDrawDataset._images[w] = ndjson.load(f)
        if word:
            return QuickDrawDataset._images[word]
        return QuickDrawDataset._images

    @staticmethod
    def attributes(word: str = None) -> dict:
        """
        Returns a dictionary of attributes for each word.

        Returns
        -------

        """
        if not QuickDrawDataset._attributes:
            QuickDrawDataset._attributes = dict()
            for w in QuickDrawDataset.words():
                with open(f"resources/quickdraw/attributes.csv") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        QuickDrawDataset._attributes[row["category"]] = {
                            "default_width": float("0" + row["default_width"]),
                            "default_height": float("0" + row["default_height"]),
                        }
        if word:
            return QuickDrawDataset._attributes[word]
        return QuickDrawDataset._attributes


