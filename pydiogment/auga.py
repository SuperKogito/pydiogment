"""
- Description: amplitude based augmentation techniques/manipulations for audio data.
"""
import os
import numpy as np
from scipy.signal import resample
from .utils.io import read_file, write_file


def apply_gain(infile, gain):
    """
    Apply gain to infile.

    Args:
        - infile (str) : input filename/path.
        - gain (float) : gain in dB (both positive and negative).
    """
    # read input file
    fs, x = read_file(filename=infile)

    # apply gain
    x = np.copy(x)
    x = x * (10**(gain / 10.0))
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
    Augment data using noise injection.

    Note:
        It simply add some random values to the input file data based on the snr.

    Args:
        - infile (str) : input filename/path.
        - snr    (int) : signal to noise ratio in dB.
    """
    # read input file
    fs, sig = read_file(filename=infile)

    # compute and apply noise
    noise = np.random.randn(len(sig))

    # compute powers
    noise_power = np.mean(np.power(noise, 2))
    sig_power = np.mean(np.power(sig, 2))

    # compute snr and scaling factor
    snr_linear = 10**(snr / 10.0)
    noise_factor = (sig_power / noise_power) * (1 / snr_linear)

    # add noise
    y = sig + np.sqrt(noise) * noise_factor

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
    Add a fade in and out effect to the audio file.

    Args:
        - infile (str) : input filename/path.
    """
    # read input file
    fs, sig = read_file(filename=infile)
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
    Normalize the signal given a certain technique (peak or rms).

    Args:
        - infile                  (str) : input filename/path.
        - normalization_technique (str) : type of normalization technique to use. (default is peak)
        - rms_level               (int) : rms level in dB.
    """
    # read input file
    fs, sig = read_file(filename=infile)

    # normalize signal
    if normalization_technique == "peak" :
        y = sig / np.max(sig)

    elif normalization_technique == "rms":
        # linear rms level and scaling factor
        r = 10**(rms_level / 10.0)
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
