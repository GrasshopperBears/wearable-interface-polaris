from collections import deque
import random
import joblib
from matplotlib import pyplot as plt
import numpy as np
import tensorflow as tf
import keras
from keras import utils, layers, optimizers
from choppa import chopAllSamples
import librosa

from featureExtraction import extractFeature

# constants
categories = []
sampleNumber = []
numberOfTestset = 0
numberOfSamples = 0
audioPath = "data/"
extName = ".wav"
testRatio = 0.2
isPrintingResultInsteadOfWeb = True
metaFileName = "data/metadata.csv"

def main():
    initialize()
    
    np.random.seed(1)
    tf.random.set_seed(1)

    # import trainset and testset with the features
    testSet, testLabel, trainSet, trainLabel = divideTrainAndTest()
    testFeatures = deque()
    trainFeatures = deque()

    for audioName in testSet:
        testFeatures.append(extractFeature(audioPath + audioName + extName))

    for audioName in trainSet:
        trainFeatures.append(extractFeature(audioPath + audioName + extName))

    npTestFeatures = np.array(testFeatures)
    npTestLabel = np.array(testLabel)
    npTrainFeatures = np.array(trainFeatures)
    npTrainLabel = np.array(trainLabel)

    print(npTestFeatures.shape)     # (684, 20, 51)
    print(npTestLabel.shape)        # (684,)
    print(npTrainFeatures.shape)    # (2739, 20, 51)
    print(npTrainLabel.shape)       # (2739,)

    item, count = np.unique(npTrainLabel, return_counts=True)
    print(dict(zip(item, count)))

    # Hyper parameter
    learning_rate = 5e-5
    N_EPOCHS = 50
    N_BATCH = 32
    N_CLASS = len(item)
    N_TRAIN = npTrainFeatures.shape[0]
    N_TEST = npTestFeatures.shape[0]
    DROP_RATE = 0.3

    # Scale the audio data
    scaler = joblib.load(f"model/scaler.pkl")
    trainShape = npTrainFeatures.shape
    testShape = npTestFeatures.shape
    npTrainFeatures = scaler.transform(npTrainFeatures.reshape(trainShape[0], -1)).reshape(trainShape)
    npTestFeatures = scaler.transform(npTestFeatures.reshape(testShape[0], -1)).reshape(testShape)

    # One-hot Encoding
    npTrainLabel = utils.to_categorical(npTrainLabel, N_CLASS)
    npTestLabel = utils.to_categorical(npTestLabel, N_CLASS)

    # Datasets
    train_dataset = tf.data.Dataset.from_tensor_slices((npTrainFeatures, npTrainLabel)).shuffle(100000).batch(N_BATCH, drop_remainder=True).repeat()
    test_dataset = tf.data.Dataset.from_tensor_slices((npTestFeatures, npTestLabel)).batch(N_BATCH)

    # Create model
    def create_model():
        model = keras.Sequential()

        model.add(layers.Conv1D(filters=32, kernel_size=3, padding='same', activation='relu'))
        model.add(layers.MaxPooling1D(pool_size=2))
        model.add(layers.Conv1D(filters=32, kernel_size=3, padding='same', activation='relu'))
        model.add(layers.MaxPooling1D(pool_size=2))
        model.add(layers.Conv1D(filters=64, kernel_size=3, padding='same', activation='relu'))
        model.add(layers.MaxPooling1D(pool_size=2))
        model.add(layers.Flatten())

        model.add(layers.Dense(128, activation="relu"))
        model.add(layers.Dropout(DROP_RATE))
        model.add(layers.Dense(64, activation="relu"))
        model.add(layers.Dropout(DROP_RATE))

        model.add(layers.Dense(N_CLASS, activation="softmax"))

        return model
    
    # Compile model
    model = create_model()
    model.compile(optimizer=optimizers.Adam(learning_rate), loss='categorical_crossentropy', metrics=['accuracy'])

    # Train the model
    steps_per_epoch = N_TRAIN // N_BATCH
    validation_steps = int(np.ceil(N_TEST / N_BATCH))

    history = model.fit(train_dataset, epochs=N_EPOCHS, steps_per_epoch=steps_per_epoch, validation_data=test_dataset, validation_steps=validation_steps)

    # Save the model
    filepath = './saved_model'
    keras.models.save_model(model, filepath)

    converter = tf.lite.TFLiteConverter.from_saved_model(filepath) # path to the SavedModel directory
    tflite_model = converter.convert()

    with open('model.tflite', 'wb') as f:
        f.write(tflite_model)

    # Loss curve
    plt.figure(figsize=(10, 7))
    
    plt.plot(history.history['loss'], label='Train loss')
    plt.plot(history.history['val_loss'], label='Validation loss')
    
    plt.title("Loss")
    plt.legend()

    # Accuracy curve
    plt.figure(figsize=(10, 7))
    
    plt.plot(history.history['accuracy'], label='Train accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation accuracy')
    
    plt.title("accuracy")
    plt.legend()
    plt.show()

def initialize():
    global categories
    global sampleNumber
    global numberOfTestset
    global numberOfSamples

    try:
        metadata = open(metaFileName, "r")
    except:
        print("Auto-chopping original audios...")
        chopAllSamples("originalAudios")
        print("Auto-chopping done.")
        metadata = open(metaFileName, "r")

    categories = metadata.readline().strip("\n").split(",")
    sampleNumber = [int(s) for s in metadata.readline().strip("\n").split(",")]
    metadata.close()

    numberOfSamples = len(categories)
    numberOfTestset = int(sum(sampleNumber) * testRatio // numberOfSamples)

def divideTrainAndTest():
    testSet = []
    testLabel = []
    trainSet = []
    trainLabel = []
    for i in range(numberOfSamples):
        numlist = [f"{categories[i]}-{j + 1}" for j in range(sampleNumber[i])]
        random.shuffle(numlist)
        testSet += numlist[:numberOfTestset]
        testLabel += [i] * (numberOfTestset)
        trainSet += numlist[numberOfTestset:]
        trainLabel += [i] * (sampleNumber[i] - numberOfTestset)

    return testSet, testLabel, trainSet, trainLabel

main()