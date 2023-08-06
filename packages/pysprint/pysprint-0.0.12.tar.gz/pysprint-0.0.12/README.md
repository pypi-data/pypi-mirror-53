
# PySprint 
[![Build Status](https://travis-ci.org/Ptrskay3/PySprint.svg?branch=master)](https://travis-ci.org/Ptrskay3/pysprint)
[![codecov](https://codecov.io/gh/Ptrskay3/PySprint/branch/master/graph/badge.svg)](https://codecov.io/gh/Ptrskay3/PySprint)
[![Maintainability](https://api.codeclimate.com/v1/badges/4e876c4899af3c4435b0/maintainability)](https://codeclimate.com/github/Ptrskay3/PySprint/maintainability)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


##### Spectrally Refined Interferometry for Python 
CURRENT RELEASE: 0.0.12 (ALPHA)

PySprint is a UI and API for interferogram evaluation. Under construction.
The GUI works only with 1920x1080 screen resolution. Lower resolution compatibility is queued on the To-Do List.


### Lastest upgrades:
  - Now pip installable, see below
  - Added CI/CD, next is CircleCI
  - Data editing features unittests done
  - Added CI along with some unittests
  - Started API
  - Numerous little fixes according to PEP8
  - Added autofit for CFF method, it will be improved later
  - Eval. methods are improved
  - Windows remember their last state, they open as they were closed
  - Added Settings panel for calibration
  - Added SPP Panel

### Known issues
* SPP Panel data storage should be rewritten
* Evaluation methods improvement
* The data loading AI sometimes produces unexpected results
* There might be unnecessary imports
* Some buttons has no effect yet.


### To-do list
* Screen resolution compatibility
* Clean up GUI from useless buttons
* ERROR HANDLING!
* Unittests
* Selectable units
* Possible performance enhancement by improving algorithms
* Possible new data manipulating features + new options for existing ones


### Installation

PySprint requires [Python 3](https://www.python.org/downloads/) to run.

```sh
$ pip install pysprint
```

Package requirements:
* To use the GUI, install [PyQt5](https://pypi.org/project/PyQt5/)
```sh
$ pip install PyQt5
```
or 
```sh
conda install -c dsdale24 pyqt5
```
* numpy, scipy, matplotlib, pandas, lmfit will be automatically collected.


## To Run the GUI
```python
from pysprint.main import main

main()
```
