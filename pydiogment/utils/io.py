"""
Description: write and read module for wave data.
"""
import os
from scipy.io.wavfile import read, write


def read_file(filename):
    """
    read wave file as mono.

    Args:
        - filename (str) : wave file / path.

    Returns:
        tuple of sampling rate and audio data.
    """
    fs, sig = read(filename=filename)
    if (sig.ndim == 1):
        samples = sig
    else:
        samples = sig[:, 0]
    return fs, samples


def write_file(output_file_path, input_file_name, name_attribute, sig, fs):
    """
    read wave file as mono.

    Args:
        - filename         (str) : wave file / path.
        - output_file_path (str) : path to save resulting wave file to.
        - input_file_name  (str) : name of processed wave file,
        - name_attribute   (str) : attribute to add to output file name.
        - sig            (array) : signal/audio array.
        - fs               (int) : sampling rate.

    Returns:
        tuple of sampling rate and audio data.
    """
    # set-up the output file name
    fname = os.path.basename(input_file_name).split(".wav")[0] + name_attribute
    fpath = os.path.join(output_file_path, fname)
    write(filename=fpath, rate=fs, data=sig)
    print("Writing data to " + fpath + ".")
