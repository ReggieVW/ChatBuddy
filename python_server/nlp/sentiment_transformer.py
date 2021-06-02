import keras
from  keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from keras_preprocessing.text import tokenizer_from_json
import os
import json
import numpy as np
import time

try:
    model =load_model(r'nlp/biLSTM_w2v.h5')
except:
    model =load_model(r'biLSTM_w2v.h5')

class_names = ['joy', 'fear', 'anger', 'sadness', 'neutral']

class SentimentNlp:

    def predict(self, message):
        max_seq_len = 500
        with open('nlp/tokenizer.json') as f:
            data = json.load(f)
            tokenizer = tokenizer_from_json(data)
        message = [message]
        seq = tokenizer.texts_to_sequences(message)
        padded = pad_sequences(seq, maxlen=max_seq_len)
        start_time = time.time()
        pred = model.predict(padded)
        print('pred: ' + str(pred))
        print('Message: ' + str(message))
        print('predicted: {} ({:.2f} seconds)'.format(class_names[np.argmax(pred)], (time.time() - start_time)))
        return class_names[np.argmax(pred)], "{0:.0%}".format(pred[0][np.argmax(pred)])
        
#sentimentNlp = SentimentNlp()
#label, percentage = sentimentNlp.predict('feeling happy')
#print(label)
#print(percentage)
