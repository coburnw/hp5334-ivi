## HP5334A/B Universal Counter driver for Python-IVI

A rough but functional driver for the HP 5334B Universal Counter

### Requirements
  * tested with Python2.7.9 and Python3.6.3 
  
### Dependencies
  * python-ivi https://github.com/python-ivi/python-ivi
  * python-vxi11 https://github.com/python-ivi/python-vxi11
  
### Installation

The typical (and perhaps easiest) way to install found ivi drivers is to comingle them In-Tree with IVI's supplied drivers
#### In Tree ####
  * copy the drivers to the python-ivi/ivi/agilent folder.
  * edit the agilent/__init__.py file to allow python to find your new drivers.
  * rebuild and reinstall python-ivi.
  * fiddle with the example code.

If you prefer to keep them more separate, this method works well:
#### In Tree but separate ####
  * see this [gist](https://gist.github.com/coburnw/57634c7e821dd7f32e9a68e1d14c16a4)
  
### Notes
  * developed for an HP5334B with an E2050A GPIB/ethernet bridge
  * if any of the agilent5334 driver files are modified, python-ivi will
    need to be rebuilt and reinstalled
  * none of the memory, math, or voltmeter functionality has been implemented
  * frequency, time_interval, period, ratio and totalize work well
  * with my older instruments, i had to define instr.term_char = '\n'.  I found
    this caused a conversion error during pack_int() of the python-vxi11
    library.  If you have the same problem, notes on how i worked around it
    are [here] (https://github.com/python-ivi/python-vxi11/commit/3b9a0e9ea7788c24c61727854a0e997b46fbd3f9)

This has been a fun trip and I appreciate the work the Python-IVI
developers have invested.
