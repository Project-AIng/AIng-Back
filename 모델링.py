#pip install tensorflow_text
#pip install wordcloud
#pip install tokenization

import tensorflow_text
import matplotlib 
import pandas as pd
import matplotlib.pyplot as plt

#from matplotlib.patches import Polygon
import numpy as n
from math import pi

import tensorflow as tf
 
import tensorflow_hub as hub



def model_init():
    bert_preprocess = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3")

    text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
    preprocessed_text = bert_preprocess(text_input)

    bert_encoder = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4")

    outputs = bert_encoder(preprocessed_text)

    l = tf.keras.layers.Dropout(0.1, name="dropout")(outputs['pooled_output'])
    l = tf.keras.layers.Dense(120, activation='relu')(l)
    l = tf.keras.layers.Dense(320, activation='relu')(l)
    l = tf.keras.layers.Dense(10, activation='softmax', name="output")(l)

    custom_objects = {'KerasLayer': hub.KerasLayer}

    model = tf.keras.models.load_model("/content/drive/MyDrive/model.h5", custom_objects=custom_objects)
    return model

def select_subject(model, test_data):
    
    # 예측 수행

    dict1 = {0:"Space", 1:"Politics",2:"Sport",3:"technology",4:"historical", 5:"Medical", 6:"Graphics",7:"Entertrainment",8:"Food",9:"business"}
    results = model.predict([test_data])[0]
    top3_indices = results.argsort()[-3:][::-1]

    for i in top3_indices:
        print(dict1[i])
        

test_data = """
Football, also known as soccer in some countries, is a beloved sport that brings people together from all walks of life. The roar of the crowd and the exhilaration of scoring a goal create an electric atmosphere in stadiums around the world. Players showcase their skills and teamwork, dribbling past opponents, executing precise passes, and unleashing powerful shots. The competitive nature of the game fosters a sense of camaraderie and sportsmanship among players. Whether it's the FIFA World Cup or local league matches, football unites fans, ignites passions, and leaves lasting memories for both players and spectators alike
"""
model = model_init()
select_subject(model,test_data)

