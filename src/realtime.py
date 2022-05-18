import os
import pickle
import joblib
import pyaudio
import librosa
import numpy as np
from constants import CHOP_TIME_IN_SEC, PADDING_START, THRESHOLD_RATE
from featureExtraction import extractFeatureWithRawData
 
RATE = 16000
CHUNK = int(RATE * CHOP_TIME_IN_SEC)
THRESHOLD = int(THRESHOLD_RATE * 32768)

padding_length = int(PADDING_START * RATE)
nbits = 16

def realtime():
    models, categories = loadModels()
    
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
            features = extractFeatureWithRawData(AudioData, RATE).reshape(1, -1)
            
            result = [model.decision_function(features) for model in models]
            if max(result) > 0:
                print(categories[np.argmax(np.array(result))])
            else:
                print("Not sure")
            
        prevData = data
        data = nextData
        
    stream.stop_stream()
    stream.close()
    p.terminate()

def loadModels(modelPath = "model/"):
    modelList = []
    categories = []
    for modelName in os.listdir(modelPath):
        modelList.append(joblib.load(f"{modelPath}/{modelName}"))
        categories.append(modelName.split(".")[0])

    return modelList, categories

if __name__ == "__main__":
    realtime()