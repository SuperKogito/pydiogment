"""
Description: implements the scipybased Butterworth filters.
bandpas: https://stackoverflow.com/questions/12093594/how-to-implement-band-pass-butterworth-filter-with-scipy-signal-butter
highpass: https://stackoverflow.com/questions/39032325/python-high-pass-filter
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz


def butter_lowpass(cutoff, fs, order=5):
    """
    design lowpass filter.

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
    design a highpass filter.

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
    design band pass filter.

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
    apply filter to signal.

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


def plot_freq_response(ftype="low", low_cut=50, high_cut=2000, fs=8000):
    # Plot the frequency response for a few different orders.
    plt.figure()
    for order in [3, 6, 9]:
        if   ftype == "band" : b, a = butter_bandpass(low_cut, high_cut, fs, order)
        elif ftype == "high" : b, a = butter_highpass(high_cut, fs, order)
        else                 : b, a = butter_lowpass(low_cut,  fs, order)
        w, h = freqz(b, a, worN=2000)
        plt.plot((fs * 0.5 / np.pi) * w, abs(h), label="order = %d" % order)

    plt.plot([0, 0.5 * fs], [np.sqrt(0.5), np.sqrt(0.5)],
             '--', label='sqrt(0.5)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain')
    plt.grid(True)
    plt.legend(loc='best')
    plt.show()


if __name__ == "__main__":

    ###########################################################################
    ######################### Butterworth filters #############################
    ###########################################################################

    # init sample rate and desired cutoff frequencies (in Hz).
    fs       = 8000.0
    low_cut  = 300.0
    high_cut = 3000.0

    for filter_type in ["low", "high", "band"]:
        # plot the frequency response for a few different orders.
        plot_freq_response(ftype=filter_type, low_cut=low_cut, high_cut=high_cut)

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

        # filter signal
        y = butter_filter(x, fs, filter_type, low_cut, high_cut, order=6)

        # plot input and filtered signal
        plt.figure()
        plt.plot(t, x, label='Noisy signal')
        plt.plot(t, y, label='Filtered signal (%g Hz)' % f0)
        plt.xlabel('time (seconds)')
        plt.hlines([-a, a], 0, T, linestyles='--')
        plt.grid(True)
        plt.axis('tight')
        plt.legend(loc='upper left')
        plt.show()
