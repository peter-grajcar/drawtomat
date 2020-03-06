

class QuickDrawDataset:

    def __init__(self):
        self.words = []
        with open("../resources/quickdraw/categories.txt") as f:
            for word in f.readlines():
                self.words.append(word.strip())
