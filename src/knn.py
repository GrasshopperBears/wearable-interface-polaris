import numpy as np
import pickle
import joblib
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

NEIGHBORS = 9

def knn_classify(train_feats, train_labels, test_feats):
    """
    This function should train a linear knn for every category (i.e., one vs all)
    and then use the learned linear classifiers to predict the category of every
    test audio. Every test feature will be evaluated with all 3 knns and the
    most confident knn will 'win'.

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

    scaler = StandardScaler()
    scaler.fit(train_feats)
    train_feats = scaler.transform(train_feats)
    test_feats = scaler.transform(test_feats)

    model = KNeighborsClassifier(n_neighbors=NEIGHBORS)
    model.fit(train_feats, train_labels)

    return model.predict(test_feats)

def make_knn_model(train_feats, train_labels):
    scaler = StandardScaler()
    scaler.fit(train_feats)
    train_feats = scaler.transform(train_feats)
    joblib.dump(scaler, f"model/scaler.pkl")
    
    model = KNeighborsClassifier(n_neighbors=NEIGHBORS)
    model.fit(train_feats, train_labels)
        
    joblib.dump(model, f"model/knn.pkl")