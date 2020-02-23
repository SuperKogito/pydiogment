"""
- Description: implements the scipybased Butterworth filters.
bandpas: https://stackoverflow.com/questions/12093594/how-to-implement-band-pass-butterworth-filter-with-scipy-signal-butter
highpass: https://stackoverflow.com/questions/39032325/python-high-pass-filter
"""
import numpy as np
from scipy.signal import butter, lfilter, freqz


def butter_lowpass(cutoff, fs, order=5):
    """
    Design lowpass filter.

    Args:
        - cutoff (float) : the cutoff frequency of the filter.
        - fs     (float) : the sampling rate.
        - order    (int) : order of the filter, by default defined to 5.
    """
    # calculate the Nyquist frequency
    nyq = 0.5 * fs

    # design filter
    low = cutoff / nyq
    b, a = butter(order, low, btype='low', analog=False)

    # returns the filter coefficients: numerator and denominator
    return b, a


def butter_highpass(cutoff, fs, order=5):
    """
    Design a highpass filter.

    Args:
        - cutoff (float) : the cutoff frequency of the filter.
        - fs     (float) : the sampling rate.
        - order    (int) : order of the filter, by default defined to 5.
    """
    # calculate the Nyquist frequency
    nyq = 0.5 * fs

    # design filter
    high = cutoff / nyq
    b, a = butter(order, high, btype='high', analog=False)

    # returns the filter coefficients: numerator and denominator
    return b, a


def butter_bandpass(low_cut, high_cut, fs, order=5):
    """
    Design band pass filter.

    Args:
        - low_cut  (float) : the low cutoff frequency of the filter.
        - high_cut (float) : the high cutoff frequency of the filter.
        - fs       (float) : the sampling rate.
        - order      (int) : order of the filter, by default defined to 5.
    """
    # calculate the Nyquist frequency
    nyq = 0.5 * fs

    # design filter
    low = low_cut / nyq
    high = high_cut / nyq
    b, a = butter(order, [low, high], btype='band')

    # returns the filter coefficients: numerator and denominator
    return b, a


def butter_filter(sig, fs, ftype="low", low_cut=50, high_cut=2000, order=5):
    """
    Apply filter to signal.

    Args:
        - sig      (array) : the signal array to filter.
        - fs       (float) : the sampling rate.
        - ftype      (str) : the filter type, by default defined to a low pass filter
        - low_cut  (float) : the low cutoff frequency, by default defined to  50Hz
        - high_cut (float) : the high cutoff frequency, by default defined to 2000Hz.
        - order      (int) : order of the filter, by default defined to 5.
    """
    if   ftype == "band" : b, a = butter_bandpass(low_cut, high_cut, fs, order)
    elif ftype == "high" : b, a = butter_highpass(high_cut, fs, order)
    else                 : b, a = butter_lowpass(low_cut,  fs, order)

    # filter signal
    y = lfilter(b, a, sig)
    return y
