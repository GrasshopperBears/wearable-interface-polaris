import numpy as np
import pickle
from sklearn import svm
import joblib


def svm_classify(train_feats, train_labels, test_feats):
    """
    This function should train a linear SVM for every category (i.e., one vs all)
    and then use the learned linear classifiers to predict the category of every
    test audio. Every test feature will be evaluated with all 3 SVMs and the
    most confident SVM will 'win'.

    :param train_feats:
        an N x d matrix, where d is the dimensionality of the feature representation.
    :param train_labels:
        an N array, where each entry is a string indicating the ground truth category
        for each training audio.
    :param test_feats:
        an M x d matrix, where d is the dimensionality of the feature representation.

    :return:
        an M array, where each entry is a string indicating the predicted
        category for each test audio.
    """

    categories = np.unique(train_labels)

    category_size = categories.shape[0]
    train_size = train_feats.shape[0]
    test_size = test_feats.shape[0]
    svmResult = np.zeros([category_size, test_size])

    for categoryIdx in range(category_size):
        category = categories[categoryIdx]
        y = np.ones([train_size])
        y[train_labels != category] = -1

        model = svm.SVC(kernel="rbf", C=1000)
        model.fit(train_feats, y)
        svmResult[categoryIdx] = model.decision_function(test_feats)

    classifiedIndex = np.argmax(svmResult, axis=0)

    return categories[classifiedIndex]

def make_svm_model(train_feats, train_labels):
    categories = np.unique(train_labels)

    category_size = categories.shape[0]
    train_size = train_feats.shape[0]

    for categoryIdx in range(category_size):
        category = categories[categoryIdx]
        y = np.ones([train_size])
        y[train_labels != category] = -1

        model = svm.SVC(kernel="rbf", C=1000)
        model.fit(train_feats, y)
        
        joblib.dump(model, f"model/{category}.pkl")