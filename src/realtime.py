import os
import joblib
import pyaudio
import numpy as np
from constants import CHOP_TIME_IN_SEC, PADDING_START, THRESHOLD_RATE
from featureExtraction import extractFeatureWithRawData
import matplotlib.pyplot as plt
import board
import adafruit_lsm9ds1
import requests
from time import time
import requests
 
RATE = 48000
CHUNK = int(RATE * CHOP_TIME_IN_SEC)
THRESHOLD = int(THRESHOLD_RATE * 32768)
IMU_THRESHOLD = 2

padding_length = int(PADDING_START * RATE)
nbits = 16

doubleTapThreshold = 0.5

BASE_URL = ''

def realtime():
    # BASE_URL = input("Enter base URL: ")
    # i2c = board.I2C()
    # sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
    if len(BASE_URL) == 0:
        print("Enter base URL")
        exit(0)
    
    prevTime = 0
    prevPredict = ""
    scaler, pca, models, categories = loadModels()
    
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    AudioData = np.zeros(CHUNK, dtype=np.float32)
    prevData = np.frombuffer(stream.read(CHUNK, exception_on_overflow = False), dtype=np.int16)
    data = np.frombuffer(stream.read(CHUNK, exception_on_overflow = False), dtype=np.int16)
    
    dynamite = 0

    while True:
        # _, _, accel_z = sensor.acceleration
        # accel_z = abs(accel_z)

        nextData = np.frombuffer(stream.read(CHUNK, exception_on_overflow = False), dtype=np.int16)
        
        overThrList = np.argwhere(np.abs(data) > THRESHOLD)
        # if len(overThrList) != 0 and accel_z > IMU_THRESHOLD:
        if len(overThrList) != 0: # the case when some value is exceed threshold
            first = overThrList[0][0]

            if dynamite > 0:
                dynamite -= 1
                prevData = data
                data = nextData
                continue

            startIdx = first - padding_length
            if startIdx > 0:
                concatData = np.concatenate((data[startIdx : ], nextData[ : startIdx]), axis=None)
            else:
                concatData = np.concatenate((prevData[startIdx : ], data[ : startIdx]), axis=None)
            
            lastIdx = startIdx + np.argwhere(np.abs(concatData) > THRESHOLD)[-1][0]
            if lastIdx > CHUNK:
                dynamite = 3 + ((lastIdx - CHUNK) // (CHUNK // 5))
                
            AudioData = concatData / (2 ** (nbits - 1))
            features = extractFeatureWithRawData(AudioData, RATE).reshape(1, -1)
            features = scaler.transform(features)
            features = pca.transform(features)

            result = [model.decision_function(features)[0] for model in models]
            # result = knn.predict(features)
            # print(features)
            # print(result)

            # wavfile.write(f"test/{AudioData[0]}{AudioData[1]}{AudioData[2]}{AudioData[3]}.wav", RATE, concatData)
            # plt.figure(1)
            # plt.title("Signal Wave???")
            # plt.plot(AudioData)
            # plt.show()
            
            print("------------------------")
            curTime = time()
            print(curTime)
            if max(result) > 0:
                category = categories[np.argmax(np.array(result))]
                
                if curTime - prevTime < doubleTapThreshold and prevPredict == category:
                    print(f"{prevPredict} double tap!")
                else:
                    print(category)
                    prevTime = curTime
                    prevPredict = category
                
                requests.post('{}/detect/{}'.format(BASE_URL, category))
                
                # print(categories)
                # print(result)
            else:
                print("Not sure")
                # print(categories)
                # print(result)
            print("")
            print("-------------------------")
            
        if dynamite > 0: dynamite -= 1
        prevData = data
        data = nextData
    
    stream.stop_stream()
    stream.close()
    p.terminate()

def loadModels(modelPath = "model/"):
    modelList = []
    categories = []
    for modelName in os.listdir(modelPath):
        if modelName.startswith("scaler"):
            scaler = joblib.load(f"{modelPath}/{modelName}")
        elif modelName.startswith("pca"):
            pca = joblib.load(f"{modelPath}/{modelName}")
        # elif modelName.startswith("knn"):
        #     knn = joblib.load(f"{modelPath}/{modelName}")
        elif not modelName.startswith("."):
            modelList.append(joblib.load(f"{modelPath}/{modelName}"))
            categories.append(modelName.split(".")[0])

    return scaler, pca, modelList, categories

if __name__ == "__main__":
    realtime()