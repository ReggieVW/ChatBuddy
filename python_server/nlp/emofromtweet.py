from pandas import Series
from pathlib import Path
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import re
import nltk
from time import time
from emoji import demojize
import os
    
def get_tokenizer_and_encoder(tokenizer_path, encoder_path):
    with tokenizer_path.open('rb') as file:
        tokenizer = pickle.load(file)

    with encoder_path.open('rb') as file:
        encoder = pickle.load(file)

    return tokenizer, encoder

def predict(message):
    model =load_model(r'nlp/model.h5', compile=False)
    sequence = Series(message)
    sequence = _preprocess(sequence)
    tokenizer_path = Path('nlp/tokenizer.pickle').resolve()
    encoder_path = Path('nlp/encoder.pickle').resolve()
    tokenizer, encoder = get_tokenizer_and_encoder(tokenizer_path, encoder_path)
    list_tokenized = tokenizer.texts_to_sequences(message)
    sequence = pad_sequences(list_tokenized, maxlen=100)
    predictions = model.predict(sequence)
    pred = predictions.argmax(axis=1)
    return encoder.classes_[pred[0]], "{0:.0%}".format(predictions[0][np.argmax(predictions[0])])
    
def _preprocess(texts, quiet=False):
  # Lowercasing
  texts = texts.str.lower()

  # Remove special chars
  texts = texts.str.replace(r"(http|@)\S+", "")
  texts = texts.apply(demojize)
  texts = texts.str.replace(r"::", ": :")
  texts = texts.str.replace(r"’", "'")
  texts = texts.str.replace(r"[^a-z\':_]", " ")

  # Remove repetitions
  pattern = re.compile(r"(.)\1{2,}", re.DOTALL)
  texts = texts.str.replace(pattern, r"\1")

  # Transform short negation form
  texts = texts.str.replace(r"(can't|cannot)", 'can not')
  texts = texts.str.replace(r"n't", ' not')

  # Remove stop words
  stopwords = nltk.corpus.stopwords.words('english')
  stopwords.remove('not')
  stopwords.remove('nor')
  stopwords.remove('no')
  texts = texts.apply(
    lambda x: ' '.join([word for word in x.split() if word not in stopwords])
  )
  return texts
  
  