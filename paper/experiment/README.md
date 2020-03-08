## Motivation
- To prove the utility of `Pydiogment` and the utility of the implemented augmentation techniques, we display its effect on a **spoken emotions recognition task**.

## Spoken Emotions Recognition Experiment

### Description
We use the [Emo-DB](http://emodb.bilderbar.info/index-1280.html) as a starting point, which is a small German audio data-set simulating 7 different emotions (neutral, sadness, anger, boredom, fear, happiness, disgust). We choose the [Mel-Frequency Cepstral Coefficients (MFCCs)](https://en.wikipedia.org/wiki/Mel-frequency_cepstrum) as the characterizing low-level audio features due to previous proved success on similar problems. The features are extracted using the [python_speech_features](https://github.com/jameslyons/python_speech_features) library.


In a first phase and using the [scikit-learn library](https://scikit-learn.org/stable/), we apply various recognition algorithms on the original data such as K-Nearest Neighbors (KNN), random forests, decision trees, Support Vector Machines (SVM) etc.
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

The results are under `results.txt`.


### How to replicate
To replicate the experiment, please follow these instructions:
1. To get the data: `python3 _1_get_data.py`
2. To generate augmented data: `python3 _2_gen_augmentations.py`
3. To extract the features: `python3 _3_get_features.py`
4. To run the experiment: `python3 _4_run_experiment.py`

To pass the the experiment's output to a results file use:
`python3 _4_run_experiment.py > results.txt`
