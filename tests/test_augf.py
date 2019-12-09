################################################################################
############################# tests for augf ###################################
################################################################################
import os
import pytest
from pydiogment.augf import convolve, change_tone


@pytest.mark.parametrize('test_file', ['tests/testfiles/test.wav'])
@pytest.mark.parametrize('ir_name', ['tel_noise'])
@pytest.mark.parametrize('level', [0.5])
def test_convolve(test_file, ir_name, level):
    """
    test the convolution function.
    """
    # apply a convolution between the audio input file and a predefined file.
    convolve(infile=test_file, ir_name=ir_name, level=level)

    # check result
    fname = "{0}_augmented_{1}_convolved_with_level_{2}.wav".format(test_file.split(".wav")[0],
                                                                    ir_name,
                                                                    level)
    assert(os.path.isfile(fname))

    # delete generated file
    os.remove(fname)


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
    assert(os.path.isfile(fname))

    # delete generated file
    os.remove(fname)
