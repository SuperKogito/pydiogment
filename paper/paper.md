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
 - name: Grenoble Institute of Technology
   index: 2
date: 25 February 2020
bibliography: paper.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
aas-doi: 10.3847/xxxxx <- update this with the DOI from AAS once you know it.
aas-journal: The Journal of Open Source Software
---

# Summary
Audio data augmentation is a key step in training Machine Learning (ML) models to solve audio classification tasks.
It is applied to increase the quality and size of the labeled training data-set, in order to improve the recognition accuracy.
Data augmentation is simply a deformation technique, that helps stretch the data, and increase its size for a better training.
Unlike image augmentation, audio augmentation is still limitly explored by research and most deformation strategies manipulate the computed spectograms rather than the raw audio. With the exception of few libraries constrained to work with Pytorch [@pytorch:2019], most existing tools in this context either act on spectograms such as Google's Specaugment [@specaugment:2019], or are developed for music data augmentation like muda [@muda:2015]. This paper describes version 0.1.0 of `Pydiogment`: a Python package for audio augmentation based on the Scipy [@scipy:2019] and FFmpeg [@ffmpeg:2019] libraries.
`Pydiogment` implements various augmentation techniques that can be used to improve the accuracy of various recognition tasks (speaker recognition, spoken emotions recognition, speech recognition etc.) and avoid over-fitting when training models.
The paper provides a brief overview of the library’s functionality, along with an emotions recognition experiment displaying the utility of the library.

# Implementation and theory
`Pydiogment` includes 3 general categories of deformations / augmentations:

## Amplitude based augmentations (`auga.py`)
  - **Apply Gain:** This deformation can be described as an amplification of the signal and the noise by applying a given gain (in dB) to the input signal. Note that excessive gain application can result in clipping [@self:2009].

  - **Add Fade:** adds fade-in and fade-out effects to the original signal. This is done by multiplying a hamming window with the original signal  $y[n] = x[n] \cdot w[n]$, where $x[n]$ is the original signal, $y[n]$ is the augmented signal and $w[n]$ is the computed hamming window  [@poularikas:1999].

  - **Normalize:** Normalization refers to the practice of applying a uniform amount of gain across a signal, where signal-to-noise ratio and general dynamics levels remain unchanged [@shelvock:2012]. The normalization can be applied using the peak normalization method $y[n] = \frac{ x[n]}{\max(x[n])}$ or the Root Mean Square (RMS) approach $y[n] = \sqrt{\frac{N \cdot 10^(\frac{r}{20})}{\sum_{i=0}^{N-1}x^2[i]}} \cdot x[n]$, where $x[n]$ is the original signal, $y[n]$ is the augmented signal, N is the length of $x[n]$ and $r$ is the input RMS level in dB.

  - **Add Noise:** Additive White Gaussian Noise (AWGN) is added to the input signal based on a given signal-to-noise ratio (SNR) in dB :
  \begin{equation}
      y[n] = x[n] + \sqrt{\frac{P_x}{P_{awgn}} \cdot 10^{-(\frac{SNR_{db}}{10})}} \cdot awgn[n]
  \end{equation}
  with $x[n]$ is the original signal, $y[n]$ is the augmented noisy signal, $awgn[n]$ is a random Gaussian white noise signal with standard deviation = 1 & mean = 0, $P_x$ & $P_{awgn}$ are respectively the signal power and noise power [@hari:2012].


## Frequency based augmentation (`augf.py`)
  - **Change tone:** a tone or pitch are sound's properties that allow ordering on a frequency-related scale. This is usually characterized by a fundamental frequency that can be adjusted without changing the tempo to provide a deformed audio, this is also know as pitch shifting [@bernsee:2005].

  - **Convolve:**  This is also called reverberating the audio and it consists of a convolution of the original signal with a given Room Impulse Response (RIR) to simulate an audio captured using far-field microphones in a different setup/channel $y[n] = x[n] * rir[n]$, where $x[n]$ is the original signal, $y[n]$ is the augmented signal and $rir[n]$ is the room impulse response [@raju:2018].

  - **Apply Filter:** apply various types of Scipy based Butterworth filters (low-pass, high-pass or band-pass).

  \begin{figure}[!htb]
      \minipage{0.32\textwidth}
        \includegraphics[width=\linewidth]{figs/lpass.png}
      \endminipage\hfill
      \minipage{0.32\textwidth}
        \includegraphics[width=\linewidth]{figs/bpass.png}
      \endminipage\hfill
      \minipage{0.32\textwidth}%
        \includegraphics[width=\linewidth]{figs/hpass.png}
      \endminipage
  \caption{Frequency-Gain graphs of the implemented Butterworth filers (left: low-pass, middle: band-pass, right: high-pass) with a low cutoff frequency of 300 $Hz$ and a high cutoff frequency of 3000 $Hz$.}
  \end{figure}

## Time based augmentation (`augt.py`)
  - **Stretch Time:** also known as time compression/expansion, it is reciprocal to pitch shifting. Essentially the audio is slowed-down or accelerated based on a given coefficient [@bernsee:2005].

  - **Shift Time:**  this includes shifting the signal in a certain time direction to create augmented signals with different chronological orders, and also reversing the whole signal.

  - **Crop:** generates a randomly cropped audio based on the original signal and minimum signal/audio length.

  - **Remove Silence:** filters out silent frames from the input signal using FFmpeg `silenceremove` filter [@ffmpeg:2019].

  - **Resample:** with the help of Scipy, the input signal is resampled given an input sampling rate with respect to the  Nyquist–Shannon sampling theorem.

The aforementioned augmentation strategies can be combined to generate various sub-strategies.
However, it is very crucial to maintain the semantic validity when augmenting the data.
*For example:* one cannot change tones when doing voice based gender classification and still expect tone to be a separating feature of the predicted classes.

# Experiment & Results
To prove the utility of `Pydiogment`, we display its effect on a spoken emotions recognition task.
We use the **Emo-DB** data-set  [@Burkhardt:2005] as a starting point, which is a small German audio data-set simulating 7 different emotions (neutral, sadness, anger, boredom, fear, happiness, disgust). We choose the Mel-Frequency Cepstral Coefficients (MFCCs) [@milner:2006] as the characterizing low-level audio features due to previous proved success on similar problems [@kandali:2008; @kishore:2013; @sreeram:2015; @dahake:2016]. The features are extracted using the python_speech_features library [@jameslyons:2020]. In a first phase and using the scikit-learn library [@scikitlearn:2011], we apply various recognition algorithms on the original data such as K-Nearest Neighbors (KNN), random forests, decision trees, Quadratic Discriminant Analysis (QDA), Support Vector Machines (SVM) etc.
In a second phase, we augment the data using `Pydiogment` by applying the following techniques:

- slow down samples using a coefficient of $0.8$.
- speed up samples coefficient of $1.2$.
- randomly crop samples with a minimum length of $1$ second.
- add noise with an SNR $= 10$ dB.
- add a fade in and fade out effect.
- apply gain of $-100$ dB.
- apply gain of $-50$ dB.
- convolve with noise file using a level $= 10^{-2.75}$.
- shift time with one second ($1$ sec) to the right (direction = right)
- shift time with one second ($1$ sec) to the left (direction = left)
- change tone with tone coefficient equal to $0.9$.
- change tone with tone coefficient equal to $1.1$.

Then we re-run the same recognition algorithms on the augmented and original data. The following is a comparison of the results:
\begin{table}[h]
    \begin{tabular}{l*{6}{c}r}
        \hline
        Machine learning Algorithm  & Accuracy (no augmentation) & Accuracy (with augmentation)\\
        \hline\hline
        AdaBoost                        &             0.309          &           0.513              \\
        Decision Tree                   &             0.454          &           0.764              \\
        Extra Trees Classifier          &             0.588          &           0.916              \\
        Gaussian Process                &             0.247          &           0.700              \\
        KNN                             &             0.629          &           0.867              \\
        Linear SVM                      &             0.608          &           0.693              \\
        MLP Classifier                  &             0.608          &           0.811              \\
        Naive Bayes                     &             0.577          &           0.610              \\
        QDA                             &             0.608          &           0.764              \\
        Random Forest                   &             0.567          &           0.929              \\
        \hline
    \end{tabular}
\caption{Accuracy comparison of results with and without data augmentation.}
\end{table}

# Conclusion
This paper introduced `Pydiogment`, a Python package for audio data augmentation, with diverse audio deformation strategies.
These strategies aim to improve the accuracy of audio based recognition system by scaling the training data-set and increasing its quality/diversity.
The utility of `Pydiogment` was proved by showing its effects when used in a spoken emotions recognition task.
In the stated experiment, the augmentation using `Pydiogment` improved the accuracy up to 50%.


# References
