## HP5334A/B Universal Counter driver for Python-IVI

A simple but functional driver for interacting with the HP 5334A and 5334B Universal Counters

### Requirements
  * tested with Python3.9.3 
  
### Dependencies
  * python-ivi https://github.com/python-ivi/python-ivi
  * python-vxi11 https://github.com/python-ivi/python-vxi11
  
### Installation
Using pip to install in editable mode seems the cleanest way to avoid pythons import troubles.
Editable allows one to make changes to the repository and have them instantly available in
their applicaton.  As an aside, using pip install -e . works perfectly well for both
python-ivi and the python-vxi11 repositories as well.
  * cd into repository
  * ```pip install -e .```

If pip refuses to install with an 'editable mode' error,
see [here](https://stackoverflow.com/a/73779542) for upgrading pip.

### Notes
  * developed for an HP5334B with an E2050A GPIB/ethernet bridge
  * none of the memory, math, or voltmeter functionality has been implemented
  * frequency, time_interval, period, ratio and totalize work well
  * with my older instruments, i had to define instr.term_char = '\n'.  I found
    this caused a conversion error during pack_int() of the python-vxi11
    library.  If you have the same problem, notes on how i worked around it
    are [here](https://github.com/python-ivi/python-vxi11/pull/26/commits/d6205bf8dd298a5b629304e5853595510519432c)

This has been a fun trip and I appreciate the work the Python-IVI
developers have invested.
