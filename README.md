<p align="center">
<img style="width: 30%; height: 30%" src="https://github.com/drcandacemakedamoore/cleanX/blob/main/test/cleanXpic.png">
</p>

# cleanX

CleanX <a href="https://doi.org/10.5281/zenodo.4725904"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.4725904.svg" alt="(DOI)"></a> <a href="https://github.com/drcandacemakedamoore/cleanX/blob/master/LICENSE"><img alt="License: GPL-3" src="https://img.shields.io/github/license/drcandacemakedamoore/cleanX"></a>
is an open source [![Anaconda-Server Badge](https://anaconda.org/doctormakeda/cleanx/badges/license.svg)](https://anaconda.org/doctormakeda/cleanx) python library
for exploring, cleaning and augmenting large datasets of X-rays, or certain other types of radiological images.
JPEG files can be extracted from [DICOM](https://www.dicomstandard.org/) files or used directly.
[![Anaconda-Server Badge](https://anaconda.org/doctormakeda/cleanx/badges/platforms.svg)](https://anaconda.org/doctormakeda/cleanx)


### The latest official release:

<a href="https://pypi.org/project/cleanX/"><img alt="PyPI" src="https://img.shields.io/pypi/v/cleanX"></a>
[![Anaconda-Server Badge](https://anaconda.org/doctormakeda/cleanx/badges/version.svg)](https://anaconda.org/doctormakeda/cleanx)


primary author: Candace Makeda H. Moore

other authors + contributors: Oleg Sivokon, Andrew Murphy

## Continous Integration (CI) status

[![Sanity](https://github.com/drcandacemakedamoore/cleanX/actions/workflows/on-commit.yml/badge.svg)](https://github.com/drcandacemakedamoore/cleanX/actions/workflows/on-commit.yml)
[![Sanity](https://github.com/drcandacemakedamoore/cleanX/actions/workflows/on-tag.yml/badge.svg)](https://github.com/drcandacemakedamoore/cleanX/actions/workflows/on-tag.yml)


## Requirements

- a [python](https://www.python.org/downloads/) installation (3.7, 3.8 or 3.9)
- ability to create virtual environments (recommended, not absolutely necessary)
- tesseract-ocr, matplotlib, pandas, pillow and opencv
- optional recommendation of simpleITK or pydicom for DICOM/dcm to jpg conversion
- anaconda is now supported, but not technically necessary 


## Documentation

Online documentation at https://drcandacemakedamoore.github.io/cleanX/

You can also build up-to-date documentation by command.

Documentation can be generated by command:

``` sh
python setup.py apidoc
python setup.py build_sphinx
```

The documentation will be generated in `./build/sphinx/html` directory. Documentation is generated
automatically as new functions are added.

Special additional documentation for medical professionals with limited programming
ability is available on the wiki (https://github.com/drcandacemakedamoore/cleanX/wiki/Medical-professional-documentation).
To get a high level overview of some of the functionality of the program you
can look at the Jupyter notebooks inside workflow_demo. 

# Installation
- setting up a virtual environment is desirable, but not absolutely necessary

- activate  the environment
### Anaconda Installation

- use command for conda as below

        conda install -c doctormakeda -c conda-forge cleanx       

You need to specify both channels because there are some cleanX
dependencies that exist in both Anaconda main channel and in
conda-forge

### pip installation
- use pip as below

        pip install cleanX
    
    

## About using this library
If you use the library, please credit me and my collaborators.  You are only free to use this library according to license. We hope that if you use the library you will open source your entire code base, and send us modifications.  You can get in touch with me by starting a discussion (https://github.com/drcandacemakedamoore/cleanX/discussions/37) if you have a legitimate reason to use my library without open-sourcing your code base, or following other conditions, and I can make you specifically a different license.

We are adding new functions and classes all the time. Many unit tests are available in the test folder. Test coverage is currently partial. Some newly added functions allow for rapid automated data augmentation (in ways that are realistic for radiological data). Some other classes and functions are for cleaning datasets including ones that: 


        Get image and metadata out of dcm (DICOM) files into jpeg and csv files 

        Process datasets from csv or json or other formats to generate reports
        
        Run on dataframes to make sure there is no image leakage

        Run on a dataframe to look for demographic or other biases in patients
    
        Crop off excessive black frames (run this on single images) one at a time
       
        Run on a list to make a prototype tiny Xray others can be compared to
    
        Run on image files which are inside a folder to check if they are "clean"

        Take a dataframe with image names and return plotted(visualized) images  

        Run to make a dataframe of pics in a folder (assuming they all have the same 'label'/diagnosis)

        Normalize images in terms of pixel values (multiple methods)

All important functions are documented in the online documentation for programmers. You can also check out one of our videos by clicking the linked picture below:

[![Video](https://raw.githubusercontent.com/drcandacemakedamoore/cleanX/main/test/cleanXpic.png)](https://youtu.be/jaX5tXmiWrQ)
