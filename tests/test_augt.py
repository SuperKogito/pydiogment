################################################################################
############################# tests for augt ###################################
################################################################################
import os
import time
import pytest
from pydiogment.augt import (slow_down, speed, random_cropping, shift_time,
                             resample_audio, eliminate_silence, reverse)


@pytest.mark.parametrize('test_file', ['tests/testfiles/test.wav'])
def test_eliminate_silence(test_file):
    """
    test function for the silence removal.
    """
    eliminate_silence(test_file)

    # check result
    fname = test_file.split(".wav")[0] + "_augmented_without_silence.wav"
    time.sleep(1)
    assert(os.path.isfile(fname))


@pytest.mark.parametrize('test_file', ['tests/testfiles/test.wav'])
@pytest.mark.parametrize('coefficient', [0.5, 0.8])
def test_slow_down(test_file, coefficient):
    slow_down(test_file, coefficient=0.8)

    # check result
    fname = "%s_augmented_slowed.wav" % (test_file.split(".wav")[0])
    time.sleep(1)
    assert(os.path.isfile(fname))


@pytest.mark.parametrize('test_file', ['tests/testfiles/test.wav'])
@pytest.mark.parametrize('coefficient', [1.2, 1.5])
def test_speed(test_file, coefficient):
    speed(test_file, coefficient=1.2)

    # check result
    fname = "%s_augmented_speeded.wav" % (test_file.split(".wav")[0])
    time.sleep(1)
    assert(os.path.isfile(fname))


@pytest.mark.parametrize('test_file', ['tests/testfiles/test.wav'])
@pytest.mark.parametrize('min_len', [1])
def test_random_cropping(test_file, min_len):
    random_cropping(test_file, min_len)

    # check result
    fname = "%s_augmented_randomly_cropped_%s.wav" % (test_file.split(".wav")[0], str(min_len))
    assert(os.path.isfile(fname))


@pytest.mark.parametrize('test_file', ['tests/testfiles/test.wav'])
@pytest.mark.parametrize('tshift', [1])
@pytest.mark.parametrize('direction', ["left", "right"])
def test_shift_time(test_file, tshift, direction):
    shift_time(test_file, tshift, direction)

    # check result
    fname = "%s_augmented_%s_%s_shifted.wav" % (test_file.split(".wav")[0], direction, tshift)
    assert(os.path.isfile(fname))


@pytest.mark.parametrize('test_file', ['tests/testfiles/test.wav'])
def test_reverse(test_file):
    """
    test function for the reversing function.
    """
    reverse(test_file)

    # check result
    fname = "{0}_augmented_reversed.wav".format(test_file.split(".wav")[0])
    time.sleep(1)
    assert(os.path.isfile(fname))


@pytest.mark.parametrize('test_file', ['tests/testfiles/test.wav'])
@pytest.mark.parametrize('sr', [4000, 6000, 9000, 16000])
def test_resample_audio(test_file, sr):
    """
    test function for the resampling function.
    """
    resample_audio(test_file, sr)

    # check result
    fname = "{0}_augmented_resampled_to_{1}.wav".format(test_file.split(".wav")[0],
                                                         sr)
    time.sleep(1)
    assert(os.path.isfile(fname))
