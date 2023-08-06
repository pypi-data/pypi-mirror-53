## Introduction

This is a software for data acquisition box from DMT. The software is targeted to be extensible and usable on multiple operating system as it has the standard of the GNOME data acquisition implemented in it. The software is modular, such that units can be reprogrammed and inserted/added to the software, do that other devices can be supported. The data is written in HDF5 format, that is compatible with the GNOME experiment data standard. More information on that can be found in the GNOME book.

### A little information on modular nature of the software

The class `DataBatch` interprets the data received by the device. The class `DataAcquire` contains the code that reads data from the device. More information can be found in the comments of the code.

##Requirements

While the code is distributed as executable, it's originally written in Python and is converted to executable using Python's `cx_freeze`. In order to run the code through python, you need the following components of Python:

Python 3.4.x must be used. Not newer or older. It's recommended that you use Anaconda/Miniconda, and create an environment for Python 3.4.

| Addon name | Use |
| ------------------| -----|
|PyQt4 | Qt port to python |
| NumPy | Numerics processing library in machine language |
| SymPy | Symbolics processing for calculating observables through data channels |
| H5Py | hdf5 library port to Python |
| PySerial | Serial port access through Python |
| Matplotlib | Plotting library for Python |
| cx_freeze | For creating the executable |

All these can be installed using `pip` using the command `pip install addon_name` or `easy_install addon_name` or `conda install addon_name`, where `addon_name` is the addon name from the table (in small case). Normally everything works fine with pip, but h5py is problematic, and for that you can use `conda`.

It wasn't possible to move to Python 3.5 due to a problem in cx_freeze. It wasn't also possible to move to PyQt5 because cx_freeze doesn't support it very well.

## Creating the installer (for Windows)
If you wish to create the installer, you should install [NSIS installer](http://nsis.sourceforge.net/Main_Page). The script `build.bat` creates the installer for you. For that to work, however, you should have the nsis executable in your system's `PATH`. You should also have `cx_freeze` that will create the Python executable before packaging the installer. You also have to have GOW installed on your system, as it uses some linux commands.