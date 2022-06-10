# from scipy.io import wavfile  # scipy library to read wav files
# import numpy as np
# import peakutils

# # spectrum
# from scipy.fftpack import fft  # fourier transform

# numberOfPeaks = 8


# def extractFeature(audioName):
#     fs, Audiodata = wavfile.read(audioName)
#     features = []

#     n = len(Audiodata)
#     AudioFreq = fft(Audiodata)
#     AudioFreq = AudioFreq[0 : int(np.ceil((n + 1) / 2.0))]  # Half of the spectrum
#     MagFreq = np.abs(AudioFreq)  # Magnitude
#     MagFreq = MagFreq / float(n)
#     MagFreq = MagFreq ** 2  # power spectrum

#     if n % 2 > 0:  # ffte odd
#         MagFreq[1 : len(MagFreq)] = MagFreq[1 : len(MagFreq)] * 2
#     else:  # fft even
#         MagFreq[1 : len(MagFreq) - 1] = MagFreq[1 : len(MagFreq) - 1] * 2

#     freqAxis = np.arange(0, int(np.ceil((n + 1) / 2.0)), 1.0) * (fs / n)

#     dBMagFreq = 10 * np.log10(MagFreq)

#     indexes = peakutils.indexes(dBMagFreq, thres=0.5, min_dist=150)

#     freqs = freqAxis[indexes]
#     magFreqs = dBMagFreq[indexes]
#     indices = np.argsort(magFreqs)[-numberOfPeaks:][::-1]
#     features += [i for i in freqs[indices]]

#     return np.array(features)

import numpy as np
import librosa


def extractFeature(audioName):
    Audiodata, fs = librosa.load(audioName, sr=None)

    return extractFeatureWithRawData(Audiodata, fs)

def extractFeatureWithRawData(Audiodata, fs):
    D = np.abs(librosa.stft(Audiodata, n_fft=fs//100, win_length=fs//100, hop_length=fs//250))
    mfcc = librosa.feature.mfcc(S=librosa.power_to_db(D), sr=fs, n_mfcc=20)

    return mfcc

def extractFeatureFlatten(audioName):
    Audiodata, fs = librosa.load(audioName, sr=None)

    return extractFeatureFlattenWithRawData(Audiodata, fs)

def extractFeatureFlattenWithRawData(Audiodata, fs):
    D = np.abs(librosa.stft(Audiodata, n_fft=fs//100, win_length=fs//100, hop_length=fs//250))
    mfcc = librosa.feature.mfcc(S=librosa.power_to_db(D), sr=fs, n_mfcc=20)

    return mfcc.reshape(-1)