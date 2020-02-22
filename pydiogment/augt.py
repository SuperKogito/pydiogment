"""
- Description: time based augmentation techniques/manipulations for audio data.
"""
import os
import math
import random
import warnings
import subprocess
import numpy as np
from .utils.io import read_file, write_file


def eliminate_silence(infile):
    """
    Eliminate silence from voice file using ffmpeg library.

    Args:
        - infile  (str) : Path to get the original voice file from.

    Returns:
        list including True for successful authentication, False otherwise and
        a percentage value representing the certainty of the decision.
    """
    # define output name if none specified
    output_path = infile.split(".wav")[0] + "_augmented_without_silence.wav"

    # filter silence in wav
    remove_silence_command = ["ffmpeg", "-i", infile,
                              "-af",
                              "silenceremove=stop_periods=-1:stop_duration=0.25:stop_threshold=-36dB",
                              "-acodec", "pcm_s16le",
                              "-ac", "1", output_path]
    out = subprocess.Popen(remove_silence_command,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    out.wait()

    with_silence_duration = os.popen(
        "ffprobe -i '" + infile +
        "' -show_format -v quiet | sed -n 's/duration=//p'").read()
    no_silence_duration = os.popen(
        "ffprobe -i '" + output_path +
        "' -show_format -v quiet | sed -n 's/duration=//p'").read()
    return with_silence_duration, no_silence_duration


def random_cropping(infile, min_len=1):
    """
    Crop the infile with an input minimum duration.

    Args:
        - infile    (str) : Input filename.
        - min_len (float) : Minimum duration for randomly cropped excerpt
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
    Slow or stretch a wave.

    Args:
        - infile        (str) : Input filename.
        - coefficient (float) : coefficient caracterising the slowing degree.
    """
    # set-up variables for paths and file names
    name_attribute = "_augmented_slowed.wav"
    output_file = input_file.split(".wav")[0] + name_attribute

    # apply slowing command
    slowing_command = ["ffmpeg", "-i", input_file, "-filter:a",
                       "atempo={0}".format(str(coefficient)),
                       output_file]
    print(" ".join(slowing_command))
    p = subprocess.Popen(slowing_command,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    output, error = p.communicate()
    print(output, error.decode("utf-8") )
    
    # for i in error.decode("utf-8") : print(i)
    print("Writing data to " + output_file + ".")


def speed(input_file, coefficient=1.25):
    """
    Speed or shrink a wave.

    Args:
        - infile        (str) : Input filename.
        - coefficient (float) : coefficient caracterising the speeding degree.
    """
    # set-up variables for paths and file names
    name_attribute = "_augmented_speeded.wav"
    output_file = input_file.split(".wav")[0] + name_attribute

    # apply slowing command
    speeding_command = ["ffmpeg", "-i", input_file, "-filter:a",
                        "atempo={0}".format(str(coefficient)),
                        output_file]
    _ = subprocess.Popen(speeding_command,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    print("Writing data to " + output_file + ".")


def shift_time(infile, tshift, direction):
    """
    Augment audio data by shifting the time in the file. Signal can be shifted
    to the left or right.

    Note:
        Time shifting is simply moving the audio to left/right with a random second.
        If shifting audio to left (fast forward) with x seconds, first x seconds will mark as 0 (i.e. silence).
        If shifting audio to right (back forward) with x seconds, last x seconds will mark as 0 (i.e. silence).

    Args:
        - infile    (str) : Input filename.
        - tshift    (int) : Signal time shift in seconds.
        - direction (str) : shift direction (to the left or right).
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
    """
    Inverses the input signal to play from the end to the beginning and writes it
    to an output file

    Args:
        - infile (str): Input filename.
    """
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



def resample_audio(infile, sr):
    """
    resample the signal according a new input sampling rate with respect to the
    Nyquist-Shannon theorem.

    Args:
        - infile (str) : input filename/path.
        - sr     (int) : new sampling rate.
    """
    # set-up variables for paths and file names
    output_file = "{0}_augmented_resampled_to_{1}.wav".format(infile.split(".wav")[0],
                                                            sr)

    # apply slowing command
    sampling_command = ["ffmpeg", "-i", infile, "-ar", str(sr), output_file]
    print(" ".join(sampling_command))
    out = subprocess.Popen(sampling_command,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    # # read input file
    # fs, sig = read_file(filename=infile)
    #
    # # compute the number of samples
    # number_of_samples = np.floor((sr / fs) * len(sig))
    #
    # # resample signal
    # y = resample(sig, number_of_samples)
    #
    # # construct file names
    # input_file_name = os.path.basename(infile).split(".wav")[0]
    # output_file_path = os.path.dirname(infile)
    # name_attribute = "_augmented_resampled_with_{}.wav".format(sr)
    #
    # # export data to file
    # write_file(output_file_path=output_file_path,
    #            input_file_name=infile,
    #            name_attribute=name_attribute,
    #            sig=y,
    #            fs=fs)
