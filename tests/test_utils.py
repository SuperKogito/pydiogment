################################################################################
####################### tests for utils.filters ################################
################################################################################
import pytest
import numpy as np
from pydiogment.utils.filters import (butter_lowpass, butter_highpass,
                                      butter_bandpass, butter_filter)


@pytest.mark.parametrize('fs', [8000.0])
@pytest.mark.parametrize('low_cut', [50.0, 150.0, 300.0])
@pytest.mark.parametrize('high_cut', [1000.0, 2000.0, 3000.0])
@pytest.mark.parametrize('filter_type', ["low", "high", "band"])
@pytest.mark.parametrize('order', [3, 5, 6, 9])
def test_filters(fs, low_cut, high_cut, filter_type, order):
    """
    test function for low, high and bandpass filters.
    """
    # define input noisy signal.
    T = 0.05
    nsamples = T * fs
    t = np.linspace(0, nsamples, endpoint=False, retstep=T)[0]
    a  = 0.02
    f0 = 600.0
    x  = 0.1 * np.sin(2 * np.pi * 1.2 * np.sqrt(t))
    x += 0.01 * np.cos(2 * np.pi * 312 * t + 0.1)
    x += a * np.cos(2 * np.pi * f0 * t + .11)
    x += 0.03 * np.cos(2 * np.pi * 2000 * t)

    try:
        # filter signal
        y = butter_filter(x, fs, filter_type, low_cut, high_cut, order)

    except Exception as e:
        print(e)
