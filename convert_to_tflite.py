"""
Convertit model.keras (entraîné sur Kaggle) en model.tflite pour l'hébergement.
À lancer une seule fois, là où TensorFlow est installé (votre PC ou Kaggle) :
    python convert_to_tflite.py
"""
import keras
import tensorflow as tf

model = keras.models.load_model("model.keras", compile=False)
converter = tf.lite.TFLiteConverter.from_keras_model(model)
with open("model.tflite", "wb") as f:
    f.write(converter.convert())
print("model.tflite créé")
