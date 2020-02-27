# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd
import scipy.io.wavfile
import python_speech_features as psf


def get_file_features(wav_fname, num_ceps):
    # read wave
    fs, sig = scipy.io.wavfile.read(wav_fname)

    # get mfccs
    mfccs = psf.mfcc(sig, samplerate=fs, winlen=0.025, winstep=0.01,
                     numcep=num_ceps, nfilt=26, nfft=512, lowfreq=0,
                     highfreq=None, preemph=0.97, ceplifter=22,
                     appendEnergy=False)

    # compute mfcc means
    mfcc_means = np.round(mfccs.mean(axis=0), 3)
    return mfcc_means


def extract_features(folder, num_ceps, fname, augmented=False):
    # collect paths to wave files
    wave_fnames = [os.path.join(root, file)
                   for root, dirs, files in os.walk(folder)  for file in files]

    # init features & errors and column names
    features = []
    errors_caused = []

    # in case augmented data is processed
    if augmented: wave_fnames = [fname for fname in wave_fnames if "augment" in fname]
    else        : wave_fnames = [fname for fname in wave_fnames if "augment" not in fname]

    # get voice features
    for wave_fname in wave_fnames[:]:
        try:
            feats = get_file_features(wave_fname, num_ceps)
            features.append([wave_fname] + [x for x in list(feats)] + [wave_fname.split("/")[-2]])
        except:
            print("Error: error occured when processing ", wave_fname)
            errors_caused.append(wave_fname)

    # define column names for csv
    column_names = ["file_name"] + ["mfcc" + str(i) for i in range(num_ceps)] + ["emotion"]

    # export results to file
    data = pd.DataFrame(features, columns=column_names)
    data.to_csv(fname)
    return errors_caused


if __name__ == "__main__":
    _ = extract_features(folder="data/waves", num_ceps=13, fname="data/features.csv")
    _ = extract_features(folder="data/waves", num_ceps=13, fname="data/augmented_features.csv", augmented=True)
