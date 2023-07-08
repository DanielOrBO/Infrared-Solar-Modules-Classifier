def example1():
    return "test"

import os 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.imagenet_utils import preprocess_input



def convert_to_binary(x):
    x = 'Anomaly' if x != 'No-Anomaly' else x
    return x



def J2Anottation(DATA_PATH, METADATA_PATH):
    
    df = pd.read_json(METADATA_PATH, orient='index').sort_index()
    # df["image_filepath"] = df.anomaly_class.apply(lambda x: os.path.join(DATA_PATH, convert_to_binary(x)))
    df['image_filepath'] = df.image_filepath.apply(lambda x: os.path.join(DATA_PATH, x))
    df["anomaly_class"] = df.anomaly_class.apply(convert_to_binary).sort_index()
    return df

def ExtFwVGG16(image_path):
    
    # Cargar el modelo preentrenado VGG16
    vgg16 = VGG16(weights='imagenet')

    # Cargar y preprocesar la imagen de entrada
    img = image.load_img(image_path, target_size=(224, 224))

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    # # Obtener las características de la imagen
    features = vgg16.predict(x)
    
    return features

def dataframe(df):
    
    sample = df.groupby("anomaly_class").sample(n=10).sort_index()
    filas = sample.index.tolist()

    for i in range(1000):
        
        colum_name = f"Columna_{i}"
        sample[colum_name] = ""
        
    for n in range(len(filas)):
        
        Features = ExtFwVGG16(df["image_filepath"][filas[n]])
        sample.iloc[n,2::] = Features[0]
    
    return sample

def PreDS (x , number_datos = 20):
    return x [0][:number_datos]
