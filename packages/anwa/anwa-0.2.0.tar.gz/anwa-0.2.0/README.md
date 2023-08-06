  
[![Build Status](https://travis-ci.org/mjirik/anwa.svg?branch=master)](https://travis-ci.org/mjirik/anwa)
[![Coverage Status](https://coveralls.io/repos/github/mjirik/anwa/badge.svg?branch=master)](https://coveralls.io/github/mjirik/anwa?branch=master)
[![PyPI version](https://badge.fury.io/py/anwa.svg)](http://badge.fury.io/py/anwa)


# anwa

Automatic animal detection in video


# Install on Windows

* Install [miniconda](https://docs.conda.io/en/latest/miniconda.html) and during install add conda to path


* In command line (`cmd` on Windows) use:

```cmd
conda create -n anwa_app -c conda-forge -c mjirik --yes anwa pywin32 imageio-ffmpeg
conda activate anwa_app
python -m anwa install
```


# Install on Linux and OsX

* Install [miniconda](https://docs.conda.io/en/latest/miniconda.html) and during install add conda to path


* In command line use:

```cmd
conda create -n anwa_app -c conda-forge -c mjirik --yes anwa imageio-ffmpeg
```

## Run 
```cmd
conda activate anwa_app
python -m anwa
```
