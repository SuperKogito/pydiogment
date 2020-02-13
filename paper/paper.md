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
 - name: Yoummday GmbH
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

This paper describes version 0.1.0 of `Pydiogment`: a Python package for audio augmentation based on the scipy [@scipy:2001] and ffmpeg [@ffmpeg:2019] libraries.
`Pydiogment` implements various augmentation techniques that can be used to improve the accuracy of various recognition tasks (speaker recognition, spoken emotions recognition, speech recognition etc.) and avoid over-fitting when training models.
The paper provides a brief overview of the library’s functionality, along with a small emotions recognition experiment displaying the utility of the library.

# Implementation and theory

Audio data augmentation is a key step in training ML models to solve audio classification tasks.
It is applied to increase the quality and size of the labeled training data set, in order to improve the recognition accuracy.
Data augmentation is simply a deformation technique, that helps stretch the data, and increase its size for a better training.
`Pydiogment` includes 3 general categories of deformations / augmentations:

|

- **Amplitude based augmentations** (`auga.py`) **:**
\vskip 0.2cm
\begin{tabular}{lp{9cm}}
\textbf{- Apply Gain} &: applies a given gain (in dB) to the input signal. \\
\textbf{- Add Fade}   &: adds a fade-in and fade-out effects to the original signal. \\
\textbf{- Normalize}  &: normalizes the signal using the peak normalization method. \\
\textbf{- Add Noise}  &: adds some random noise to the input signal based on a given signal to noise ratio (SNR). \\
\end{tabular}

|

- **Frequency based augmentation** (`augf.py`) **:**
\vskip 0.2cm
\begin{tabular}{lp{9cm}}
\textbf{- Change tone}  &: changes the pitch of the audio (lowered or raised). \\
\textbf{- Apply Filter} &: ... \\
\end{tabular}

|

- **Time based augmentation** (`augt.py`) **:**
\vskip 0.2cm
\begin{tabular}{lp{8cm}}
\textbf{- Time Stretching}  &: slows down speeds up the original audio based on a given coefficient. \\
\textbf{- Time Shifting}    &: includes shifting the signal in a certain time direction or reversing the whole signal.\\
\textbf{- Random Cropping}  &: generates a randomly cropped audio based on the original signal. \\
\textbf{- Eliminate Silenc} &: filters out silent frames from the input signal. \\
\textbf{- Resample}         &: resamples the the input signal given an input sampling rate.\\
\end{tabular}

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

\newpage

# Conclusion

This paper introduced `Pydiogment`, a Python package for audio data augmentation, with diverse audio deformation strategies.
These strategies aims to improve the accuracy of audio based recognition system by scaling the training data set and increasing its quality/diversity.
The utility of `Pydiogment` was proved by showing its effects when used in a spoken emotions recognition task. In the stated experiment, the augmentation using `Pydiogment` improved the accuracy up to 50%.


# Acknowledgements

This work was supported by Yoummday GmbH.

# References
