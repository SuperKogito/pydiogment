################################################################################
############################# tests for augt ###################################
################################################################################
import os
import pytest
from pydiogment.augt import slow_down, speed, random_cropping, shift_time


@pytest.mark.parametrize('test_file', ['tests/testfiles/test.wav'])
@pytest.mark.parametrize('coefficient', [0.5, 0.8])
def test_slow_down(test_file, coefficient):
    slow_down(test_file, coefficient=0.8)

    # check result
    fname = "%s_augmented_slowed.wav" % (test_file.split(".wav")[0])
    assert(os.path.isfile(fname))

    # delete generated file
    os.remove(fname)


@pytest.mark.parametrize('test_file', ['tests/testfiles/test.wav'])
@pytest.mark.parametrize('coefficient', [1.2, 1.5])
def test_speed(test_file, coefficient):
    speed(test_file, coefficient=1.2)

    # check result
    fname = "%s_augmented_speeded.wav" % (test_file.split(".wav")[0])
    assert(os.path.isfile(fname))

    # delete generated file
    os.remove(fname)


@pytest.mark.parametrize('test_file', ['tests/testfiles/test.wav'])
@pytest.mark.parametrize('min_len', [1])
def test_random_cropping(test_file, min_len):
    random_cropping(test_file, min_len)

    # check result
    fname = "%s_augmented_randomly_cropped_%s.wav" % (test_file.split(".wav")[0], str(min_len))
    assert(os.path.isfile(fname))

    # delete generated file
    os.remove(fname)


@pytest.mark.parametrize('test_file', ['tests/testfiles/test.wav'])
@pytest.mark.parametrize('tshift', [1])
@pytest.mark.parametrize('direction', ["left", "right"])
def test_shift_time(test_file, tshift, direction):
    shift_time(test_file, tshift, direction)

    # check result
    fname = "%s_augmented_%s_%s_shifted.wav" % (test_file.split(".wav")[0], direction, tshift)
    assert(os.path.isfile(fname))

    # delete generated file
    os.remove(fname)
