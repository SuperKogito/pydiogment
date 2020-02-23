<p align="center">
<img src="https://github.com/SuperKogito/pydiogment/blob/master/docs/icon.png?raw=true">
</p>

:bell:	pydiogment
==========

[![Build Status](https://travis-ci.org/SuperKogito/pydiogment.svg?branch=master)](https://travis-ci.org/SuperKogito/pydiogment) [![Documentation Status](https://readthedocs.org/projects/pydiogment/badge/?version=latest)](https://pydiogment.readthedocs.io/en/latest/?badge=latest) [![License](https://img.shields.io/badge/license-BSD%203--Clause%20License%20(Revised)%20-blue)](https://github.com/SuperKogito/pydiogment/blob/master/LICENSE) [![Python](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7-blue)](https://www.python.org/doc/versions/) [![Coverage Status](https://codecov.io/gh/SuperKogito/pydiogment/graph/badge.svg)](https://codecov.io/gh/SuperKogito/pydiogment) [![Coverage Status](https://coveralls.io/repos/github/SuperKogito/pydiogment/badge.svg?branch=master)](https://coveralls.io/github/SuperKogito/pydiogment?branch=master)

pydiogment aims to simplify audio augmentation. It generates multiple audio files based on a starting mono audio file. The library can generates files with higher speed, slower, and different tones etc.

:inbox_tray: Installation
============

Dependencies
------------

pydiogment requires:

-	[Python](https://www.python.org/download/releases/3.0/) (>= 3.5)  
-	[NumPy](https://numpy.org/) (>= 1.17.2)
  `pip install numpy`

-	[SciPy](https://www.scipy.org/)  (>= 1.3.1)
  `pip install scipy`


- [FFmpeg](https://www.ffmpeg.org/)
  `sudo apt install ffmpeg`



Installation
-------------

If you already have a working installation of numpy and scipy, you can simply install pydiogment using pip:

```
pip install -U pydiogment
```

:bulb:  How to use
==========

- ## Amplitude related augmentation
  - ### Apply a fade in and fade out effect
    ```python3
    from pydiogment.auga import fade_in_and_out

    test_file = "path/test.wav"
    fade_in_and_out(test_file)
    ```

  - ### Apply gain to file
    ```python3
    from pydiogment.auga import apply_gain

    test_file = "path/test.wav"
    apply_gain(test_file, -100)
    apply_gain(test_file, -50)
    ```

  - ### Add Random Gaussian Noise based on SNR to file
    ```python3
    from pydiogment.auga import add_noise

    test_file = "path/test.wav"
    add_noise(test_file, 10)
    ```


- ## Frequency related augmentation
  - ### Change file tone
    ```python3
    from pydiogment.augf import change_tone

    test_file = "path/test.wav"
    change_tone(test_file, 0.9)
    change_tone(test_file, 1.1)
    ```

- ## Time related augmentation    
  - #### Slow-down/ speed-up file
    ```python3
    from pydiogment.augt import slowdown, speed

    test_file = "path/test.wav"
    slowdown(test_file, coefficient=0.8)
    speed(test_file, coefficient=1.2)
    ```

  - ### Apply random cropping to the file
    ```python3
    from pydiogment.augt import random_cropping

    test_file = "path/test.wav"
    random_cropping(test_file, 1)
    ```

  - ### Change shift data on the time axis in a certain direction
    ```python3
    from pydiogment.augt import shift_time

    test_file = "path/test.wav"
    shift_time(test_file, 1,"right")
    shift_time(test_file, 1,"left")
    ```

:bookmark_tabs:  Documentation  
==============
A thorough documentation of the library is available under [pydiogment.readthedocs.io](https://pydiogment.readthedocs.io/en/latest/index.html).

:construction_worker:	 Contributing        
============

Contributions are welcome and encouraged. To learn more about how to contribute to pydiogment please refer to the [Contributing guidelines](https://github.com/SuperKogito/pydiogment/blob/master/CONTRIBUTING.md)

:tada:	Acknowledgment and credits     
============================
- The test file used in the pytests is [OSR_us_000_0060_8k.wav](https://www.voiptroubleshooter.com/open_speech/american/OSR_us_000_0060_8k.wav) from the [Open Speech Repository](https://www.voiptroubleshooter.com/open_speech/american.html).
