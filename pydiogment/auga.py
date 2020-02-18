"""
- Description: amplitude based augmentation techniques/manipulations for audio data.
rms_normalization = https://www.hackaudio.com/digital-signal-processing/amplitude/rms-normalization/
https://samplecraze.com/2019/01/03/normalisation-peak-and-rms/
"""
import os
import math
import random
import tempfile
import warnings
import subprocess
import numpy as np
from scipy.signal import resample
from .augt import eliminate_silence
from .io import read_file, write_file


def apply_gain(infile, gain):
    """
    apply gain to infile.

    Args:
        infile (str) : input filename/path.
        gain (float) : gain in dB (both positive and negative).
    """
    # read input file
    fs, x = read_file(filename=infile)

    # apply gain
    x = np.copy(x)
    x = x * (10**(gain / 20.0))
    x = np.minimum(np.maximum(-1.0, x), 1.0)
    x /= np.mean(np.abs(x))

    # export data to file
    input_file_name = os.path.basename(infile)
    output_file_path = os.path.dirname(infile)
    name_attribute = "_augmented_with_%s_gain.wav" % str(gain)
    write_file(output_file_path=output_file_path,
               input_file_name=infile,
               name_attribute=name_attribute,
               sig=x,
               fs=fs)


def add_noise(infile, snr):
    """
    augment data using noise injection.

    Note:
        It simply add some random values to the input file data based on the snr.

    Args:
        infile (str) : input filename/path.
        snr    (int) : signal to noise ratio in dB.
    """
    # read input file
    fs, sig = read_file(filename=infile)

    # compute and apply noise
    noise = np.random.randn(len(sig))

    # compute rms
    rms_noise = np.sqrt(np.mean(np.power(noise, 2)))
    rms_sig = np.sqrt(np.mean(np.power(sig, 2)))

    snr_linear = 10**(snr / 20.0)
    noise_factor = (rms_sig / rms_noise) * snr_linear

    y = sig + noise * noise_factor
    rms_y = np.sqrt(np.mean(np.power(y, 2)))
    y = y * rms_sig / rms_y

    # normalize signal
    y /= np.mean(np.abs(y))

    # construct file names
    input_file_name = os.path.basename(infile)
    output_file_path = os.path.dirname(infile)
    name_attribute = "_augmented_%s_noisy.wav" % snr

    # export data to file
    write_file(output_file_path=output_file_path,
               input_file_name=infile,
               name_attribute=name_attribute,
               sig=y,
               fs=fs)


def fade_in_and_out(infile):
    """
    add a fade in and out effect to the audio file.

    Args:
        infile (str) : input filename/path.
    """
    # read input file
    fs, sig = read_file(filename=infile)
    kernel = 0.5**np.arange(len(sig))
    window = np.hamming(len(sig))

    # construct file names
    input_file_name = os.path.basename(infile).split(".wav")[0]
    output_file_path = os.path.dirname(infile)
    name_attribute = "_augmented_fade_in_out.wav"

    # fade in and out
    window = np.hamming(len(sig))
    augmented_sig = window * sig
    augmented_sig /= np.mean(np.abs(augmented_sig))

    # export data to file
    write_file(output_file_path=output_file_path,
               input_file_name=infile,
               name_attribute=name_attribute,
               sig=augmented_sig,
               fs=fs)


def normalize(infile, normalization_technique="peak", rms_level=0):
    """
    normalize the signal given a certain technique (peak or rms).

    Args:
        infile                  (str) : input filename/path.
        normalization_technique (str) : type of normalization technique to use.
                                        default is peak
        rms_level               (int) : rms level in dB.
    """
    # read input file
    fs, sig = read_file(filename=infile)

    # normalize signal
    if normalization_technique == "peak" :
        y = sig / np.max(sig)

    elif normalization_technique == "rms":
        # compute rms values
        rms_sig = np.sqrt(np.sum(sig**2) / len(sig))

        # linear rms level and scaling factor
        r = 10**(rms_level / 20.0)
        a = np.sqrt( (len(sig) * r**2) / np.sum(sig**2) )

        # normalize
        y = sig * a

    else :
        print("ParameterError: Unknown normalization_technique variable.")

    # construct file names
    input_file_name = os.path.basename(infile).split(".wav")[0]
    output_file_path = os.path.dirname(infile)
    name_attribute = "_augmented_{}_normalized.wav".format(normalization_technique)

    # export data to file
    write_file(output_file_path=output_file_path,
               input_file_name=infile,
               name_attribute=name_attribute,
               sig=y,
               fs=fs)


def resample(infile, sr):
    """
    normalize the signal given a certain technique (peak or rms).

    Args:
        infile (str) : input filename/path.
        sr     (int) : new sampling rate.
    """
    # read input file
    fs, sig = read_file(filename=infile)

    # compute the number of samples
    number_of_samples = np.floor((sr / fs) * len(x))

    # resample signal
    y = resample(sig, number_of_samples)

    # construct file names
    input_file_name = os.path.basename(infile).split(".wav")[0]
    output_file_path = os.path.dirname(infile)
    name_attribute = "_augmented_resampled_with_{}.wav".format(sr)

    # export data to file
    write_file(output_file_path=output_file_path,
               input_file_name=infile,
               name_attribute=name_attribute,
               sig=y,
               fs=fs)
