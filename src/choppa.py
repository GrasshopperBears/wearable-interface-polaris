from scipy.io import wavfile  # scipy library to read wav files
import numpy as np
import os

CHOP_TIME_IN_SEC = 0.3
THRESHOLD_RATE = 0.2
PADDING_START = 0.01

AUTO_CHOP_DIR = "data"


def chopSample(basedir, audioName):
    fs, Audiodata = wavfile.read(os.path.join(basedir, audioName))
    n = len(Audiodata)
    chopLength = int(fs * CHOP_TIME_IN_SEC)
    paddingLength = int(fs * PADDING_START)

    nameBase = audioName.split(".")[0]

    maxVolume = np.max(Audiodata)
    thresholdVolume = maxVolume * THRESHOLD_RATE

    idx = 0
    sampleNumber = 1
    while idx < n:
        if abs(Audiodata[idx]) > thresholdVolume:
            data = Audiodata[idx - paddingLength : idx - paddingLength + chopLength]
            wavfile.write(f"{AUTO_CHOP_DIR}/{nameBase}-{sampleNumber}.wav", fs, data)
            sampleNumber += 1
            idx += chopLength
        else:
            idx += 1

    os.remove(f"{AUTO_CHOP_DIR}/{nameBase}-{sampleNumber-1}.wav")

    return nameBase, sampleNumber - 2


def chopAllSamples(dirName):
    fileList = [
        f for f in os.listdir(dirName) if os.path.isfile(os.path.join(dirName, f))
    ]
    nameList = []
    countList = []
    for f in fileList:
        name, count = chopSample(dirName, f)
        nameList.append(name)
        countList.append(str(count))

    metafile = open(f"{AUTO_CHOP_DIR}/metadata.csv", "w")
    metafile.write(",".join(nameList) + "\n")
    metafile.write(",".join(countList) + "\n")
    metafile.close()


if __name__ == "__main__":
    chopAllSamples("originalAudios")