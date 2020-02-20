################################################################################
############################# tests for auga ###################################
################################################################################
import os
import time
import pytest
from pydiogment.auga import apply_gain, add_noise, fade_in_and_out, normalize


@pytest.mark.parametrize('test_file', ['tests/testfiles/test.wav'])
@pytest.mark.parametrize('gain', [-100, -50, -25])
def test_apply_gain(test_file, gain):
    """
    test apply gain function.
    """
    apply_gain(infile=test_file, gain=gain)

    # check result
    fname = "%s_augmented_with_%s_gain.wav" % (test_file.split(".wav")[0], str(gain))
    time.sleep(1)
    assert(os.path.isfile(fname))


@pytest.mark.parametrize('test_file', ['tests/testfiles/test.wav'])
@pytest.mark.parametrize('snr', [-3, -6, -20, -50, -100])
def test_add_noise(test_file, snr):
    """
    test adding noise function.
    """
    add_noise(test_file, snr)

    # check result
    fname = "%s_augmented_%s_noisy.wav" % (test_file.split(".wav")[0], str(snr))
    time.sleep(1)
    assert(os.path.isfile(fname))


@pytest.mark.parametrize('test_file', ['tests/testfiles/test.wav'])
def test_fade_in_and_out(test_file):
    """
    test function for adding a fade in and fade out effect.
    """
    fade_in_and_out(test_file)

    # check result
    fname = "%s_augmented_fade_in_out.wav" % (test_file.split(".wav")[0])
    time.sleep(1)
    assert(os.path.isfile(fname))


@pytest.mark.parametrize('test_file', ['tests/testfiles/test.wav'])
@pytest.mark.parametrize('normalization_technique', ['peak', 'rms'])
@pytest.mark.parametrize('rms_level', [-6, -3, 0, 3, 6])
def test_normalize(test_file, normalization_technique, rms_level):
    """
    test function for the normalization function.
    """
    normalize(test_file, normalization_technique, rms_level)

    # check result
    fname = "{0}_augmented_{1}_normalized.wav".format(test_file.split(".wav")[0],
                                                      normalization_technique)
    time.sleep(1)
    assert(os.path.isfile(fname))
