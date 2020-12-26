#!/usr/bin/env python3
import fasttext

model = fasttext.train_unsupervised("../../conceptualcaptions-dataset/train.txt", "cbow")

model.save_model("conceptual-captions-fasttext.model")

