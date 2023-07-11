
import os 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import mysql.connector
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
        sample.iloc[n,2::] = Features[0].tolist()
    
    return sample

def PreDS (x , number_datos = 20):
    return np.array([x [0][:number_datos]])

def ReadDB():
    
    conn =  mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "Paneles_img")
    # El cursor es el que nos permite interactuar con la bbdd
    cursor = conn.cursor()

    sql = """ SELECT * FROM FEATURES"""
    cursor.execute(sql)
    Features = cursor.fetchall()
    df = pd.DataFrame(Features)

    return df

def UploadDB (df):

    conn =  mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    #port = "3306" # Se puede omitir (lo comentamos), se coloca por defecto
    database = "Paneles_img"
    )
    cursor = conn.cursor()
    tabla = "imagenes"
    columnas = ', '.join(df.columns)

    consulta = f"INSERT INTO {tabla} ({columnas}) VALUES "

    valores = ", ".join(["%s"] * len(df.columns))
    cursor.executemany(consulta + f"({valores})", df.values.tolist())

    conn.commit()
    conn.close()