import numpy as np
import random
from collections import deque

from featureExtraction import extractFeature
from svm import svm_classify
from create_results_webpage import create_results_webpage

# number of samples
NUMBER_OF_SAMPLES = 3

# constants
categories = ["coffee", "desk", "oculus"]
audioPath = "audios/"
sampleNumber = [52, 51, 53]
extName = ".wav"
testRatio = 0.2
numberOfTestset = int(sum(sampleNumber) * testRatio // 3)
isPrintingResultInsteadOfWeb = True

# for multiple training
isSavingToCSV = True
if isSavingToCSV:
    outputFileName = "output.csv"
    outputFile = open(outputFileName, "w")
    iteration = 100


def main():
    if isSavingToCSV:
        for ctg in categories:
            outputFile.write(f"{ctg}-precision,{ctg}-recall,{ctg}-f1,")
        outputFile.write("total-accuracy\n")

        for i in range(iteration):
            loop()

    else:
        loop()


def loop():
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

    svmResult = svm_classify(npTrainFeatures, npTrainLabel, npTestFeatures)

    if isSavingToCSV:
        outputFile.write(printAllResults(svmResult, npTestLabel))
    else:
        if isPrintingResultInsteadOfWeb:
            printAllResults(svmResult, npTestLabel)
        else:
            create_results_webpage(
                np.array(["image.jpg" for i in trainLabel]),
                np.array(["image.jpg" for i in testLabel]),
                npTrainLabel,
                npTestLabel,
                categories,
                categories,
                svmResult,
            )


def printAllResults(result, oracle):
    returnString = ""
    for i in range(NUMBER_OF_SAMPLES):
        ctg = categories[i]
        samplesInCtg = result[oracle == categories[i]]
        samplesNotInCtg = result[oracle != categories[i]]
        totalSample = len(oracle)

        tp = np.sum(samplesInCtg == ctg)
        fn = np.sum(samplesInCtg != ctg)
        fp = np.sum(samplesNotInCtg == ctg)
        tn = np.sum(samplesNotInCtg != ctg)

        precision = tp / (tp + fp)
        recall = tp / (tp + fn)

        f1 = 2 * (precision * recall) / (precision + recall)

        if isSavingToCSV:
            returnString += f"{precision},{recall},{f1},"
        else:
            print(f"============ {categories[i]} ============")
            print("tp", tp / totalSample * 100, "%")
            print("fn", fn / totalSample * 100, "%")
            print("fp", fp / totalSample * 100, "%")
            print("tn", tn / totalSample * 100, "%")
            print("---------------------")
            print("precision: ", precision)
            print("recall: ", recall)
            print("---------------------")
            print("f1: ", f1)
            print()

    accuracy = np.sum(result == oracle) / totalSample * 100
    if isSavingToCSV:
        returnString += f"{accuracy}%\n"
    else:
        print(f"============ total ============")
        print("total accuracy: ", accuracy, "%")

    if isSavingToCSV:
        return returnString


def divideTrainAndTest():
    testSet = []
    testLabel = []
    trainSet = []
    trainLabel = []
    for i in range(NUMBER_OF_SAMPLES):
        numlist = [f"{categories[i]}-{j + 1}" for j in range(sampleNumber[i])]
        random.shuffle(numlist)
        testSet += numlist[:numberOfTestset]
        testLabel += [categories[i]] * (numberOfTestset)
        trainSet += numlist[numberOfTestset:]
        trainLabel += [categories[i]] * (sampleNumber[i] - numberOfTestset)

    return testSet, testLabel, trainSet, trainLabel


if __name__ == "__main__":
    main()