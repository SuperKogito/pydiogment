"""
- Description: frequency based augmentation techniques/manipulations for audio data.
- Author: Ayoub Malek
"""
import os
import math
import random
import tempfile
import warnings
import subprocess
import numpy as np
from .io import read_file, write_file


def convolve(infile, ir_name, level=0.5):
    """
    apply convolution to infile using the given impulse response file.

    Args:
        infile  (str) : input filename/path.
        ir_name (str) : name of impulse response file.
        level (float) : can be between 0 and 1, default value = 0.5
    """
    # read input file
    fs1, x = read_file(filename=infile)
    x = np.copy(x)

    # change the path below for the sounds folder
    ir_path = 'pydiogment/sounds/{0}.wav'.format(ir_name)
    fs2, ir = read_file(filename=ir_path)

    # apply convolution
    y = np.convolve(x, ir, 'full')[0:x.shape[0]] * level + x * (1 - level)

    # normalize
    y /= np.mean(np.abs(y))

    # export data to file
    input_file_name = os.path.basename(infile)
    output_file_path = os.path.dirname(infile)
    name_attribute = "_augmented_{0}_convolved_with_level_{1}.wav".format(ir_name, level)
    write_file(output_file_path=output_file_path,
               input_file_name=infile,
               name_attribute=name_attribute,
               sig=y,
               fs=fs1)


def change_tone(infile, tone):
    """
    change the tone of an audio file.

    Args:
        infile (str) : input audio filename.
        tone   (int) : tone to change.
    """
    # read input file
    fs, sig = read_file(filename=infile)

    # prepare file names for the tone changing command
    input_file_name = os.path.basename(infile).split(".wav")[0]
    output_file_path = os.path.dirname(infile)
    name_attribute = "_augmented_%s_toned.wav" % str(tone)
    outfile = os.path.join(output_file_path, input_file_name + name_attribute)

    # change tone
    tone_change_command = ["ffmpeg", "-i", infile,
                           "-af", f"asetrate={fs}*{tone},aresample={fs}", outfile]

    _ = subprocess.Popen(tone_change_command,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
