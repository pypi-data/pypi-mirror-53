Micrograph Junker
=================

An ultra-simple tool for manually culling micrographs, i.e. from cryo-EM 
data sets. 

Installation
------------

Create a conda environment for `junker`::

    conda create -n env_junker python=3.7
    source activate env_junker
    conda install numpy scipy skimage pyside2
    pip install mrcz
    
Usage
-----

Navigate to your target directory,

    source activate env_junker
    junker

The tool will create PNGs from every `.mrc, .mrcz` file in the directory, and 
shows a GUI that you can use to navigate. 

- 'Spacebar': moves the image to a 'junk' subdirectory.
- 'Enter': moves the image to a 'salvage' subdirectory.
- 'Z': undos the image move.
