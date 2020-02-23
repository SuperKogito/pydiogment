import numpy as np
import matplotlib.pyplot as plt

def SNR_Set(sig, Desired_SNR_dB):
    """
   #  Filename SNR_Set_test.m
   #
   #  Tests the 'SNR_Set()" function.  Adds a predefined
   #  amount of random noise to a noise-free signal such that
   #  the noisy signal has a desired signal-to-noise ratio (SNR).
   #
   #  Author: Richard Lyons [December 2011]
    """
    len_sig = len(sig)
    noise   = np.random.randn(len_sig)

    sig_pow   = np.mean(sig**2)
    noise_pow = np.mean(noise**2)
    Initial_SNR = 10*(np.log10(sig_pow/noise_pow))

    K = (sig_pow/noise_pow) * 10**(-Desired_SNR_dB/10) # Scale factor

    New_Noise = np.sqrt(K)*noise # Change Noise level
    New_Noise_Power = np.mean(New_Noise**2)
    New_SNR = 10*(np.log10(sig_pow/New_Noise_Power))

    print(Initial_SNR, New_SNR)
    Noisy_Signal = sig + New_Noise
    return Noisy_Signal


# Create a noise-free signal
Npts = 128                                  # Number of time samples
n    = np.arange(0, Npts-1)                 # Time-domain index
Cycles = 5                                  # Integer number of cycles in noise-free sinwave signal
Signal = 3*np.sin(2*np.pi * Cycles * n / Npts) #  Real-valued noise-free signal

Desired_SNR_dB = 9# Set desired SNR in dB
Noisy_Signal = SNR_Set(Signal, Desired_SNR_dB)# Generate noisy signal

# Plot original and 'noisy' signals
plt.figure(1)
plt.subplots
plt.subplot(2,1,1)
plt.plot(n, Signal, '-bo')
plt.title('Original Signal')
plt.subplot(2,1,2)
plt.plot(n, Noisy_Signal, '-bo')
plt.title('Noisy Signal')
plt.xlabel('Time-samples')
plt.show()

# Measure SNR in freq domain
Spec     = np.fft.fft(Noisy_Signal)
Spec_Mag = np.abs(Spec) # Spectral magnitude
plt.figure(2)
plt.plot(Spec_Mag, '-bo')
plt.title('Spec Mag of Noisy Signal')
plt.xlabel('Freq-samples')
plt.ylabel('Linear')
plt.show()


Signal_Power = Spec_Mag[Cycles+1]**2 + Spec_Mag[Npts-Cycles+1]**2
Noise_Power  = np.sum(Spec_Mag**2) - Signal_Power
Measured_SNR = 10 * np.log10(Signal_Power/Noise_Power)
