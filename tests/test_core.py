import pytest
import numpy as np
import scipy.io.wavfile
from augmentation import *


@pytest.fixture
def sig():
    __EXAMPLE_FILE = 'test.wav'
    return scipy.io.wavfile.read(__EXAMPLE_FILE)[1]


@pytest.fixture
def fs():
    __EXAMPLE_FILE = 'test.wav'
    return scipy.io.wavfile.read(__EXAMPLE_FILE)[0]


def test_(sig, fs):
    slowdown(test_file, coefficient=0.8)


def test_(sig, fs):
    speed(test_file, coefficient=1.2)


def test_(sig, fs):
    random_cropping(test_file, 1)


def test_(sig, fs):
    add_noise(test_file, 10)


def test_(sig, fs):
    fade_in_and_out(test_file)


def test_(sig, fs):
    apply_gain(test_file, -100)


def test_(sig, fs):
    apply_gain(test_file, -50)


def test_(sig, fs):
    convolve(test_file, "noise", 10**-2.75)


def test_(sig, fs):
    shift_time(test_file, 1,"right")


def test_(sig, fs):
    shift_time(test_file, 1,"left")


def test_(sig, fs):
    change_tone(test_file, .9)


def test_(sig, fs):
    change_tone(test_file, 1.1)
