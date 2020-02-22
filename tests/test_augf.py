################################################################################
############################# tests for augf ###################################
################################################################################
import os
import time
import pytest
from pydiogment.augf import convolve, change_tone, apply_filter


@pytest.mark.parametrize('test_file', ['tests/testfiles/test.wav'])
@pytest.mark.parametrize('ir_fname', ['tel_noise'])
@pytest.mark.parametrize('level', [0.5, 0.25, 0.01])
def test_convolve(test_file, ir_fname, level):
    """
    test the convolution function.
    """
    # apply a convolution between the audio input file and a predefined file.
    convolve(infile=test_file, ir_fname=ir_fname, level=level)

    # check result
    fname = "{0}_augmented_{1}_convolved_with_level_{2}.wav".format(test_file.split(".wav")[0],
                                                                    ir_fname,
                                                                    level)
    time.sleep(1)
    assert(os.path.isfile(fname))


@pytest.mark.parametrize('test_file', ['tests/testfiles/test.wav'])
@pytest.mark.parametrize('tone', [0.9, 1.1])
def test_change_tone(test_file, tone):
    """
    test the tone changing function.
    """
    # change audio file tone
    change_tone(infile=test_file, tone=tone)

    # check result
    fname = "%s_augmented_%s_toned.wav" % (test_file.split(".wav")[0], str(tone))
    time.sleep(5)
    assert(os.path.isfile(fname))


@pytest.mark.parametrize('test_file', ['tests/testfiles/test.wav'])
@pytest.mark.parametrize('filter_type', [0.9, 1.1])
@pytest.mark.parametrize('low_cutoff_freq', [20, 30, 50, 100])
@pytest.mark.parametrize('high_cutoff_freq', [500, 700, 1200, 1500])
@pytest.mark.parametrize('order', [3, 5, 9])
def test_apply_filter(test_file, filter_type, low_cutoff_freq,
                      high_cutoff_freq, order):
    """
    test the Buttenworth filters.
    """
    # apply filter
    apply_filter(test_file, filter_type, low_cutoff_freq, high_cutoff_freq, order)

    # check result
    fname = "{0}_augmented_{1}_pass_filtered.wav".format(test_file.split(".wav")[0], filter_type)
    time.sleep(3)
    print(fname, os.path.isfile(fname))
    assert(os.path.isfile(fname))
