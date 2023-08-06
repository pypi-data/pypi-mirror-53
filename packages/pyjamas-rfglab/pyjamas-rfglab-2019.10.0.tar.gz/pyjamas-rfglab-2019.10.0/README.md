# PyJAMAS 2019.8

[**Py**JAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) is **J**ust **A** **M**ore **A**wesome **S**iesta.

## Installing PyJAMAS
The easiest way to install [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) is using [PyPi](https://pypi.org/project/pyjamas-rfglab/). 

### A note on the *Python interpreter*
[PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) requires that you have [Python](https://www.python.org/downloads/) installed.  

[PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) has been extensively tested with with [Python 3.6.6](https://www.python.org/downloads/release/python-366/)--[Python 3.6.8](https://www.python.org/downloads/release/python-368/). [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) can probably work well with other Python 3 releases prior to 3.6.6.  

[PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) does **NOT** work with Python >= 3.7. The reason for this is that [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) uses some tools from [TensorFlow](https://www.tensorflow.org/), a machine learning package, and [TensorFlow](https://www.tensorflow.org/) is not yet friends with Python >= 3.7.  

[PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) does **NOT** work with Python 2. We try to use type annotations (whenever we remember), and the annotation style that we use is not supported in Python 2.


If you are interested in using [Python](https://www.python.org/downloads/) for your research, you should consider installing [Anaconda](https://www.anaconda.com/distribution/#download-section), a scientific Python distribution. The most recent version of [Anaconda](https://www.anaconda.com/distribution/#download-section) (a scientific Python distribution) comes with Python >= 3.7. To downgrade to [Python 3.6.8](https://www.python.org/downloads/release/python-368/), you can open a terminal and type:  

```python
conda install python=3.6.8
```

### MacOS and Linux
Open a terminal and type:  

```python
pip install pyjamas-rfglab
```

To run [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) type:  

```python
pyjamas
```

at the user prompt.  

### Windows
We recommend that, before installing [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/), you install [Anaconda](https://www.anaconda.com/distribution/#download-section) (a scientific Python distribution). In principle, the [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) [PyPi](https://pypi.org/project/pyjamas-rfglab/) package is self-contained, and will install all the necessary modules. However, in Windows there is an issue with [Shapely](https://pypi.org/project/Shapely/), a package used in [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) to represent geometric objects such as points or polygons. [Shapely](https://pypi.org/project/Shapely/) is based on [GEOS](https://trac.osgeo.org/geos/), a C++ library that comes with [Anaconda](https://www.anaconda.com/distribution/#download-section) but that fails to install with the [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) [PyPi](https://pypi.org/project/pyjamas-rfglab/) package. It is recommended to start by manually installing [Shapely](https://pypi.org/project/Shapely/). To that end, download the appropriate Shapely version from [this link](https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely). For example, use  Shapely‑1.6.4.post1‑cp36‑cp36m‑win_amd64.whl for a 64-bit machine running [Python 3.6]((https://www.python.org/downloads/release/python-368/)). Open a command prompt and change into the folder that contains the downloaded .whl file using the **cd** command. Complete the installation of [Shapely](https://pypi.org/project/Shapely/) by typing:

```python
pip install Shapely‑1.6.4.post1‑cp36‑cp36m‑win_amd64.whl
```
substituting the downloaded file name.


Once [Shapely](https://pypi.org/project/Shapely/), has been set up, you can proceed with a regular [PyPi](https://pypi.org/project/pyjamas-rfglab/) installation of [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/). Just be sure to read our note on the interpreter [above](#a-note-on-the-interpreter). After that, open a command prompt and type:  

```python
pip install pyjamas-rfglab
```

To run [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) type:  

```python
pyjamas
```

at the user prompt.  
