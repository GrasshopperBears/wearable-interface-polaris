import os
import pickle
import joblib
import pyaudio
import librosa
import numpy as np
from constants import CHOP_TIME_IN_SEC, PADDING_START, THRESHOLD_RATE
from featureExtraction import extractFeatureWithRawData
from scipy.io import wavfile  # scipy library to write wav files
import soundfile as sf
import matplotlib.pyplot as plt
import keras

from choppa import chopAllSamples
 
RATE = 48000
CHUNK = int(RATE * CHOP_TIME_IN_SEC)
THRESHOLD = int(THRESHOLD_RATE * 32768)

padding_length = int(PADDING_START * RATE)
nbits = 16

# constants
categories = []
metaFileName = "data/metadata.csv"

def realtime():
    scaler, model = loadModels()
    
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    AudioData = np.zeros(CHUNK, dtype=np.float32)
    prevData = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)

    while True:
        nextData = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        
        overThrList = np.argwhere(np.abs(data) > THRESHOLD)
        if len(overThrList) != 0: # the case when some value is exceed threshold
            first = overThrList[0][0]
            startIdx = first - padding_length
            if startIdx > 0:
                concatData = np.concatenate((data[startIdx : ], nextData[ : startIdx]), axis=None)
            else:
                concatData = np.concatenate((prevData[startIdx : ], data[ : startIdx]), axis=None)
                
            AudioData = concatData / (2 ** (nbits - 1))
            features = extractFeatureWithRawData(AudioData, RATE)
            s = features.shape
            print(s)
            features = scaler.transform(features.reshape(1, -1)).reshape(1, s[0], s[1])

            result = model.predict(features)
            print(categories[np.argmax(result)])
            
        prevData = data
        data = nextData
        
    stream.stop_stream()
    stream.close()
    p.terminate()

def loadModels(modelPath = "model/"):
    scaler = joblib.load(f"model/scaler.pkl")
    model = keras.models.load_model("./saved_model")

    return scaler, model

def initialize():
    global categories

    try:
        metadata = open(metaFileName, "r")
    except:
        print("Auto-chopping original audios...")
        chopAllSamples("originalAudios")
        print("Auto-chopping done.")
        metadata = open(metaFileName, "r")

    categories = metadata.readline().strip("\n").split(",")
    metadata.close()

if __name__ == "__main__":
    initialize()
    realtime()