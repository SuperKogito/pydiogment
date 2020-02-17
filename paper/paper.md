---
title: 'Pydiogment: A Python package for audio augmentation'
tags:
  - Python
  - Signal processing
  - Data augmentation
  - Audio classification
authors:
  - name: Ayoub Malek
    orcid: 0000-0003-0872-7098
    affiliation: "1"
  - name: Hasna Marwa Malek
    orcid: 0000-0003-0872-7098
    affiliation: "2"
affiliations:
 - name: Technical University of Munich
   index: 1
 - name: Grenoble Institute of Technology (Grenoble INP)
   index: 2
date: 25 February 2020
bibliography: paper.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
aas-doi: 10.3847/xxxxx <- update this with the DOI from AAS once you know it.
aas-journal: The Journal of Open Source Software
---

# Summary
Audio data augmentation is a key step in training Machine Learnign (ML) models to solve audio classification tasks.
It is applied to increase the quality and size of the labeled training data set, in order to improve the recognition accuracy.
Data augmentation is simply a deformation technique, that helps stretch the data, and increase its size for a better training.
Unlike image augmentation, audio augmentation is still limit explored by research and most deformation strategies manipulate the computed spectorams rather than the raw audio. With the exception of few libraries constrained to work with Pytorch [@pytorch:2019], most existing tools in this context either act on spectograms such as Google's Specaugment [@specaugment:2019], or are developed for music data augmentation like muda [@muda:2015]. This paper describes version 0.1.0 of `Pydiogment`: a Python package for audio augmentation based on the scipy [@scipy:2001] and ffmpeg [@ffmpeg:2019] libraries.
`Pydiogment` implements various augmentation techniques that can be used to improve the accuracy of various recognition tasks (speaker recognition, spoken emotions recognition, speech recognition etc.) and avoid over-fitting when training models.
The paper provides a brief overview of the library’s functionality, along with a small emotions recognition experiment displaying the utility of the library.

# Implementation and theory

`Pydiogment` includes 3 general categories of deformations / augmentations:

|

- **Amplitude based augmentations** (`auga.py`) **:**
  - Apply Gain : applies a given gain (in dB) to the input signal.
  - Add Fade : adds a fade-in and fade-out effects to the original signal.
  - Normalize : normalizes the signal using either the peak normalization method or the root means square approach.
  - Add Noise : adds some random noise to the input signal based on a given signal to noise ratio (SNR).

|

- **Frequency based augmentation** (`augf.py`) **:**
  - Change tone:
  changes the pitch of the audio (lowered or raised).
  - Convolve with impulse response : convolves the signal with a given impulse signal to simulate a output channel in a different setup (for example: room with echo).
  - Apply Filter : apply various types of Butterworth filters (low-pass, high-pass or band-pass).

|

- **Time based augmentation** (`augt.py`) **:**
  - Time Stretching : slows down speeds up the original audio based on a given coefficient.
  - Time Shifting :  includes shifting the signal in a certain time direction or reversing the whole signal
  - Random Cropping : generates a randomly cropped audio based on the original signal.
  - Eliminate Silence : filters out silent frames from the input signal.
  - Resample : resamples the the input signal given an input sampling rate.

It is very important to maintain the semantic validity when augmenting the data.
*For example:* one cannot change tones when doing voice based gender classification and still expect tone to be a separating features of the predicted classes.

# Experiment & Results
To prove the utility of `Pydiogment`, we display its effect on a spoken emotions recognition task.
We use the Emo-DB data set  [@Burkhardt:2005] as a starting point, which is a small German audio data set simulating 7 different emotions (neutral, sadness, anger, boredom, fear, happiness, disgust).
In a first phase, we apply various recognition algorithms on the original data such as K-Nearest Neighbors (KNN), random forests, decision trees, Support Vector Machines (SVM) etc.
In a second phase, we augment the data using `Pydiogment` by applying the following techniques:

- slow down samples using a coefficient of 0.8.
- speed up samples coefficient of 1.2.
- randomly crop samples with a minimum length of 1 second.
- add noise with an SNR = 10
- add a fade in and fade out effect.
- apply gain of -100 dB.
- apply gain of -50 dB.
- convolve with noise file using a level = 10**-2.75.
- shift time with one second (1 sec) to the right (direction = right)
- shift time with one second (1 sec) to the left (direction = left)
- change tone with tone coefficient equal to 0.9.
- change tone with tone coefficient equal to 1.1.

Then we re-run the same algorithms on the augmented and original data. The following is a comparison of the results:
\begin{table}[h]
    \begin{tabular}{l*{6}{c}r}
        \hline
        \\Machine learning Algorithm  & Accuracy (no augmentation) & Accuracy (with augmentation) \\\\
        \hline
        KNN                         &             0.588          &           0.622              \\
        Decision Tree               &             0.474          &           0.568              \\
        AdaBoost                    &             0.258          &           0.429              \\
        Random Forest               &             0.639          &           0.753              \\
        Linear SVM                  &             0.113          &           0.286              \\
        Extra Trees Classifier      &             0.680          &           0.768              \\
        \hline
    \end{tabular}
\caption{ Accuracy comparison of results with and without data augmentation.}
\end{table}

\newpage

# Conclusion

This paper introduced `Pydiogment`, a Python package for audio data augmentation, with diverse audio deformation strategies.
These strategies aims to improve the accuracy of audio based recognition system by scaling the training data set and increasing its quality/diversity.
The utility of `Pydiogment` was proved by showing its effects when used in a spoken emotions recognition task. In the stated experiment, the augmentation using `Pydiogment` improved the accuracy up to 50%.


# References
