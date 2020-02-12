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
affiliations:
 - name: Yoummday GmbH
   index: 1
date: 25 February 2020
bibliography: paper.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
aas-doi: 10.3847/xxxxx <- update this with the DOI from AAS once you know it.
aas-journal: The Journal of Open Source Software
---

# Summary

This paper describes version 0.1.0 of `pydiogment`: a Python package for audio augmentation, that can be used to improve various recognition tasks (speaker recognition, spoken emotions recognition, etc.).
The paper provides a brief overview of the library’s functionality, along with a small emotions recognition experiment displaying the utility of the library.

# Data Augmentation

Audio data augmentation is a key step in training ML models to solve audio classification tasks.
It is applied to increase the quality and size of the labeled training data set, in order to improve the recognition accuracy.
Data augmentation is simply a deformation technique, that helps stretch the data, and increase its size for a better training.
`pydiogment` includes 3 general categories of deformations / augmentations:

|

- `auga` **Amplitude based augmentations:**
  - *Apply Gain:*  This will apply a given gain (in dB) to the input signal.
  - *Add Fade:*    This adds a fade-in and fade-out effects to the original signal.
  - *Add Noise:*   This adds some random noise to the input signal based on a given signal to noise ratio (SNR).

|

- `augf` **Frequency based augmentation:**
  - *Change tone:* The pitch of the audio is changed (lowered or raised).
  - *Apply Filter:*

|

- `augt` **Time based augmentation:**
  - *Time Stretching:* This slows down speeds up the original audio based on a given coefficient.
  - *Time Shifting:* This includes shifting the signal in a certain time direction or reversing the whole signal.
  - *Random Cropping:* This generates a randomly cropped audio based on the original signal.
  - *Eliminate Silence:* This deformation can will filter out silent frames from the input signal.



It is very important to maintain the semantic validity when augmenting the data.
*For example:* one cannot change tones when doing voice based gender classification and still expect tone to be a separating features of the predicted classes.

# Experiment & Results
To prove the utility of `pydiogment`, we use it in a spoken emotions recognition task.
We use the Emo-DB data set  [@Burkhardt:2005] as a starting point, which is a small German audio data set simulating 7 different emotions (neutral, sadness, anger, boredom, fear, happiness, disgust).
We apply various recognition algorithms on the original data such as K-Nearest Neighbors (KNN), random forests, decision trees, Support Vector Machines (SVM) etc. then we augment the data using `pydiogment` and re-run the same algorithms.
The following is a comparison of the results:

| <sub> Machine learning Algorithm </sub>    | <sub> Accuracy (no augmentation) </sub> |  <sub> Accuracy (with augmentation) </sub> | <sub>Accuracy improvement</sub> |
|--------------------------------------------|-----------------------------------------|--------------------------------------------|---------------------------------|
| <sub>KNN  </sub>                           |      <sub>0.588</sub>                   |  <sub>0.622</sub>                          | <sub>0.05</sub>                 |
| <sub>Decision Tree  </sub>                 |      <sub>0.474</sub>                   |  <sub>0.568</sub>                          | <sub>0.09</sub>                 |
| <sub>AdaBoost </sub>                       |      <sub>0.258</sub>                   |  <sub>0.429</sub>                          | <sub>0.17</sub>                 |
| <sub>Random Forest </sub>                  |      <sub>0.639</sub>                   |  <sub>0.753</sub>                          | <sub>0.12</sub>                 |
| <sub>Linear SVM </sub>                     |      <sub>0.113</sub>                   |  <sub>0.286</sub>                          | <sub>0.17</sub>                 |
| <sub>Extra Trees Classifier </sub>         |      <sub>0.68</sub>                    |  <sub>0.768</sub>                          | <sub>0.08</sub>                 |



# Conclusion

This paper introduced `pydiogment`, a Python package for audio data augmentation, with diverse audio deformation strategies.
These strategies aims to improve the accuracy of audio based recognition system by scaling the training data set and increasing its quality/diversity.
The utility of `pydiogment` was proved by showing its effects when used in a spoken emotions recognition task. In the stated experiment, the augmentation using `pydiogment` improved the accuracy up to 50%.


# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

# Acknowledgements

This work was supported by Yoummday GmbH.s

# References
