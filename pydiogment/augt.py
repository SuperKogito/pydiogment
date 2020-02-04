"""
Description: time based augmentation techniques/manipulations for audio data.
Author: Ayoub Malek
"""
import os
import math
import random
import tempfile
import warnings
import subprocess
import numpy as np
from .io import read_file, write_file


def eliminate_silence(input_path, output_path):
    """
    Eliminate silence from voice file using ffmpeg library.

    Args:
        input_path  (str) : Path to get the original voice file from.
        output_path (str) : Path to save the processed file to.

    Returns:
        (list)  : List including True for successful authentication, False
                  otherwise and a percentage value representing the certainty
                  of the decision.
    """
    # filter silence in mp3 file
    filter_command = [
        "ffmpeg", "-i", input_path, "-af", "silenceremove=1:0:0.05:-1:1:-36dB",
        "-ac", "1", "-ss", "0", "-t", "90", output_path, "-y"
    ]
    out = subprocess.Popen(filter_command,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    out.wait()

    with_silence_duration = os.popen(
        "ffprobe -i '" + input_path +
        "' -show_format -v quiet | sed -n 's/duration=//p'").read()
    no_silence_duration = os.popen(
        "ffprobe -i '" + output_path +
        "' -show_format -v quiet | sed -n 's/duration=//p'").read()

    # print duration specs
    try:
        print("%-32s %-7s %-50s" %
              ("ORIGINAL SAMPLE DURATION", ":", float(with_silence_duration)))
        print("%-23s %-7s %-50s" % ("SILENCE FILTERED SAMPLE DURATION", ":",
                                    float(no_silence_duration)))
    except BaseException:
        print("WaveHandlerError: Cannot convert float to string",
              with_silence_duration, no_silence_duration)

    # convert file to wave and read array
    load_command = ["ffmpeg", "-i", output_path, "-f", "wav", "-"]
    p = subprocess.Popen(load_command,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    data = p.communicate()[0]
    audio_np = np.frombuffer(data[data.find(b'\x00data') + 9:], np.int16)

    # delete temp silence free file, as we only need the array
    # os.remove(output_path)
    return audio_np, no_silence_duration


def random_cropping(infile, min_len=1):
    """
    cropping the infile with a minimum duration of min_len

    Args:
        infile (str): Filename
        min_len (float) : Minimum duration for randomly cropped excerpt
    """
    fs, x = read_file(filename=infile)
    t_end = x.size / fs
    if (t_end > min_len):
        # get start and end time
        start = random.uniform(0.0, t_end - min_len)
        end = random.uniform(start + min_len, t_end)

        # crop data
        y = x[int(math.floor(start * fs)):int(math.ceil(end * fs))]

        # construct file names
        input_file_name = os.path.basename(infile)
        output_file_path = os.path.dirname(infile)
        name_attribute = "_augmented_randomly_cropped_%s.wav" % str(min_len)

        # export data to file
        write_file(output_file_path=output_file_path,
                   input_file_name=infile,
                   name_attribute=name_attribute,
                   sig=y,
                   fs=fs)

    else:
        warning_msg = """
                      min_len provided is greater than the duration of the song.
                      """
        warnings.warn(warning_msg)

def slow_down(input_file, coefficient=0.8):
    """
    slow or stretch a wave.
    """
    # set-up variables for paths and file names
    name_attribute = "_augmented_slowed.wav"
    output_file = input_file.split(".wav")[0] + name_attribute

    # apply slowing command
    slowing_command = ["ffmpeg", "-i", input_file, "-filter:a",
                      '"atempo=', str(coefficient) + '"',
                       output_file, "> /dev/null"]
    _ = subprocess.Popen(slowing_command,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    print("Writing data to " + output_file + ".")


def speed(input_file, coefficient=1.25):
    # set-up variables for paths and file names
    name_attribute = "_augmented_speeded.wav"
    output_file = input_file.split(".wav")[0] + name_attribute

    # apply slowing command
    speeding_command = ["ffmpeg", "-i", input_file, "-filter:a",
                        '"atempo=', str(coefficient) + '"',
                        output_file, "> /dev/null"]
    _ = subprocess.Popen(speeding_command,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    print("Writing data to " + output_file + ".")


def shift_time(infile, tshift, direction):
    """
    Augment data using noise injection.

    Note:
        Time shifting is simply moving the audio to left/right with a random second.
        If shifting audio to left (fast forward) with x seconds, first x seconds will mark as 0 (i.e. silence).
        If shifting audio to right (back forward) with x seconds, last x seconds will mark as 0 (i.e. silence).

    Args:
        sig  (array) : audio data.
        fs     (int) : sampling rate.
        k      (int) : noise factor.

    Returns:
        audio data with noise.
    """
    fs, sig = read_file(filename=infile)
    shift = int(tshift * fs) * int(direction == "left") - \
            int(tshift * fs) * int(direction == "right")

    # shift time
    augmented_sig = np.roll(sig, shift)

    # construct file names
    input_file_name = os.path.basename(infile)
    output_file_path = os.path.dirname(infile)
    name_attribute = "_augmented_%s_%s_shifted.wav" % (direction, tshift)

    # export data to file
    write_file(output_file_path=output_file_path,
               input_file_name=infile,
               name_attribute=name_attribute,
               sig=augmented_sig,
               fs=fs)


def reverse(infile):
    fs, sig = read_file(filename=infile)
    augmented_sig = sig[::-1]

    # construct file names
    input_file_name = os.path.basename(infile)
    output_file_path = os.path.dirname(infile)
    name_attribute = "_augmented_reversed.wav"

    # export data to file
    write_file(output_file_path=output_file_path,
               input_file_name=infile,
               name_attribute=name_attribute,
               sig=augmented_sig,
               fs=fs)
