.. pydiogment documentation master file, created by
   sphinx-quickstart on Mon Dec  9 14:08:11 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pydiogment's documentation!
======================================

.. image:: _static/logo1.png
   :scale: 75 %
   :align: center


Pydiogment (python audio augmentation) aims to simplify audio augmentation.
It generates multiple audio files based on a starting mono audio file.
The library can generates files with higher speed, slower, and different tones etc.


Dependencies
------------

pydiogment is built using Python3_  and it requires the following:

-	Python packages:
  -	NumPy_ (>= 1.17.2) :  ``pip install numpy``
  -	SciPy_  (>= 1.3.1) :  ``pip install scipy``

  Or you can simply use the requirements file in ``pip install -r requirements.txt``

- Pydiogment also requires FFmpeg_, which you can install using: ``sudo apt install ffmpeg``


Installation
------------

If you already have a working installation of numpy and scipy, you can simply install pydiogment using pip:

  ``pip install pydiogment``

To update an exisiting pydiogment version use:

  ``pip install -U pydiogment``

Documentation
-------------

.. toctree::

   code


Citation
--------

  @software{ayoubmalek2020,
    author = {Ayoub Malek},
    title = {pydiogment/pydiogment: 0.1.0},
    month = Apr,
    year = 2020,
    version = {0.1.2},
    url = {https://github.com/SuperKogito/spafe}
  }


.. _Python3 : https://www.python.org/download/releases/3.0/
..	_NumPy : https://numpy.org/
..	_SciPy : https://scipy.org/
.. _FFmpeg : https://www.ffmpeg.org/
