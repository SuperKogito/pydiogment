"""
Description: data augmentation techniques for speech data
based on: https://medium.com/@makcedward/data-augmentation-for-audio-76912b01fdf6

# A toolkit for augmenting audio data. Provides:
#
#     white noise augmentation
#     pitch augmentation
#     speed augmentation
#     background noise augmentation
#     value augmentation
#     feature extraction: MFCC, LMFBE & LMFBP
#     Vocal Tract Length Perturbation (VTLP)
#     The Synchronous Overlap and Add (SOLA)

to clean up voice:
sox infile.wav outfile.wav remix -  highpass 100 norm compand 0.05,0.2 6:-54,-90,-36,-36,-24,-24,0,-12 0 -90 0.1 vad -T 0.6 -p 0.2 -t 5 reverse reverse norm -0.5

"""
import os
import math
import random
import tempfile
import warnings
import subprocess
import numpy as np
from io import read_file, write_file


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

        # export data to file
        input_file_name = os.path.basename(infile)
        output_file_path = os.path.dirname(infile)
        name_attribute = "_augmented_randomly_cropped_%s.wav" % min_len

        write_file(output_file_path=output_file_path,
                   input_file_name=infile,
                   name_attribute=name_attribute,
                   sig=y,
                   fs=fs)

    else:
        warnings.warn(
            "min_len provided is greater than the duration of the song.")


def convolve(infile, ir_name, level=0.5):
    """
    apply convolution to infile using impulse response given

    Args:
        infile (str): Filename
        ir_name can be  'smartphone_mic' or 'classroom'
        level (float) : can be between 0 and 1, default value = 0.5
    """
    fs1, x = read_file(filename=infile)
    x = np.copy(x)

    # change the path below for the sounds folder
    ir_path = './sounds/{0}.wav'.format(ir_name)
    fs2, ir = read_file(filename=ir_path)

    # apply convolution
    y = np.convolve(x, ir, 'full')[0:x.shape[0]] * level + x * (1 - level)

    # normalize
    y /= np.mean(np.abs(y))

    # export data to file
    input_file_name = os.path.basename(infile)
    output_file_path = os.path.dirname(infile)
    name_attribute = "_augmented_{0}_convolved{1}.wav".format(ir_name, level)
    write_file(output_file_path=output_file_path,
               input_file_name=infile,
               name_attribute=name_attribute,
               sig=y,
               fs=fs1)


def apply_gain(infile, gain):
    """
    apply gain to infile

    Args:
        infile (str) : filename
        gain (float) : gain in dB (both positive and negative)
    """
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


def slowdown(input_file, coefficient=0.8):
    """
    slow or stretch a wave.
    """
    # set-up variables for paths and file names
    name_attribute = "_augmented_slowed.wav"
    output_file = input_file.split(".wav")[0] + name_attribute

    # apply slowing command
    cmd = f"ffmpeg -i {input_file} -filter:a \"atempo={coefficient}\" {output_file} > /dev/null"
    os.system(cmd)
    print("Writing data to " + output_file + ".")


def speed(input_file, coefficient=1.25):
    # set-up variables for paths and file names
    name_attribute = "_augmented_speeded.wav"
    output_file = input_file.split(".wav")[0] + name_attribute

    # apply slowing command
    cmd = f"ffmpeg -i {input_file} -filter:a \"atempo={coefficient}\" {output_file} > /dev/null"
    os.system(cmd)
    print("Writing data to " + output_file + ".")


def add_noise(infile, snr):
    """
    augment data using noise injection.

    Note:
        It simply add some random value into data by using numpy.

    Args:
        sig  (array) : audio data.
        snr  (int) : signal to noise ratio in dB.
    """
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

    # export data to file
    input_file_name = os.path.basename(infile)
    output_file_path = os.path.dirname(infile)
    name_attribute = "_augmented_%s_noisy.wav" % snr

    write_file(output_file_path=output_file_path,
               input_file_name=infile,
               name_attribute=name_attribute,
               sig=y,
               fs=fs)


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
    shift = int(tshift * fs) * int(direction == "left") - int(
        tshift * fs) * int(direction == "right")
    print(shift)

    # shift time
    augmented_sig = np.roll(sig, shift)

    # export data to file
    input_file_name = os.path.basename(infile)
    output_file_path = os.path.dirname(infile)
    name_attribute = "_augmented_%s_%s_shifted.wav" % (direction, shift)

    write_file(output_file_path=output_file_path,
               input_file_name=infile,
               name_attribute=name_attribute,
               sig=augmented_sig,
               fs=fs)


def reverse(infile):
    fs, sig = read_file(filename=infile)
    augmented_sig = sig[::-1]

    # export data to file
    input_file_name = os.path.basename(infile)
    output_file_path = os.path.dirname(infile)
    name_attribute = "_augmented_reversed.wav"

    write_file(output_file_path=output_file_path,
               input_file_name=infile,
               name_attribute=name_attribute,
               sig=augmented_sig,
               fs=fs)


def fade_in_and_out(infile):
    fs, sig = read_file(filename=infile)
    kernel = 0.5**np.arange(len(sig))
    window = np.hamming(len(sig))

    # augmented_sig = np.convolve(sig, window, mode='full')

    # export data to file
    input_file_name = os.path.basename(infile).split(".wav")[0]
    output_file_path = os.path.dirname(infile)
    name_attribute = "_augmented_fade_in_out.wav"

    # eliminate silence
    non_silence_sig, duration = eliminate_silence(
        input_path=infile,
        output_path=os.path.join(output_file_path,
                                 input_file_name + "_no_silence.wav"))

    # fade in and out
    window = np.hamming(len(non_silence_sig))
    augmented_sig = window * non_silence_sig
    augmented_sig /= np.mean(np.abs(augmented_sig))

    write_file(output_file_path=output_file_path,
               input_file_name=infile,
               name_attribute=name_attribute,
               sig=augmented_sig,
               fs=fs)


def change_tone(infile, tone):
    fs, sig = read_file(filename=infile)
    # export data to file
    input_file_name = os.path.basename(infile).split(".wav")[0]
    output_file_path = os.path.dirname(infile)
    name_attribute = "_augmented_%s_toned.wav" % tone
    outfile = os.path.join(output_file_path, input_file_name + name_attribute)
    cmd = f"ffmpeg -i {infile} -af asetrate={fs}*{tone},aresample={fs} {outfile}"
    os.system(cmd)
