from collections import defaultdict
from email.policy import default
from scipy.io import wavfile  # scipy library to read wav files
import numpy as np
import os
from constants import CHOP_TIME_IN_SEC, PADDING_START, THRESHOLD_RATE

AUTO_CHOP_DIR = "data"
sampleNumberDict = defaultdict(int)


def chopSample(basedir, audioName):
    fs, Audiodata = wavfile.read(os.path.join(basedir, audioName))
    n = len(Audiodata)
    chopLength = int(fs * CHOP_TIME_IN_SEC)
    paddingLength = int(fs * PADDING_START)

    nameBase = audioName.split(".")[0].replace("1", "")
    print(nameBase)

    maxVolume = np.max(Audiodata)
    thresholdVolume = maxVolume * THRESHOLD_RATE

    idx = 0
    sampleNumber = sampleNumberDict[nameBase]
    while idx < n:
        if abs(Audiodata[idx]) > thresholdVolume:
            data = Audiodata[idx - paddingLength : idx - paddingLength + chopLength]
            if sampleNumber != 0:
                wavfile.write(f"{AUTO_CHOP_DIR}/{nameBase}-{sampleNumber}.wav", fs, data)
            sampleNumber += 1
            idx += chopLength
        else:
            idx += 1

    os.remove(f"{AUTO_CHOP_DIR}/{nameBase}-{sampleNumber-1}.wav")
    sampleNumberDict[nameBase] = sampleNumber - 2


def chopAllSamples(dirName):
    fileList = [
        f for f in os.listdir(dirName) if os.path.isfile(os.path.join(dirName, f)) and not f.startswith(".")
    ]
    for f in fileList:
        print(dirName, f)
        chopSample(dirName, f)

    metafile = open(f"{AUTO_CHOP_DIR}/metadata.csv", "w")
    metafile.write(",".join(list(sampleNumberDict.keys())) + "\n")
    metafile.write(",".join([str(i) for i in sampleNumberDict.values()]) + "\n")
    metafile.close()


if __name__ == "__main__":
    chopAllSamples("originalAudios")