

class QuickDrawDataset:
    """
    Tris class provides data from the Google's "Quick, Draw!" dataset.
    """
    _words = None

    @staticmethod
    def words():
        if not QuickDrawDataset._words:
            QuickDrawDataset._words = []
            with open("../resources/quickdraw/categories.txt") as f:
                for word in f.readlines():
                    QuickDrawDataset._words.append(word.strip())

        return QuickDrawDataset._words
