<p align="center">
<img src="https://github.com/SuperKogito/pydiogment/blob/master/docs/icon.png?raw=true">
</p>

:bell:	Pydiogment
==========

[![Build Status](https://travis-ci.org/SuperKogito/pydiogment.svg?branch=master)](https://travis-ci.org/SuperKogito/pydiogment) [![Build status](https://ci.appveyor.com/api/projects/status/bnxaa6dw82cyhl5h?svg=true)](https://ci.appveyor.com/project/SuperKogito/pydiogment) [![Documentation Status](https://readthedocs.org/projects/pydiogment/badge/?version=latest)](https://pydiogment.readthedocs.io/en/latest/?badge=latest) [![License](https://img.shields.io/badge/license-BSD%203--Clause%20License%20(Revised)%20-blue)](https://github.com/SuperKogito/pydiogment/blob/master/LICENSE) [![Python](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7-blue)](https://www.python.org/doc/versions/) [![Coverage Status](https://codecov.io/gh/SuperKogito/pydiogment/graph/badge.svg)](https://codecov.io/gh/SuperKogito/pydiogment) [![Coverage Status](https://coveralls.io/repos/github/SuperKogito/pydiogment/badge.svg?branch=master)](https://coveralls.io/github/SuperKogito/pydiogment?branch=master) [![CodeFactor](https://www.codefactor.io/repository/github/superkogito/pydiogment/badge/master)](https://www.codefactor.io/repository/github/superkogito/pydiogment/overview/master)

**Pydiogment** aims to simplify audio augmentation. It generates multiple audio files based on a starting mono audio file. The library can generates files with higher speed, slower, and different tones etc.

:inbox_tray: Installation
============

Dependencies
------------

**Pydiogment** requires:

-	[Python](https://www.python.org/download/releases/3.0/) (>= 3.5)  
-	[NumPy](https://numpy.org/) (>= 1.17.2)
  
-	[SciPy](https://www.scipy.org/)  (>= 1.3.1)

- [FFmpeg](https://www.ffmpeg.org/)

### On Linux
On Linux you can use the following commands to get the libraries:
- Numpy: `pip install numpy`
- Scipy:  `pip install scipy`
- FFmpeg: `sudo apt install ffmpeg`

### On Windows
On Windows you can use the following installation binaries:
- Numpy: https://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy or if you have Python already installed you can use install it using `pip3 install numpy`
- Scipy: https://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy
- FFmpeg: https://ffmpeg.org/download.html#build-windows

### On MacOS
On MacOs, use homebrew to install the packages:
- Numpy:  `brew install numpy --with-python3`
- Scipy:  You need to first install a compilation tool like Gfortran using homebrew `brew install gfortran` when it's done, install Scipy `pip install scipy`
for more information and guidelines you can check this link: https://github.com/scipy/scipy/blob/master/INSTALL.rst.txt#mac-os-x
- FFmpeg: `brew install ffmpeg`


Installation
-------------
If you already have a working installation of [NumPy](https://numpy.org/) and [SciPy](https://www.scipy.org/) , you can simply install **Pydiogment** using pip:

```
pip install pydiogment
```
To update an existing version of  **Pydiogment**, use:
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
    slowdown(test_file, 0.8)
    speed(test_file, 1.2)
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
    shift_time(test_file, 1, "right")
    shift_time(test_file, 1, "left")
    ```
- ## Audio files format 
This library currently supports mono WAV files only.

:bookmark_tabs:  Documentation  
==============
A thorough documentation of the library is available under [pydiogment.readthedocs.io](https://pydiogment.readthedocs.io/en/latest/index.html).

:construction_worker:	 Contributing and bugs report      
============

Contributions are welcome and encouraged. To learn more about how to contribute to **Pydiogment** please refer to the [Contributing guidelines](https://github.com/SuperKogito/pydiogment/blob/master/CONTRIBUTING.md)

To report bugs, request a feature or just ask for help you can refer to the [issues](https://github.com/SuperKogito/pydiogment/issuesif) section.
Before reporting a bug please make sure it is not addressed by an older issue and make sure to add your operating system type, its version number and the versions of the dependencies used.

:tada:	Acknowledgment and credits     
============================
- The test file used in the pytests is [OSR_us_000_0060_8k.wav](https://www.voiptroubleshooter.com/open_speech/american/OSR_us_000_0060_8k.wav) from the [Open Speech Repository](https://www.voiptroubleshooter.com/open_speech/american.html).
