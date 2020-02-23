"""
- Description: frequency based augmentation techniques/manipulations for audio data.
"""
import os
import subprocess
import numpy as np
from .utils.filters import butter_filter
from .utils.io import read_file, write_file


def convolve(infile, ir_fname, level=0.5):
    """
    Apply convolution to infile using the given impulse response file.

    Args:
        - infile   (str) : input filename/path.
        - ir_fname (str) : name of impulse response file.
        - level  (float) : can be between 0 and 1, default value = 0.5
    """
    # read input file
    fs1, x = read_file(filename=infile)
    x = np.copy(x)

    # change the path below for the sounds folder
    fs2, ir = read_file(filename=ir_fname)

    # apply convolution
    y = np.convolve(x, ir, 'full')[0:x.shape[0]] * level + x * (1 - level)

    # normalize
    y /= np.mean(np.abs(y))

    # export data to file
    input_file_name = os.path.basename(infile)
    output_file_path = os.path.dirname(infile)
    name_attribute = "_augmented_{0}_convolved_with_level_{1}.wav".format(os.path.basename(ir_fname.split(".")[0]),
                                                                          level)
    write_file(output_file_path=output_file_path,
               input_file_name=infile,
               name_attribute=name_attribute,
               sig=y,
               fs=fs1)


def change_tone(infile, tone):
    """
    Change the tone of an audio file.

    Args:
        - infile (str) : input audio filename.
        - tone   (int) : tone to change.
    """
    # read input file
    fs, sig = read_file(filename=infile)

    # prepare file names for the tone changing command
    input_file_name = os.path.basename(infile).split(".wav")[0]
    output_file_path = os.path.dirname(infile)
    name_attribute = "_augmented_%s_toned.wav" % str(tone)
    outfile = os.path.join(output_file_path, input_file_name + name_attribute)

    # change tone
    tone_change_command = ["ffmpeg", "-i", infile, "-af",
                           "asetrate="+str(fs) + "*" + str(tone) + ",aresample=" + str(fs),
                           outfile]

    _ = subprocess.Popen(tone_change_command,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)


def apply_filter(infile, filter_type, low_cutoff_freq, high_cutoff_freq=None, order=5):
    """
    Apply a certain type of Buttenworth filter on the input audio.

    Args:
        - infile             (str) : input audio filename.
        - filter_type        (str) : type of the filter to apply.
        - low_cutoff_freq  (float) : the low cut-off frequency of the filter.
        - high_cutoff_freq (float) : the high cut-off frequency of the filter.
        - order              (int) : filter order to define its accuracy.
    """
    # read input file
    fs, sig = read_file(filename=infile)

    # apply filter
    y = butter_filter(sig=sig, fs=fs, ftype=filter_type,
                      low_cut=low_cutoff_freq,
                      high_cut=high_cutoff_freq,
                      order=order)

    # export data to file
    input_file_name = os.path.basename(infile)
    output_file_path = os.path.dirname(infile)
    name_attribute = "_augmented_{0}_pass_filtered.wav".format(filter_type)
    write_file(output_file_path=output_file_path,
               input_file_name=infile,
               name_attribute=name_attribute,
               sig=y,
               fs=fs)
