---
title: 'pydiogment: A Python package for audio augmentation'
tags:
  - Python
  - Signal processing
  - Data augmentation
authors:
  - name: Ayoub Malek
    orcid: 0000-0003-0872-7098
    affiliation: "1"
affiliations:
 - name: Yoummday GmbH
   index: 1
date: 15 February 2020
bibliography: paper.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
aas-doi: 10.3847/xxxxx <- update this with the DOI from AAS once you know it.
aas-journal: Astrophysical Journal <- The name of the AAS journal.
---

# Summary
peech augmentation is a common and effective strategy toavoid overfitting and improve on the robustness of an emo-tion recognition model. In this paper, we investigate for thefirst time the intrinsic attributes in a speech signal using themulti-resolution analysis theory and the Hilbert-Huang Spec-trum, with the goal of developing a robust speech augmenta-tion approach from raw speech data. Specifically, speech de-composition in a double tree complex wavelet transform do-main is realized, to obtain sub-speech signals; then, the HilbertSpectrum using Hilbert-Huang Transform is calculated for eachsub-band to capture the noise content in unseen environmentswith the voice restriction to 100−4000 Hz; finally, the speech-specific noise that varies with the speaker individual, scenar-ios, environment, and voice recording equipment, can be recon-structed from the top two high-frequency sub-bands to enhancethe raw signal. Our proposed speech augmentation is demon-strated using five robust machine learning architectures basedon the RAVDESS database, achieving up to 9.3 % higher accu-racy compared to the performance on raw data for an emotionrecognition task.Index Terms: Emotion Recognition, Speech Augmentation,Speech decomposition, Bidirectional LSTM−Attention


Audiogmenter: a MATLAB Toolbox for Audio Data AugmentationGianluca Maguoloa, Michelangelo Pacib, Loris Nannia, Ludovico Bonanaa DEI, University of Padua, viale Gradenigo 6, Padua, Italy. loris.nanni@unipd.itb BioMediTech, Faculty of Medicine and Health Technology, Tampere University, Arvo Ylpön katu 34, D 219, FI-33520,Tampere, FinlandAbstractAudio  data  augmentation  is  a  key  step  in  training  deep  neural  networks  for  solving  audioclassification tasks. In this paper,we introduce Audiogmenter, anovel audio data augmentation library in MATLAB. We provide 15different augmentation algorithms for raw audio data and 8 for spectrograms. We integrate the MATLAB built-in audio data augmenter with other methods that  proved their  effectivenessin  literature.  To  the  best  of  our  knowledge,  this  is  the  largestMATLAB audiodata  augmentation library  freely  available.  The  toolbox and its documentation can be downloaded at https://github.com/LorisNanni/AudiogmenterKeywordsAudio augmentation; Spectrogram; Convolutional neural network.1.IntroductionData augmentation for audio classification problems is a key step for achieving high classification performance,  especially for  smalldatasets, as they  arein  many audio-related applications[1]. Audio data augmentation techniques fall into two different categories, depending on whether they are directly applied to the audio signal[2]or toa spectrogram generated from theaudio signal[3]. At  the  moment, fewwell-performing  MATLAB  libraries  for  data  augmentation  are  available:Mauch et al.[4]released the Audio Degradation Toolbox, a library designed for reproducing the degradation  of  sound  due  to  low-quality  microphones,  noisy  environments  and  many other scenarios.Besides, MATLAB2019bcontains abuilt-in audio dataaugmenterthat enables simple audio transformations.Other libraries for audio data augmentation are available in other languages, such as Librosa [5]and Muda [6]for Python.In this paper,we propose a comprehensive libraryspecifically designedfor audio data augmentation,that includes all the methodsin [4]and manyother  methods  that  showed  their  efficiency  in  the  literature.  Our  library  contains15different methods for  the  augmentation  of  the  raw  audio  signalsand8 that  work  on  the  spectrogramsgenerated from the raw audios.Our goal is to create an audio data augmentation library that can supportresearchers in this field and representa good baseline for testing new data augmentation algorithms in the future.The library is available at https://github.com/LorisNanni/Audiogmenter.The rest of the paper is organized as follows: Section 2 describes the specific problem background and our strategy for audio data augmentation;Section 3 detailsthe implementation of the toolbox;Section 4 provides one illustrative example; in Section 5 conclusions are drawn.






The forces on stars, galaxies, and dark matter under external gravitational
fields lead to the dynamical evolution of structures in the universe. The orbits
of these bodies are therefore key to understanding the formation, history, and
future state of galaxies. The field of "galactic dynamics," which aims to model
the gravitating components of galaxies to study their structure and evolution,
is now well-established, commonly taught, and frequently used in astronomy.
Aside from toy problems and demonstrations, the majority of problems require
efficient numerical tools, many of which require the same base code (e.g., for
performing numerical orbit integration).

``pydiogment`` is an Astropy-affiliated Python package for galactic dynamics. Python
enables wrapping low-level languages (e.g., C) for speed without losing
flexibility or ease-of-use in the user-interface. The API for ``Gala`` was
designed to provide a class-based and user-friendly interface to fast (C or
Cython-optimized) implementations of common operations such as gravitational
potential and force evaluation, orbit integration, dynamical transformations,
and chaos indicators for nonlinear dynamics. ``Gala`` also relies heavily on and
interfaces well with the implementations of physical units and astronomical
coordinate systems in the ``Astropy`` package [@astropy] (``astropy.units`` and
``astropy.coordinates``).

``pydiogment`` was designed to be used by both astronomical researchers and by
students in courses on gravitational dynamics or astronomy.

# Mathematics

Single dollars ($) are required for inline mathematics e.g. $f(x) = e^{\pi/x}$

Double dollars make self-standing equations:

$$\Theta(x) = \left\{\begin{array}{l}
0\textrm{ if } x < 0\cr
1\textrm{ else}
\end{array}\right.$$


# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"

# Figures

Figures can be included like this: ![Example figure.](figure.png)

# Acknowledgements

We acknowledge contributions from Brigitta Sipocz, Syrtis Major, and Semyeong
Oh, and support from Kathryn Johnston during the genesis of this project.

# References
